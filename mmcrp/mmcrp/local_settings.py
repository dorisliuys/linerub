from settings import PROJECT_ROOT, BASE_DIR
import os

DEBUG = True
TEMPLATE_DEBUG = True

DATABASES = {
"default": {
  "ENGINE": "django.db.backends.postgresql_psycopg2",
  "NAME": "mmcrp_base",
  "USER": "postgres",
  "PASSWORD": "Jr94oo2",
  "HOST": "localhost",
  "PORT": "5432",
}
}
