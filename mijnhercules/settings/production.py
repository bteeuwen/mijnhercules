from .base import *

import dj_database_url

# heroku database resolver
DATABASES['default'] =  dj_database_url.config()

# try:
#     DATABASES['default'] =  dj_database_url.config()
# except:
#     pass

# celery free plan limitation heroku addon https://devcenter.heroku.com/articles/cloudamqp
BROKER_POOL_LIMIT = 1
BROKER_URL = os.environ['CLOUDAMQP_URL']
