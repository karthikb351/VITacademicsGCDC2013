# -*- coding: utf-8 -*-
import cgi
import logging
import re
import urllib
import urllib2
import datetime

import webapp2
import json
from webapp2_extras import auth, sessions, jinja2
from jinja2.runtime import TemplateNotFound
from google.appengine.ext import db
from google.appengine.api import memcache

import secrets
from simpleauth import SimpleAuthHandler


subjects = json.loads(
    '''[{"sl_no":"1","slot":"D1","code":"CSE303","title":"Computer Networks","classnbr":"2622","extra":"","regdate":"27/06/2013 09:01:02","conducted":"44","attended":"37","details":["11-Jul-2013","Absent","12-Jul-2013","Absent","16-Jul-2013","Present","18-Jul-2013","Present","19-Jul-2013","Present","23-Jul-2013","Present","25-Jul-2013","Present","26-Jul-2013","Present","30-Jul-2013","Present","01-Aug-2013","Present","02-Aug-2013","Present","06-Aug-2013","Present","08-Aug-2013","Present","13-Aug-2013","Present","16-Aug-2013","Present","20-Aug-2013","Present","22-Aug-2013","Absent","23-Aug-2013","Present","03-Sep-2013","Absent","05-Sep-2013","Present","06-Sep-2013","Absent","10-Sep-2013","Present","12-Sep-2013","Absent","13-Sep-2013","Present","17-Sep-2013","Present","19-Sep-2013","Absent","20-Sep-2013","Present","24-Sep-2013","Present","26-Sep-2013","Present","01-Oct-2013","Present","03-Oct-2013","Present","04-Oct-2013","Present","15-Oct-2013","Present","17-Oct-2013","Present","18-Oct-2013","Present","22-Oct-2013","Present","24-Oct-2013","Present","25-Oct-2013","Present","29-Oct-2013","Present","07-Nov-2013","On Duty","08-Nov-2013","On Duty","12-Nov-2013","Present","14-Nov-2013","Present","15-Nov-2013","Present"],"percentage":"85%","type":"Theory Only","marks":{"CAT 1":"41.00","CAT 2":"41.00","Quiz 1":"3.00","Quiz 2":"3.75","Quiz 3":"4.50","Assignment":"4.25","Finals":"83.00"},"timetable":{"Tuesday":"10:00-11:00","Thursday":"08:00-09:00","Friday":"11:00-12:00"}},{"sl_no":"2","slot":"L25+L26+L27","code":"CSE304","title":"Computer Networks Lab","classnbr":"2644","extra":"","regdate":"27/06/2013 09:02:08","conducted":"42","attended":"33","details":["12-Jul-2013","Absent","19-Jul-2013","Present","26-Jul-2013","Present","02-Aug-2013","Present","16-Aug-2013","Present","23-Aug-2013","Present","06-Sep-2013","Absent","13-Sep-2013","Present","20-Sep-2013","Present","04-Oct-2013","Absent","18-Oct-2013","Present","25-Oct-2013","Present","08-Nov-2013","Present","15-Nov-2013","Present"],"percentage":"79%","type":"Lab Only","marks":{"Internals":"48.00","Finals":"46.00"},"timetable":{"Friday":"08:00-11:00"}},{"sl_no":"3","slot":"F1","code":"CSE305","title":"Embedded Systems","classnbr":"2768","extra":"","regdate":"15/07/2013 21:53:31","conducted":"41","attended":"30","details":["17-Jul-2013","Present","18-Jul-2013","Present","22-Jul-2013","Absent","24-Jul-2013","Present","25-Jul-2013","Present","29-Jul-2013","Present","31-Jul-2013","Present","01-Aug-2013","Present","05-Aug-2013","Absent","07-Aug-2013","Present","08-Aug-2013","Present","12-Aug-2013","Absent","14-Aug-2013","Present","19-Aug-2013","Absent","21-Aug-2013","Present","22-Aug-2013","Present","02-Sep-2013","Absent","04-Sep-2013","Absent","05-Sep-2013","Absent","11-Sep-2013","Present","12-Sep-2013","Present","16-Sep-2013","Present","18-Sep-2013","Present","19-Sep-2013","Present","23-Sep-2013","Absent","25-Sep-2013","Absent","26-Sep-2013","Present","30-Sep-2013","Present","03-Oct-2013","Present","14-Oct-2013","Present","17-Oct-2013","Present","21-Oct-2013","Present","23-Oct-2013","Present","24-Oct-2013","Present","28-Oct-2013","Present","30-Oct-2013","Absent","06-Nov-2013","Absent","07-Nov-2013","On Duty","11-Nov-2013","Present","13-Nov-2013","Present","14-Nov-2013","Present"],"percentage":"74%","type":"Theory Only","marks":{"CAT 1":"50.00","CAT 2":"48.33","Quiz 1":"4.50","Quiz 2":"4.50","Quiz 3":"4.50","Assignment":"4.50","Finals":"83.00"},"timetable":{"Monday":"09:00-10:00","Wednesday":"09:00-10:00","Thursday":"10:00-11:00"}},{"sl_no":"4","slot":"L10+L11+L12","code":"CSE306","title":"Embedded Systems Lab","classnbr":"2780","extra":"","regdate":"27/06/2013 09:35:04","conducted":"45","attended":"36","details":["16-Jul-2013","Present","23-Jul-2013","Present","30-Jul-2013","Absent","06-Aug-2013","Present","13-Aug-2013","Present","20-Aug-2013","Present","03-Sep-2013","Present","10-Sep-2013","Present","17-Sep-2013","Present","24-Sep-2013","Absent","01-Oct-2013","Present","15-Oct-2013","Present","22-Oct-2013","Present","29-Oct-2013","Absent","12-Nov-2013","Present"],"percentage":"80%","type":"Lab Only","marks":{"Internals":"49.00","Finals":"49.00"},"timetable":{"Tuesday":"11:00-13:00"}},{"sl_no":"5","slot":"C2","code":"CSE310","title":"Software Engineering","classnbr":"4368","extra":"","regdate":"27/06/2013 09:00:41","conducted":"43","attended":"27","details":["11-Jul-2013","Present","15-Jul-2013","Present","17-Jul-2013","Present","18-Jul-2013","Present","22-Jul-2013","Present","24-Jul-2013","Present","25-Jul-2013","Present","29-Jul-2013","Present","31-Jul-2013","Present","01-Aug-2013","Present","05-Aug-2013","Present","07-Aug-2013","Present","08-Aug-2013","Present","12-Aug-2013","Present","14-Aug-2013","Present","19-Aug-2013","Present","21-Aug-2013","Present","22-Aug-2013","Absent","02-Sep-2013","Present","04-Sep-2013","Absent","05-Sep-2013","Present","11-Sep-2013","Present","12-Sep-2013","Present","16-Sep-2013","Present","18-Sep-2013","Absent","19-Sep-2013","Absent","23-Sep-2013","Absent","25-Sep-2013","Absent","26-Sep-2013","Present","30-Sep-2013","Absent","03-Oct-2013","Absent","14-Oct-2013","Absent","17-Oct-2013","Absent","21-Oct-2013","Present","23-Oct-2013","Absent","24-Oct-2013","Present","28-Oct-2013","Absent","30-Oct-2013","Absent","06-Nov-2013","Absent","07-Nov-2013","On Duty","11-Nov-2013","Present","13-Nov-2013","Absent","14-Nov-2013","Absent"],"percentage":"63%","type":"Theory Only","marks":{"CAT 1":"33.00","CAT 2":"36.00","Quiz 1":"4.00","Quiz 2":"2.50","Quiz 3":"3.50","Assignment":"4.50","Finals":"78.00"},"timetable":{"Monday":"16:00-17:00","Wednesday":"14:00-15:00","Thursday":"17:00-18:00"}},{"sl_no":"6","slot":"L4+L5+L6","code":"CSE311","title":"Software Engineering Lab","classnbr":"4370","extra":"","regdate":"27/06/2013 09:00:50","conducted":"42","attended":"33","details":["15-Jul-2013","Present","22-Jul-2013","Present","29-Jul-2013","Present","05-Aug-2013","Present","12-Aug-2013","Present","19-Aug-2013","Absent","02-Sep-2013","Present","16-Sep-2013","Present","23-Sep-2013","Absent","30-Sep-2013","Present","14-Oct-2013","Absent","21-Oct-2013","Present","28-Oct-2013","Present","11-Nov-2013","Present"],"percentage":"79%","type":"Lab Only","marks":{"Internals":"44.00","Finals":"48.00"},"timetable":{"Monday":"11:00-13:00"}},{"sl_no":"7","slot":"G2+TG2","code":"CSE319","title":"Soft Computing","classnbr":"2629","extra":"","regdate":"15/07/2013 11:03:03","conducted":"42","attended":"29","details":["12-Jul-2013","Absent","16-Jul-2013","Absent","17-Jul-2013","Present","19-Jul-2013","Present","23-Jul-2013","Present","24-Jul-2013","Present","26-Jul-2013","Present","30-Jul-2013","Present","31-Jul-2013","Present","02-Aug-2013","Absent","06-Aug-2013","Present","07-Aug-2013","Present","13-Aug-2013","Present","14-Aug-2013","Present","16-Aug-2013","Present","20-Aug-2013","Present","21-Aug-2013","Present","23-Aug-2013","Absent","03-Sep-2013","Present","04-Sep-2013","Present","06-Sep-2013","Absent","10-Sep-2013","Present","11-Sep-2013","Present","13-Sep-2013","Present","17-Sep-2013","Present","18-Sep-2013","Present","20-Sep-2013","Absent","24-Sep-2013","Present","25-Sep-2013","Present","01-Oct-2013","Absent","04-Oct-2013","Absent","15-Oct-2013","Present","18-Oct-2013","Absent","22-Oct-2013","Present","23-Oct-2013","Absent","25-Oct-2013","Absent","29-Oct-2013","Absent","30-Oct-2013","Absent","06-Nov-2013","Absent","08-Nov-2013","On Duty","12-Nov-2013","Present","13-Nov-2013","Present","15-Nov-2013","Present"],"percentage":"70%","type":"Theory Only","marks":{"CAT 1":"40.00","CAT 2":"38.50","Quiz 1":"3.00","Quiz 2":"5.00","Quiz 3":"5.00","Assignment":"4.00","Finals":"88.00"},"timetable":{"Tuesday":"15:00-16:00","Wednesday":"18:00-19:00","Friday":"16:00-17:00"}},{"sl_no":"8","slot":"F2","code":"CSE408","title":"Data Warehousing and Data Mining","classnbr":"2613","extra":"","regdate":"15/07/2013 17:32:09","conducted":"41","attended":"26","details":["11-Jul-2013","Absent","15-Jul-2013","Absent","17-Jul-2013","Present","18-Jul-2013","Present","22-Jul-2013","Present","24-Jul-2013","Present","25-Jul-2013","Present","29-Jul-2013","Present","31-Jul-2013","Present","01-Aug-2013","Absent","05-Aug-2013","Present","07-Aug-2013","Present","08-Aug-2013","Present","12-Aug-2013","Present","14-Aug-2013","Present","19-Aug-2013","Present","21-Aug-2013","Present","22-Aug-2013","Absent","02-Sep-2013","Present","04-Sep-2013","Absent","05-Sep-2013","Absent","11-Sep-2013","Present","12-Sep-2013","Present","16-Sep-2013","Present","18-Sep-2013","Absent","19-Sep-2013","Absent","23-Sep-2013","Present","25-Sep-2013","Absent","26-Sep-2013","Present","30-Sep-2013","Present","03-Oct-2013","Absent","14-Oct-2013","Absent","17-Oct-2013","Present","21-Oct-2013","Present","23-Oct-2013","Absent","24-Oct-2013","Absent","28-Oct-2013","Absent","30-Oct-2013","Absent","06-Nov-2013","Absent","07-Nov-2013","On Duty","11-Nov-2013","Present","13-Nov-2013","Present","14-Nov-2013","Absent"],"percentage":"64%","type":"Theory Only","marks":{"CAT 1":"35.50","CAT 2":"44.50","Quiz 1":"3.25","Quiz 2":"3.00","Quiz 3":"5.00","Assignment":"5.00","Finals":"86.00"},"timetable":{"Monday":"15:00-16:00","Wednesday":"15:00-16:00","Thursday":"16:00-17:00"}},{"sl_no":"9","slot":"C1","code":"CSE413","title":"Computer Graphics","classnbr":"2596","extra":"","regdate":"27/06/2013 08:59:50","conducted":"43","attended":"29","details":["11-Jul-2013","Present","15-Jul-2013","Present","17-Jul-2013","Present","18-Jul-2013","Present","22-Jul-2013","Present","24-Jul-2013","Present","25-Jul-2013","Present","29-Jul-2013","Present","31-Jul-2013","Absent","01-Aug-2013","Present","05-Aug-2013","Absent","07-Aug-2013","Present","08-Aug-2013","Present","12-Aug-2013","Present","14-Aug-2013","Present","19-Aug-2013","Present","21-Aug-2013","Present","22-Aug-2013","Present","02-Sep-2013","Present","04-Sep-2013","Absent","05-Sep-2013","Absent","11-Sep-2013","Absent","12-Sep-2013","Present","16-Sep-2013","Present","18-Sep-2013","Present","19-Sep-2013","Present","23-Sep-2013","Absent","25-Sep-2013","Present","26-Sep-2013","Absent","30-Sep-2013","Absent","03-Oct-2013","Absent","14-Oct-2013","Present","17-Oct-2013","Absent","21-Oct-2013","Present","23-Oct-2013","Absent","24-Oct-2013","Present","28-Oct-2013","Absent","30-Oct-2013","Present","06-Nov-2013","Absent","07-Nov-2013","On Duty","11-Nov-2013","Present","13-Nov-2013","Absent","14-Nov-2013","Present"],"percentage":"68%","type":"Theory Only","marks":{"CAT 1":"40.00","CAT 2":"31.00","Quiz 1":"2.50","Quiz 2":"3.50","Quiz 3":"3.00","Assignment":"3.00","Term End":"87.00"},"timetable":{"Monday":"10:00-11:00","Wednesday":"08:00-09:00","Thursday":"11:00-12:00"}}]''')
