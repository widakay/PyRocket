import credentials, boto, os, shutil, subprocess, json


class Project:
	def __init__(self, db, id=-1):
		if len(db.select('projects', where="id="+str(int(id))).list()) == 0:
			with db.transaction():
				self.id = db.insert('projects')
			if len(db.select('projects', where="id="+str(int(self.id))).list()) == 0:
				raise Exception("Error creating project")
		else:
			self.id = id
		self.folder = 'projects/project-' + str(int(self.id)) + '/'
		self.folderUrl = "https://pyrocketprojects.objects.dreamhost.com/" + self.folder
		self.url = '/project/'+str(self.id)
		self.image = self.folderUrl + "img.png"
		self.dlMac = ""
		self.state = 0

		data = db.select('projects', where="id="+str(int(self.id))).list()[0]
		self.name = data["name"]
		self.creator = data["creator"]
		self.created = data["created"]
		self.description = data["description"]
		self.state = data["state"]


		# restore project from database
		string = data["objectData"]

		if type(string) == type(None):
			string = "{}"
		data = json.loads(string)
		self.__dict__ = dict(self.__dict__.items() + data.items())
		self.db = db

	def __enter__(self):
		return self


	def addZip(self, zip):
		fileName = self.folder + 'src/' + zip.filename
		uploadFile(fileName, zip.value)

		mkdir(self.folder)
		mkdir(self.folder + 'src/')
		
		file = open(fileName, "w")
		file.write(zip.value)
		file.close()
		self.state = 1

	def finalize(self):
		self.state = 4
		self.saveState()
		print "finalizing..."
		mkdir(self.folder + 'mac/')
		fileName = self.folder + 'src/' + "main.py"

		with open(os.devnull, 'w') as devnull:
			subprocess.Popen(["sh", "Py2App.sh", self.folder+"src/", "main.py"], stdout=devnull, stderr=devnull)

		zipLocation = self.folder + "mac/app.zip"

		with open(zipLocation, mode='rb') as file: # b is important -> binary
			zipContent = file.read()
			file.close()

		uploadFile(self.folder + "mac/app.zip", zipContent, perms="public-read")

		with open ("resources/default-image.png", "r") as img:
			uploadFile(self.folder + "img.png", img.read(), perms="public-read")

		self.dlMac = self.folderUrl+"mac/app.zip"
		self.description = "THIS IS TOTALLY AWESOME"
		self.creator = 5
		self.name = "SomeApp"
		print "Done finalizing......"
		self.state = 5
		return

	def delete(self):
		self.state = -1

	def saveState(self):
		# save project to database
		data = dict(self.__dict__.items())
		print "___________"
		prev = self.db.select('projects', where="id="+str(int(self.id))).list()[0]
		for key in ["db", "created", "creator", "name", "description", "state"]:
			if key not in ["db", "created"]:
				print "|",key + ":", prev[key], "->", data[key]
				self.db.update('projects', where="id="+str(int(self.id)), **{key:data[key]})
			if key in data: del data[key]

		self.db.update('projects', where="id="+str(int(self.id)), objectData=json.dumps(data))
		print "----------"

	def __del__(self):
		self.saveState()
		try:
			shutil.rmtree(self.folder+'mac/')
		except OSError:
			pass



def mkdir(path):
	try:
		os.mkdir(path)
	except OSError, e:
		pass

def uploadFile(fileName, contents, perms="private"):
	bucket_name = 'pyrocketprojects'
	conn = boto.connect_s3(
		aws_access_key_id = credentials.access_key,
		aws_secret_access_key = credentials.secret_key,
		host = 'objects.dreamhost.com',
	)

	bucket = conn.get_bucket(bucket_name)
	key = bucket.new_key(fileName)
	key.set_contents_from_string(contents)
	key.set_acl(perms)