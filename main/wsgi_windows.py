activate_this = 'C:/VES/PRODUCTION/Scripts/activate_this.py'
# execfile(activate_this, dict(__file__=activate_this))
exec(open(activate_this).read(),dict(__file__=activate_this))

import os
import sys
import site

# Add the site-packages of the chosen virtualenv to work with
site.addsitedir('C:/VES/PRODUCTION/Lib/site-packages')


# Add the app's directory to the PYTHONPATH
sys.path.append('C:/APPS/diris-reclamos')
sys.path.append('C:/APPS/diris-reclamos/main')

os.environ['DJANGO_SETTINGS_MODULE'] = 'main.settings_main.prod_windows'
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "main.settings_main.prod_windows")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()