tthelper = json.loads('''["08:00-09:00",
"09:00-10:00",
"10:00-11:00",
"11:00-12:00",
"12:00-13:00",
"13:00-14:00",
"14:00-15:00",
"15:00-16:00",
"16:00-17:00",
"17:00-18:00",
"18:00-19:00"]''')
days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]


class Notice(db.Model):
    cnum = db.StringProperty()
    text = db.TextProperty()
    author = db.StringProperty()
    timestamp = db.DateTimeProperty(auto_now=True, auto_now_add=True)


class BaseRequestHandler(webapp2.RequestHandler):
    def dispatch(self):
        # Get a session store for this request.
        self.session_store = sessions.get_store(request=self.request)

        try:
            # Dispatch the request.
            webapp2.RequestHandler.dispatch(self)
        finally:
            # Save all sessions.
            self.session_store.save_sessions(self.response)

    @webapp2.cached_property
    def jinja2(self):
        """Returns a Jinja2 renderer cached in the app registry"""
        return jinja2.get_jinja2(app=self.app)

    @webapp2.cached_property
    def session(self):
        """Returns a session using the default cookie key"""
        return self.session_store.get_session()

    @webapp2.cached_property
    def auth(self):
        return auth.get_auth()

    @webapp2.cached_property
    def current_user(self):
        """Returns currently logged in user"""
        user_dict = self.auth.get_user_by_session()
        return self.auth.store.user_model.get_by_id(user_dict['user_id'])

    @webapp2.cached_property
    def logged_in(self):
        """Returns true if a user is currently logged in, false otherwise"""
        return self.auth.get_user_by_session() is not None


    def render(self, template_name, template_vars={}):
        # Preset values for the template
        values = {
            'allsubjects': subjects,
            'url_for': self.uri_for,
            'logged_in': self.logged_in,
            'flashes': self.session.get_flashes()
        }

        # Add manually supplied template values
        values.update(template_vars)

        # read the template or 404.html
        try:
            self.response.write(self.jinja2.render_template(template_name, **values))
        except TemplateNotFound:
            self.abort(404)

    def head(self, *args):
        """Head is used by Twitter. If not there the tweet button shows 0"""
        pass


