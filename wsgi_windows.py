from django.core.wsgi import get_wsgi_application

activate_this = 'C:/Users/BEdev/Envs/BEOperations/Scripts/activate_this.py'
# execfile(activate_this, dict(__file__=activate_this))
exec(open(activate_this).read(),dict(__file__=activate_this))

import os
import sys
import site

# Add the site-packages of the chosen virtualenv to work with
site.addsitedir('C:/Users/BEdev/Envs/BEOperations/Lib/site-packages')

# Add the app's directory to the PYTHONPATH
sys.path.append('C:/Users/BEdev/Documents/BEOperations/BEOperations')
sys.path.append('C:/Users/BEdev/Documents/BEOperations/BEOperations/BEOperations')

os.environ['DJANGO_SETTINGS_MODULE'] = 'BEOperations.settings'
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "BEOperations.settings")

# application = get_wsgi_application()
django_app = get_wsgi_application()
