import web, random, json, os, subprocess, credentials

from Project import Project


import boto
from boto.s3.key import Key



render = web.template.render('templates/')

web.config.debug = False

		
urls = (
	'/upload', 'uploadRedir',
	'/project/(.*)/upload', 'upload',
	'/create', 'create',
	'/gallery', 'gallery',
	'/project/(.*)/finalize', 'finalize',
	'/project/(.*)/download', 'download',
	'/project/(.*)/download/(mac|lin|win)', 'downloadDirect',
	'/project/(.*)', 'project',
	'/static/(.*)', 'static',
	'/login', 'login',
	'/logout', 'logout',
	'/(.*)', 'index'
)
app = web.application(urls, globals())


db = web.database(dbn='mysql', db=credentials.mysql_database, user=credentials.mysql_username, pw=credentials.mysql_password)


#store = web.session.DiskStore('sessions')
store = web.session.DBStore(db, 'sessions')
session = web.session.Session(app, store)

class uploadRedir:
	def GET(self):
		project = setupSession()
		raise web.seeother(project.url+"/upload")


def setupSession():
	if session.get('projId', -1) == -1:
		project = Project(db)
		session.projId = project.id
	else:
		project = Project(db, id=session.projId)
	return project


class project:
	def GET(self, id):
		project = Project(db, id=id)
		return render.index("project", render.project(project))

class create:
	def GET(self):
		project = setupSession()

		#session.projId = db.select()
		raise web.seeother("/upload")
		
class upload:
	def GET(self, id):
		project = Project(db, id=id)
		return render.index("upload", render.uploadForm())

	def POST(self, id):
		project = Project(db, id=id)
		x = web.input(file={})

		project.addZip(x['file'])

		result = x['file'].filename
		return result


class finalize:
	def POST(self, id):
		project = Project(db, id=id)
		project.finalize()
		raise web.seeother("/project/"+str(int(id))+"/download")

	def GET(self, id):
		raise web.seeother("/project/"+str(int(id))+"/download")


class download:
	def GET(self, id):
		project = Project(db, id=id)
		title = project.name
		body = ""

		if project.state < 5:
			body += "Project is getting processed.  Please refresh page in 10 seoncds"
		else:
			url = project.dlMac
			body += "Your project can be downloaded here:<br>"
			body += "<a href='" + url + "'>Mac</a>"
		return render.index(title, body)


class downloadDirect:
	def GET(self, id, os):
		project = Project(db, id=id)
		url = project.dlMac

		if os == "mac":
			raise web.seeother(project.dlMac)
		else:
			raise web.seeother(project.url+"/download")
		title = "HELLO!"
		body = "Your project can be downloaded here:<br>"
		body += "<a href='" + url + "'>Mac</a>"
		return render.index(title, body)

class gallery:
	def GET(self, page=0):
		return render.index("Projects", render.gallery(db.select('projects')))


class static:
	def GET(self, media, file):
		try:
			f = open(media+'/'+file, 'r')
			return f.read()
		except:
			return '404' # you can send an 404 error here if you want


class index:
	def GET(self, args):
		title = ""
		body = ""

		body += str(session.get('projId', -1))
		title = "HELLO!"
		body += "PyRocket will be re-written in this soon!<br><br><a href='/upload'>Upload Python</a>"
		body += "<br><br><a href='/gallery'>See other awesome projects</a>"
		body += str(render.gallery(db.select('projects')))
		
		return render.index(title, body)

class login:
	def GET(self):
		session.logged_in = True
		raise web.seeother('/')

class logout:
	def GET(self):
		session.logged_in = False
		raise web.seeother('/')



if __name__ == "__main__":
	app.run()
