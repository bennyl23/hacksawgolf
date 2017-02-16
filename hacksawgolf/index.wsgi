import os
import sys
import site

# Add the site-packages of the chosen virtualenv to work with
site.addsitedir('~/.virtualenvs/hacksawgolf/lib/python2.7/site-packages')

# Add the app's directory to the PYTHONPATH
sys.path.append('/projects/hacksawgolf/hacksawgolf')
sys.path.append('/projects/hacksawgolf/hacksawgolf/hacksawgolf')

os.environ['DJANGO_SETTINGS_MODULE'] = 'hacksawgolf.settings'

os.environ['HTTPS'] = "off"

# Activate your virtual env
activate_env=os.path.expanduser("/virtualenvs/hacksawgolf/bin/activate_this.py")
execfile(activate_env, dict(__file__=activate_env))

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
