
import cherrypy
from mako.template import Template
import json
import pickle
import passthing
from passthing.PassDatabase import InvalidPassword
from cryptography.fernet import InvalidToken


class PassThingWeb(object):

    @cherrypy.expose
    def get_entry(self, entry_name, master_password):
        result = {
            "status": "success"
        }
        try:
            database_filename = cherrypy.request.app.config['passthing']['database.filename']
            database = passthing.PassDatabase(database_filename)
            username, password = database.get_entry(entry_name, master_password)
            result["username"] = username
            result["password"] = str(password, "utf-8")
        except InvalidPassword:
            result["status"] = "invalid_password"
        return json.dumps(result)

    @cherrypy.expose
    def index(self):
        database_filename = cherrypy.request.app.config['passthing']['database.filename']
        database = passthing.PassDatabase(database_filename)
        return Template(filename='index.html').render(entry_names=sorted(database.get_entry_names()))

cherrypy.quickstart(PassThingWeb(), '/', "passthing.conf")
