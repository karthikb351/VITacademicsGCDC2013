import webapp2

from google.appengine.api import users
from google.appengine.ext import db
import os
import jinja2
import re

JINJA = jinja2.Environment(autoescape=True,
                           loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), 'templates')))


class UserModel(db.Model):
    linkedRegno = db.BooleanProperty(default=False)
    regno = db.StringProperty()
    email = db.UserProperty()
    editedOn = db.DateTimeProperty(auto_now=True)
    createdOn = db.DateTimeProperty(auto_now_add=True)


class Dashboard(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            if re.search("\**@vit\.ac\.in", user.email()):
                customUser = UserModel.get_by_key_name(key_names=user.email())
                if customUser:
                    if customUser.linkedRegno:
                        template_values = {
                            'loggedIn': True,
                            'logout_url': users.create_logout_url('/'),
                            'name': user.nickname(),
                            'email': user.email()
                        }
                        template = JINJA.get_template('dashboard.html')
                        self.response.out.write(template.render(template_values))
                    else:
                        self.redirect('/')
                else:
                    self.redirect('/')
            else:
                self.redirect('/')
        else:
            self.redirect('/')


class LinkRegnoForm(webapp2.RedirectHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            if re.search("\**@vit\.ac\.in", user.email()):
                customUser = UserModel.get_by_key_name(key_names=user.email())
                if customUser:
                    if customUser.linkedRegno:
                        self.redirect('/dashboard')
                    else:
                        template_values = {
                            'logout_url': users.create_logout_url('/'),
                            'name': user.nickname(),
                            'email': user.email(),
                            'message': 'Please enter you regno and dob to continue',
                            'form_url': '/'
                        }
                        template = JINJA.get_template('link_regno_form.html')
                        self.response.out.write(template.render(template_values))
                else:
                    self.redirect('/')
            else:
                self.redirect('/')
        else:
            self.redirect('/')


class LinkRegnoSubmit(webapp2.RedirectHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            if re.search("\**@vit\.ac\.in", user.email()):
                customUser = UserModel.get_by_key_name(key_names=user.email())
                if customUser:
                    customUser.linkedRegno=True
                    customUser.put()
                    self.redirect('/dashboard')
                else:
                    self.redirect('/')
            else:
                self.redirect('/')
        else:
            self.redirect('/')

class Index(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            if re.search("\**@vit\.ac\.in", user.email()):
                customUser = UserModel.get_by_key_name(key_names=user.email())
                if customUser:
                    if customUser.linkedRegno:
                        self.redirect('/dashboard')
                    else:
                        self.redirect('/linkregnoform')
                else:
                    customUser=UserModel(key_name=user.email())
                    customUser.put()
                    self.redirect('/linkregnoform')
            else:
                template_values = {
                    'error': True,
                    'message': "Please sign in with you VIT email ID. Not "+user.email(),
                    'logout_url': users.create_logout_url('/')
                }
                template = JINJA.get_template('index.html')
                self.response.out.write(template.render(template_values))
        else:
            template_values = {
                'error': False,
                'message': "You aren't logged in",
                'login_url': users.create_login_url('/')
            }
            template = JINJA.get_template('index.html')
            self.response.out.write(template.render(template_values))

app = webapp2.WSGIApplication([
                                  ('/', Index),
                                  ('/linkregnoform',LinkRegnoForm),
                                  ('/linkregnosubmit',LinkRegnoSubmit),
                                  ('/dashboard',Dashboard)
                              ], debug=True)