class AuthHandler(BaseRequestHandler, SimpleAuthHandler):
    """Authentication handler for OAuth 2.0, 1.0(a) and OpenID."""

    # Enable optional OAuth 2.0 CSRF guard
    OAUTH2_CSRF_STATE = True

    USER_ATTRS = {
        'facebook': {
            'id': lambda id: ('avatar_url',
                              'http://graph.facebook.com/{0}/picture?type=large'.format(id)),
            'name': 'name',
            'link': 'link'
        },
        'google': {
            'picture': 'avatar_url',
            'name': 'name',
            'profile': 'link',
        },
        'windows_live': {
            'avatar_url': 'avatar_url',
            'name': 'name',
            'link': 'link'
        },
        'twitter': {
            'profile_image_url': 'avatar_url',
            'screen_name': 'name',
            'link': 'link'
        },
        'linkedin': {
            'picture-url': 'avatar_url',
            'first-name': 'name',
            'public-profile-url': 'link'
        },
        'linkedin2': {
            'picture-url': 'avatar_url',
            'first-name': 'name',
            'public-profile-url': 'link'
        },
        'foursquare': {
            'photo': lambda photo: ('avatar_url', photo.get('prefix') + '100x100' + photo.get('suffix')),
            'firstName': 'firstName',
            'lastName': 'lastName',
            'contact': lambda contact: ('email', contact.get('email')),
            'id': lambda id: ('link', 'http://foursquare.com/user/{0}'.format(id))
        },
        'openid': {
            'id': lambda id: ('avatar_url', '/img/missing-avatar.png'),
            'nickname': 'name',
            'email': 'link'
        }
    }

    def _on_signin(self, data, auth_info, provider):
        """Callback whenever a new or existing user is logging in.
     data is a user info dictionary.
     auth_info contains access token or oauth token and secret.
    """
        auth_id = '%s:%s' % (provider, data['id'])
        logging.info('Looking for a user with id %s', auth_id)
        user = self.auth.store.user_model.get_by_auth_id(auth_id)
        _attrs = self._to_user_model_attrs(data, self.USER_ATTRS[provider])
        _attrs.update({
            'email': data['email'],
            'valid': False,
            'verified': False,
            'registration_number': None,
        })
        if re.search("\**@vit\.ac\.in", data['email']):
            _attrs.update({
                'valid': True
            })
        if re.search("[0-9]{2}[A-Z|a-z]{3}[0-9]{3,4}", data['family_name']):
            _attrs.update({
                'registration_number': data['family_name']
            })
        _attrs.update({'firsttime': True});
        if user:
            logging.info('Found existing user to log in')
            # Existing users might've changed their profile data so we update our
            # local model anyway. This might result in quite inefficient usage
            # of the Datastore, but we do this anyway for demo purposes.
            #
            # In a real app you could compare _attrs with user's properties fetched
            # from the datastore and update local user in case something's changed.
            user.populate(**_attrs)
            user.put()
            self.auth.set_session(
                self.auth.store.user_to_dict(user))

        else:
            # check whether there's a user currently logged in
            # then, create a new user if nobody's signed in,
            # otherwise add this auth_id to currently logged in user.

            if self.logged_in:
                logging.info('Updating currently logged in user')
                u = self.current_user
                u.populate(**_attrs)
                # The following will also do u.put(). Though, in a real app
                # you might want to check the result, which is
                # (boolean, info) tuple where boolean == True indicates success
                # See webapp2_extras.appengine.auth.models.User for details.
                u.add_auth_id(auth_id)

            else:
                logging.info('Creating a brand new user')
                ok, user = self.auth.store.user_model.create_user(auth_id, **_attrs)
                if ok:
                    self.auth.set_session(self.auth.store.user_to_dict(user))

        # Remember auth data during redirect, just for this demo. You wouldn't
        # normally do this.
        self.session.add_flash(data, 'data - from _on_signin(...)')
        self.session.add_flash(auth_info, 'auth_info - from _on_signin(...)')

        # Go to the profile page
        self.redirect('/dashboard')

    def logout(self):
        self.auth.unset_session()
        self.redirect('/')

    def handle_exception(self, exception, debug):
        logging.error(exception)
        self.render('error.html', {'exception': exception})

    def _callback_uri_for(self, provider):
        return self.uri_for('auth_callback', provider=provider, _full=True)

    def _get_consumer_info_for(self, provider):
        """Returns a tuple (key, secret) for auth init requests."""
        return secrets.AUTH_CONFIG[provider]

    def _to_user_model_attrs(self, data, attrs_map):
        """Get the needed information from the provider dataset."""
        user_attrs = {}
        for k, v in attrs_map.iteritems():
            attr = (v, data.get(k)) if isinstance(v, str) else v(data.get(k))
            user_attrs.setdefault(*attr)

        return user_attrs


