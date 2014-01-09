# -*- coding: utf-8 -*-
import sys
from secrets import SESSION_KEY

from webapp2 import WSGIApplication, Route

# inject './lib' dir in the path so that we can simply do "import ndb" 
# or whatever there's in the app lib dir.
if 'lib' not in sys.path:
    sys.path[0:0] = ['lib']

# webapp2 config
app_config = {
  'webapp2_extras.sessions': {
    'cookie_name': '_simpleauth_sess',
    'secret_key': SESSION_KEY
  },
  'webapp2_extras.auth': {
    'user_attributes': []
  }
}
    
# Map URLs to handler
routes = [
  Route('/', handler='handlers.RootHandler', name='root'),
  Route('/dashboard', handler='handlers.DashboardHandler', name='profile'),
  Route('/subject/<classnbr>', handler='handlers.SubjectHandler', name='subject'),
  Route('/timetable', handler='handlers.TimetableHandler', name='timetable'),
  Route('/notice', handler='handlers.NoticeHandler', name='notice'),
  Route('/noticedel/<noticeid>/<classnbr>', handler='handlers.NoticeDeleteHandler', name='noticedel'),
  Route('/disclaimer', handler='handlers.DisclaimerHandler', name='disclaimer'),
  Route('/sms', handler='handlers.SMSHandler', name='smsusage'),
  Route('/backend', handler='handlers.BackendHandler', name='backend'),
  Route('/logout', handler='handlers.AuthHandler:logout', name='logout'),
  Route('/auth/<provider>',
    handler='handlers.AuthHandler:_simple_auth', name='auth_login'),
  Route('/auth/<provider>/callback',
    handler='handlers.AuthHandler:_auth_callback', name='auth_callback'),
  Route('/txtweb',
    handler='handlers.txtWebHandler', name='txtweb'),
  Route('/txtwebdispatch',
    handler='handlers.txtWebDispatchHandler', name='txtweb')
]

app = WSGIApplication(routes, config=app_config, debug=True)
