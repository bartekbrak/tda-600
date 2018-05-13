import environ


this = environ.Path(__file__)
repo = this - 4
backend = this - 3
whale = this - 2
env = environ.Env(DEBUG=(bool, False), )
# environ.Env.read_env(repo('.env'))
SITE_ROOT = whale()

SECRET_KEY = 'q+xd2#&_xbdng5dk#!9ymb9@hi1)m1uswp&rxbn3j36a+tc-mb'
DEBUG = False

ALLOWED_HOSTS = []
INSTALLED_APPS = [
    # 'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    # 'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'dynamic_rest',
    'core',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    # 'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
            ],
        },
    },
]


ROOT_URLCONF = 'backend.urls'


WSGI_APPLICATION = 'backend.wsgi.application'

DATABASES = {
    'default': env.db(default='postgresql:///tda600'),
    'extra': env.db('SQLITE_URL', default='sqlite:///tda600.sqlite3')
}
DATABASES['default']['ATOMIC_REQUESTS'] = True
AUTH_PASSWORD_VALIDATORS = []
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = False
USE_L10N = False
USE_TZ = True
STATIC_URL = '/static/'