class RootHandler(BaseRequestHandler):
    def get(self):
        """Handles default landing page"""
        error = self.request.get('error')
        values = {
            'error': error,
            'disclaimerpage': True,
        }
        if self.logged_in:
            user=self.current_user
            values.update({
                'user': user,
                'session': self.auth.get_user_by_session(),
                'data': user.to_dict()})
        self.render('home.html', values)


class SubjectHandler(BaseRequestHandler):
    def get(self, classnbr):
        """Handles GET /subject/<classnbr>"""
        if self.logged_in:
            user = self.current_user
            values = {
                'user': user,
                'session': self.auth.get_user_by_session(),
                'data': user.to_dict()
            }
            subject = {}
            for sub in subjects:
                if sub['classnbr'] == str(classnbr):
                    subject = sub
                #if subject is None, fail
            notices=[]
            nots = Notice.all()
            for nt in nots:
                if nt.cnum==classnbr:
                    notices.append(nt)
            nsjson = [] #Stores the JSONArray of all relavant notices for the given class
            for notice in notices:
                njson = {"cnum": notice.cnum, "text": notice.text, "author": notice.author, "id": notice.key().id(),
                         "timestamp": (notice.timestamp+datetime.timedelta(0,19800)).strftime("%H:%M on %Y-%m-%d")} #Temporarily stores every notice's JSON
                nsjson.append(njson)
            values.update({
                'classnbr': subject['classnbr'],
                'subject': subject,
                'notices': nsjson
            })
            self.render('subject.html', values)
        else:
            self.redirect('/')

