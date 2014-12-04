import web, random, json, os, subprocess, credentials


import boto
from boto.s3.key import Key

# This is my second key for the PyRocket buckets
access_key = credentials.access_key
secret_key = credentials.secret_key


render = web.template.render('templates/')

web.config.debug = True

        
urls = (
    '/word', 'word',
    '/upload', 'upload',
    '/gallery', 'gallery',
    '/finalize', 'finalize',
    '/project/(.*)', 'project',
    '/static/(.*)', 'static',
    '/(.*)', 'index'
)
app = web.application(urls, globals())


db = web.database(dbn='mysql', db=credentials.mysql_database, user=credentials.mysql_username, pw=credentials.mysql_password)
store = web.session.DBStore(db, 'sessions')
session = web.session.Session(app, store, initializer={'projId': 0})



def createWord():
    vowels = ['a','e','i','o','u']
    consonants = ['b','c','d','f','g','h','j','k','l','m','n','p','q','r','s','t','v','w','x','y','z']
    a = random.sample(consonants,2)
    a.insert(1,random.choice(vowels))
    a.append(random.choice(vowels))
    
    return "".join(a)

def uploadFile(fileName, contents, perms="private"):
    bucket_name = 'pyrocketprojects'
    conn = boto.connect_s3(
        aws_access_key_id = access_key,
        aws_secret_access_key = secret_key,
        host = 'objects.dreamhost.com',
    )

    bucket = conn.get_bucket(bucket_name)
    key = bucket.new_key(fileName)
    key.set_contents_from_string(contents)
    key.set_acl(perms)

class upload:
    def GET(self):
        return render.index("upload", render.uploadForm())

    def POST(self):
        if session["projId"] == 0:
            with db.transaction():
                projId = db.insert('projects')
                session.projId = projId
        session.projectID = db.select

        x = web.input(file={})

        folder = 'projects/project-' + str(session.projId) + '/'
        fileName = folder + 'src/' + x['file'].filename

        mkdir(folder)
        mkdir(folder + 'src/')
        mkdir(folder + 'mac/')

        uploadFile(fileName, x['file'].value)


        file = open(fileName, "w")
        file.write(x['file'].value)
        file.close()



        result = x['file'].filename
        return result

        """
        x['myfile'].value[0:10]

        
        web.debug(x['myfile'].filename) # This is the filename
        web.debug(x['myfile'].value) # This is the file contents
        web.debug(x['myfile'].file.read()) # Or use a file(-like) object
        raise web.seeother('/upload')"""


class finalize:
    def POST(self):
        folder = 'projects/project-' + str(session.projId) + '/'
        fileName = folder + 'src/' + "main.py"

        subprocess.call(["sh", "Py2App.sh", folder+"src/", "main.py"])

        zipLocation = folder + "mac/app.zip"

        with open(zipLocation, mode='rb') as file: # b is important -> binary
            zipContent = file.read()
            file.close()

        uploadFile(folder + "mac/app.zip", zipContent, perms="public-read")
        raise web.seeother("/finalize")


        return "This will convert the uploaded files to an application..."
    def GET(self):
        url = "https://pyrocketprojects.objects.dreamhost.com/projects/project-"+str(projId)+"/mac/app.zip"
        title = "HELLO!"
        body = "Your project can be downloaded here:<br>"
        body += "<a href='" + url + "'>Mac</a>"
        return render.index(title, body)

class gallery:
    def GET(self):
        title = "Projects"
        projects = db.select('projects')
        return render.index(title, render.gallery(projects))



class static:
    def GET(self, media, file):
        try:
            f = open(media+'/'+file, 'r')
            return f.read()
        except:
            return '404' # you can send an 404 error here if you want


class word:
    def GET(self):
        return createWord()

class index:
    def GET(self, args):
        title = "HELLO!"
        body = "PyRocket will be re-written in this soon!<br><br><a href='/upload'>Upload Python</a>"
        body += "<br><br><a href='/gallery'>See other awesome projects</a>"
        
        return render.index(title, body)

if __name__ == "__main__":
    app.run()


def mkdir(path):
    try:
        os.mkdir(path)
    except OSError, e:
        pass