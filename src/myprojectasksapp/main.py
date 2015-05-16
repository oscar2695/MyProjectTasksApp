#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import os
from types import NoneType
import webapp2
import jinja2
from google.appengine.ext import ndb
from google.appengine.api import users
import time

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader( os.path.dirname( __file__ ) ),
    extensions=[ "jinja2.ext.autoescape" ],
    autoescape=True )

class Project(ndb.Model):
    name = ndb.StringProperty(required=True)
    duration = ndb.IntegerProperty()
    time = ndb.DateTimeProperty( auto_now_add =True)
    user = ndb.StringProperty()

class Task(ndb.Model):
    name = ndb.StringProperty(required=True)
    description = ndb.StringProperty()
    duration = ndb.IntegerProperty()
    time = ndb.DateTimeProperty( auto_now_add =True)
    project = ndb.StringProperty()

class LoginHandler(webapp2.RequestHandler):
    def post(self):
        user = users.get_current_user()
        if user:
            self.redirect("/main")
        else:
            self.redirect(users.create_login_url('/main'))

class LogoutHandler(webapp2.RequestHandler):
    def post(self):
        self.redirect(users.create_logout_url('/'))


class MainHandler(webapp2.RequestHandler):
    def __init__(self,request=None, response=None):
        self.initialize(request,response)
        self.username = ""
        self.password = ""
        self.answer = ""

        try:
            self.username = self.request.get("username")
            self.password = self.request.get("password")
        except:
            self.answer = "<html><body><b>ERROR</b> acquiring data</body></html>"

    def get(self):

        user = users.get_current_user()

        if user:
            projects = Project.query()
            projectsFinal=[]

            for project in projects:
                if project.user==user.nickname():
                    projectsFinal.append(project)


            template_values = {
                'user': user.nickname(),
                'projects': projectsFinal,
            }
            template = JINJA_ENVIRONMENT.get_template("main.html")
            self.response.write(template.render(template_values))
        else:
            answer = "<html><script>window.alert('Usuario no existe');window.location.href='/';</script></html>"
            self.response.write(answer)



class addProjectHandler(webapp2.RequestHandler):
    def __init__(self,request=None, response=None):
        self.initialize(request,response)
        self.nombre=""
        self.answer=""

        try:
            self.nombre = self.request.get("project")
        except:
            self.answer = "<html><body><b>ERROR</b> acquiring data</body></html>"


    def post(self):
        if (len(self.nombre)>0):
            user = users.get_current_user();
            clave = self.nombre+user.nickname();
            project = Project(id = clave,name=self.nombre, duration = 0, user = user.nickname())
            project.put()
            time.sleep(0.5)


        self.redirect("/main")


class delProjectHandler(webapp2.RequestHandler):
    def __init__(self,request=None, response=None):
        self.initialize(request,response)
        self.project = ""

        try:
            self.project = self.request.get("pro")
        except:
            self.answer = "<html><body><b>ERROR</b> acquiring data</body></html>"


    def post(self):
        user = users.get_current_user()
        borrar = self.project+user.nickname()

        tasks = Task.query(Task.project==borrar)
        task_keys = []
        for task in tasks:
            task_keys.append(task.key)

        ndb.delete_multi(task_keys)


        project_k = ndb.Key('Project', borrar)
        print(project_k)
        ndb.delete_multi([project_k])
        time.sleep(0.5)
        self.redirect("/main")
        """self.response.write(borrar)"""


class viewTasksHandler(webapp2.RequestHandler):
    def __init__(self,request=None, response=None):
        self.initialize(request,response)
        self.project=""
        self.answer = ""

        try:
            self.project = self.request.get("pro")
        except:
            self.answer = "<html><body><b>ERROR</b> acquiring data</body></html>"

    def post(self):
        tasks = Task.query(Task.project==self.project+users.get_current_user().nickname())
        template_values = {
            'user':users.get_current_user().nickname(),
            'project': self.project,
            'tasks': tasks,
        }
        template = JINJA_ENVIRONMENT.get_template("tasks.html")
        self.response.write(template.render(template_values))

    def get(self):
        tasks = Task.query(Task.project==self.project+users.get_current_user().nickname())
        template_values = {
            'user':users.get_current_user().nickname(),
            'project': self.project,
            'tasks': tasks,
        }
        template = JINJA_ENVIRONMENT.get_template("tasks.html")
        self.response.write(template.render(template_values))

class addTaskHandler(webapp2.RequestHandler):
    def __init__(self,request=None, response=None):
        self.initialize(request,response)
        self.nombre=""
        self.description=""
        self.duration=0
        self.project=""
        self.answer=""

        try:
            self.nombre = self.request.get("name")
            self.description = self.request.get("description")
            self.duration = int(self.request.get("duration"))
            self.project = self.request.get("pro")
        except:
            self.answer = "<html><body><b>ERROR</b> acquiring data</body></html>"


    def post(self):
        if (len(self.nombre)>0):
            user = users.get_current_user()
            project_k = ndb.Key('Project', self.project+user.nickname())
            projects = ndb.get_multi([project_k])
            project=projects[0]
            project.duration += self.duration
            project.put()

            clave = self.nombre + self.project +user.nickname()
            task = Task(id = clave,name=self.nombre,description=self.description, duration = self.duration, project = self.project+user.nickname())
            task.put()
            time.sleep(0.5)

        self.redirect("/viewtasks?pro="+self.project)

class delTaskHandler(webapp2.RequestHandler):
    def __init__(self,request=None, response=None):
        self.initialize(request,response)
        self.task = ""

        try:
            self.task = self.request.get("tsk")
            self.pro =self.request.get("pro")
        except:
            self.answer = "<html><body><b>ERROR</b> acquiring data</body></html>"


    def post(self):
        task_k = ndb.Key('Task', self.task+self.pro+users.get_current_user().nickname())
        tareas=ndb.get_multi([task_k])
        tarea = tareas[0]
        project=tarea.project

        project_k = ndb.Key('Project', project)
        projects = ndb.get_multi([project_k])
        project1=projects[0]
        project1.duration -= tarea.duration
        project1.put()



        ndb.delete_multi([task_k])
        time.sleep(0.5)

        self.redirect("/viewtasks?pro="+self.pro+"")


app = webapp2.WSGIApplication(
    [('/main', MainHandler),('/login', LoginHandler),('/logout',LogoutHandler),('/addproject',addProjectHandler),('/delproject',delProjectHandler),('/viewtasks',viewTasksHandler),('/addtask',addTaskHandler),('/deltask',delTaskHandler)],
    debug=True)