class NoticeDeleteHandler(BaseRequestHandler):
    def get(self, noticeid, classnbr):
        notice = Notice.get_by_id(int(noticeid))
        notice.delete()
        self.redirect('/subject/'+classnbr)

class NoticeHandler(BaseRequestHandler):
    def post(self):
        cnum = self.request.get("cnum")
        text = self.request.get("text")
        author = self.request.get("author")
        Notice(cnum=cnum, text=text, author=author).put()
        self.redirect('/subject/'+cnum)

class TimetableHandler(BaseRequestHandler):
    def get(self):
        """Handles GET /timetable"""
        if self.logged_in:
            user = self.current_user
            values = {
                'user': user,
                'session': self.auth.get_user_by_session(),
                'data': user.to_dict()
            }
            timetable = []
            flag = True
            for i in range(0, 5):
                ttrow = [days[i]]
                for tt in tthelper:
                    flag = False
                    for sub in subjects:
                        if days[i] in sub['timetable'].keys():
                            if tt in sub['timetable'][days[i]]:
                                flag = True
                                ttrow.append(sub)
                    if flag == False:
                        ttrow.append(None)
                timetable.append(ttrow)
            timetable[4][1] = timetable[4][2] = timetable[4][3] = subjects[1]
            timetable[0][4] = timetable[0][5] = timetable[0][6] = subjects[5]
            timetable[1][4] = timetable[1][5] = timetable[1][6] = subjects[3]
            values.update({
                'timetable': timetable
            })
            self.render('timetable.html', values)
        else:
            self.redirect('/')

