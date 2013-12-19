import webapp2

from google.appengine.api import users
import os
import jinja2

JINJA = jinja2.Environment(autoescape=True,
                           loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), 'templates')))


class Dashboard(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            template_values = {
                'loggedIn': True,
                'logout_url': users.create_logout_url('/'),
                'name': user.nickname(),
                'email': user.email()
            }
        else:
            template_values = {
                'loggedIn': False,
                'login_url': users.create_login_url("/")
            }
        template = JINJA.get_template('dashboard.html')
        self.response.out.write(template.render(template_values))


class Dashboard(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            self.redirect('/dashboard')
            return
        else:
            self.response.write()
            template_values = {
                'login_url': users.create_login_url('/dashboard')
            }
            template = JINJA.get_template('index.html')
            self.response.out.write(template.render(template_values))

app = webapp2.WSGIApplication([
                                  ('/', Dashboard),
                              ], debug=True)