class SMSHandler(BaseRequestHandler):
    def get(self):
        """Handles /sms page"""
        if self.logged_in:
            user=self.current_user
            error = self.request.get('error')
            values = {
                'error': error,
                'user': user,
                'session': self.auth.get_user_by_session(),
                'data': user.to_dict()
            }
            self.render('smsusage.html', values)
        else:
            self.redirect('/')

class DashboardHandler(BaseRequestHandler):
    def get(self):
        """Handles GET /dashboard"""
        if self.logged_in:
            user = self.current_user
            values = {
                'user': user,
                'session': self.auth.get_user_by_session(),
                'data': user.to_dict()
            }
            if user.firsttime:
                self.redirect('/disclaimer')
                return
            else:
                values.update({
                    'subjects': subjects
                })
                self.render('overview.html', values)
        else:
            self.redirect('/')


class DisclaimerHandler(BaseRequestHandler):
    def get(self):
        """Handles GET /disclaimer"""
        if self.logged_in:
            user = self.current_user
            user.firsttime = False
            user.put()
            values = {
                'user': user,
                'session': self.auth.get_user_by_session(),
                'data': user.to_dict(),
                'disclaimerpage': True
            }
            self.render('disclaimer.html', values)
        else:
            self.redirect('/')


class BackendHandler(BaseRequestHandler):
    def get(self):
        """Handles /backend page"""
        if self.logged_in:
            user=self.current_user
            error = self.request.get('error')
            values = {
                'user': user,
                'session': self.auth.get_user_by_session(),
                'data': user.to_dict(),
                'error': error,
                'disclaimerpage': True
            }
            self.render('backend.html', values)


class txtWebHandler(BaseRequestHandler):
    def get(self):
        message = cgi.escape(self.request.get('txtweb-message')) #get hold of txtweb-message here
        mobilehash = cgi.escape(self.request.get('txtweb-mobile'))
        if mobilehash != None:
            memcache.set("hash", mobilehash)
        logging.info(mobilehash)
        error = False
        reply = ""
        temp1=None
        if message == "attendance":
            for sub in subjects:
                reply=reply+sub['title']+" - "+sub['percentage']+"<br>"
        elif message == "courses":
            reply="<b>Course Title: Course Number</b> <br>"
            for sub in subjects:
                reply=reply+sub['title']+":"+sub['classnbr']+"</br>"
        elif message[0:message.find(' ')] == "course":
            for sub in subjects:
                if sub['classnbr']==message[message.find(' ') + 1:]:
                    temp=sub
            if temp == None:
                error=True
            else:
                reply=temp['title']\
                      +"<br>Attended:"+temp['attended']+"/"+temp['conducted']\
                      +"<br>Percentage:"+temp['percentage']
                for k, v in temp['marks'].items():
                    reply=reply+"<br>"+k+"-"+v
        elif message[0:message.find(' ')] == "notices":
            for sub in subjects:
                if sub['classnbr']==message[message.find(' ') + 1:]:
                    temp=sub
            if temp == None:
                error=True
            else:
                reply=sub['title']+"<br>"
                notices=[]
                nots = Notice.all()
                for nt in nots:
                    if nt.cnum==message[message.find(' ') + 1:]:
                        notices.append(nt)
                nsjson = [] #Stores the JSONArray of all relavant notices for the given class
                for notice in notices:
                    reply=reply+"Title - "+notice.text+"<br> Posted at "+(notice.timestamp+datetime.timedelta(0,19800)).strftime("%H:%M %Y-%m-%d")+" by "+notice.author+"<br>"
        elif message == "help":
            reply="<b>List of commands</b><br>Attendance Overview - @vitacademics attendance <br>Courses List - @vitacademics courses <br>Course Details - @vitacademics course [course-number] <br>Notices - @vitacademics notices [course-number] <br>Help - @vitacademics help"
        else:
            reply="<b>List of commands</b><br>Attendance Overview - @vitacademics attendance <br>Courses List - @vitacademics courses <br>Course Details - @vitacademics course [course-number] <br>Notices - @vitacademics notices [course-number] <br>Help - @vitacademics help"
        if error:
            reply="<b>List of commands</b><br>Attendance Overview - @vitacademics attendance <br>Courses List - @vitacademics courses <br>Course Details - @vitacademics course [course-number] <br>Notices - @vitacademics notices [course-number] <br>Help - @vitacademics help"

        self.response.out.write(
                """<html><head><meta name="txtweb-appkey" content="f137b995-5146-4c2e-b8d4-5df474f39316" /></head><body>""" + reply + """<br/></body></html>""")


class txtWebDispatchHandler(BaseRequestHandler):
    def get(self):
        mobilehash = memcache.get("hash")
        if mobilehash != None:
            data = """<html><head><meta name="txtweb-appkey" content="f137b995-5146-4c2e-b8d4-5df474f39316" /></head><body><p>Sent from server. yay!:D</p></body></html>""";
            args = {
                'txtweb-mobile': mobilehash,
                'txtweb-message': data,
                'txtweb-pubkey': '73868ac1-9b70-4063-a298-a4833664a1f3'
            }
            logging.info(urllib.urlencode(args))
            response = urllib2.urlopen("http://api.txtweb.com/v1/push", urllib.urlencode(args)).read()
            self.response.out.write(response)
        else:
            self.response.out.write("No hash saved")


class VerifyHandler(BaseRequestHandler):
    def get(self):
        """Handles GET /verify"""
        invalid_cred = self.request.self('error')
        if self.logged_in:
            user = self.current_user
            values = {
                'error': invalid_cred,
                'user': user,
                'session': self.auth.get_user_by_session(),
                'data': user.to_dict()
            }
            self.render('verify.html', values)
        else:
            self.redirect('/')

    def post(self):
        """Handles POST /verify"""
        if self.logged_in:
            post_regno = self.request.get('regno')
            post_dob = self.request.get('dob')
            if re.search("[0-9]{2}[A-Z|a-z]{3}[0-9]{3,4}", post_regno):
                #verify regno and dob here using post_regno and post_dob
                self.redirect()
            else:
                self.redirect('/verify?error=InvalidCred')
        else:
            self.redirect('/')