# -*- coding: utf-8 -*-
import datetime
import logging
import os
import socket

from django.utils.functional import lazy

from heka.config import client_from_dict_config

from mkt import asset_bundles

#################################################
# Environment.
#
# Make filepaths relative to the root of zamboni.
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
path = lambda *a: os.path.join(ROOT, *a)

# We need to track this because jenkins can't just call its checkout "zamboni".
# It puts it in a dir called "workspace".  Way to be, jenkins.
ROOT_PACKAGE = os.path.basename(ROOT)

# The host currently running the site.  Only use this in code for good reason;
# the site is designed to run on a cluster and should continue to support that
HOSTNAME = socket.gethostname()

try:
    # If we have build ids available, we'll grab them here and add them to our
    # CACHE_PREFIX.  This will let us not have to flush memcache during updates
    # and it will let us preload data into it before a production push.
    from build import BUILD_ID_CSS, BUILD_ID_JS
    build_id = '%s%s' % (BUILD_ID_CSS[:2], BUILD_ID_JS[:2])
except ImportError:
    build_id = ''

##########################################
# Standard Django configuration variables.
#
# Please see the Django documentation for information on these
# variables: https://docs.djangoproject.com/en/dev/ref/settings/
ADMINS = ()
ALLOWED_HOSTS = [
    '.allizom.org',
    '.mozilla.org',
    '.mozilla.com',
    '.mozilla.net',
    '.firefox.com',
    '.firefox.com.cn'
]

AUTH_USER_MODEL = 'users.UserProfile'
AUTHENTICATION_BACKENDS = ('django_browserid.auth.BrowserIDBackend',)

CACHE_MIDDLEWARE_SECONDS = 60 * 3
CSRF_FAILURE_VIEW = 'mkt.site.views.csrf_failure'

DATABASE_ROUTERS = ('multidb.PinningMasterSlaveRouter',)
DATABASES = {
    'default': {
        'NAME': 'zamboni',
        'ENGINE': 'django.db.backends.mysql',
        'HOST': '',
        'PORT': '',
        'USER': '',
        'PASSWORD': '',
        'OPTIONS': {'init_command': 'SET storage_engine=InnoDB'},
        'TEST_CHARSET': 'utf8',
        'TEST_COLLATION': 'utf8_general_ci',
    },
}

DEBUG = True
DEBUG_PROPAGATE_EXCEPTIONS = True
DEFAULT_FROM_EMAIL = 'Firefox Marketplace <nobody@mozilla.org>'
DOMAIN = HOSTNAME

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

INSTALLED_APPS = (
    'amo',  # amo comes first so it always takes precedence.
    'abuse',
    'access',
    'addons',
    'applications',
    'cronjobs',
    'csp',
    'editors',
    'files',
    'jingo_minify',
    'lib.es',
    'product_details',
    'reviews',
    'stats',
    'tags',
    'tower',  # for ./manage.py extract
    'translations',
    'users',
    'versions',
    'zadmin',

    # Third party apps
    'djcelery',
    'django_extensions',
    'django_nose',
    'gunicorn',
    'raven.contrib.django',
    'waffle',

    # Django contrib apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.messages',
    'django.contrib.sessions',

    # Has to load after auth
    'django_browserid',
    'django_statsd',

    'devhub',  # Put here so helpers.py doesn't get loaded first.
    'mkt.site',
    'mkt.account',
    'mkt.api',
    'mkt.collections',
    'mkt.comm',
    'mkt.commonplace',
    'mkt.detail',
    'mkt.developers',
    'mkt.ecosystem',
    'mkt.feed',
    'mkt.files',
    'mkt.fireplace',
    'mkt.inapp',
    'mkt.lookup',
    'mkt.monolith',
    'mkt.operators',
    'mkt.purchase',
    'mkt.prices',
    'mkt.ratings',
    'mkt.receipts',
    'mkt.reviewers',
    'mkt.search',
    'mkt.stats',
    'mkt.submit',
    'mkt.zadmin',
    'mkt.webapps',
    'mkt.webpay',
)

MIDDLEWARE_CLASSES = (
    'mkt.api.middleware.GZipMiddleware',
    'mkt.site.middleware.CacheHeadersMiddleware',
    'django_statsd.middleware.GraphiteMiddleware',
    'amo.middleware.RemoveSlashMiddleware',
    # Munging REMOTE_ADDR must come before ThreadRequest.
    'commonware.middleware.SetRemoteAddrFromForwardedFor',
    'commonware.middleware.StrictTransportMiddleware',
    'waffle.middleware.WaffleMiddleware',
    'csp.middleware.CSPMiddleware',
    'amo.middleware.CommonMiddleware',
    'amo.middleware.NoVarySessionMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'commonware.log.ThreadRequestMiddleware',
    'mkt.search.middleware.ElasticsearchExceptionMiddleware',
    'session_csrf.CsrfMiddleware',
    'commonware.middleware.ScrubRequestOnException',
    'mkt.site.middleware.RequestCookiesMiddleware',
    'mkt.site.middleware.RedirectPrefixedURIMiddleware',
    'mkt.api.middleware.RestOAuthMiddleware',
    'mkt.api.middleware.RestSharedSecretMiddleware',
    'access.middleware.ACLMiddleware',
    'mkt.site.middleware.LocaleMiddleware',
    'mkt.regions.middleware.RegionMiddleware',
    'mkt.site.middleware.DeviceDetectionMiddleware',
    'mkt.site.middleware.DoNotTrackTrackingMiddleware',
    'mkt.api.middleware.TimingMiddleware',
    'mkt.api.middleware.APIVersionMiddleware',
    'mkt.api.middleware.CORSMiddleware',
    'mkt.api.middleware.APIPinningMiddleware',
    'mkt.api.middleware.APITransactionMiddleware',
    'mkt.api.middleware.APIFilterMiddleware',
)

LANGUAGE_CODE = 'en-US'
LOCALE_PATHS = (path('locale'),)

LOGIN_URL = '/login'
LOGIN_REDIRECT_URL = '/'
LOGOUT_URL = '/logout'
LOGOUT_REDIRECT_URL = '/developers/'

LOGGING = {
    'loggers': {
        'amqplib': {'handlers': ['null']},
        'caching.invalidation': {'handlers': ['null']},
        'caching': {'level': logging.WARNING},
        'suds': {'handlers': ['null']},
        'z.task': {'level': logging.INFO},
        'z.es': {'level': logging.INFO},
        'z.heka': {'level': logging.INFO},
        's.client': {'level': logging.INFO},
        'nose': {'level': logging.WARNING},
    },
}
LOGGING_CONFIG = None

MANAGERS = ADMINS
MEDIA_ROOT = path('media')
MEDIA_URL = '/media/'

PASSWORD_HASHERS = ()

ROOT_URLCONF = 'mkt.urls'

SECRET_KEY = 'please change this'

SESSION_ENGINE = 'django.contrib.sessions.backends.signed_cookies'
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_COOKIE_AGE = 1209600
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_DOMAIN = ".%s" % DOMAIN  # bug 608797
MESSAGE_STORAGE = 'django.contrib.messages.storage.cookie.CookieStorage'

TEMPLATE_DEBUG = DEBUG

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.media',
    'django.core.context_processors.request',
    'session_csrf.context_processor',
    'django.contrib.messages.context_processors.messages',
    'amo.context_processors.i18n',
    'amo.context_processors.static_url',
    'jingo_minify.helpers.build_ids',
    'mkt.site.context_processors.global_settings',
    'mkt.carriers.context_processors.carrier_data',
)

TEMPLATE_DIRS = (
    path('media/docs'),
    path('templates'),
    path('mkt/templates'),
    path('mkt/zadmin/templates')
)

TEMPLATE_LOADERS = (
    'lib.template_loader.Loader',
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

TIME_ZONE = 'America/Los_Angeles'

USE_ETAGS = True
USE_I18N = True

######################################################
# Project specific ones.
# - Grouped by purpose then alpha.
# - If a variable is needed by others, its moved to the top of the section

###########################################
# Team Emails
ABUSE_EMAIL = 'Firefox Marketplace Staff <marketplace-staff+abuse@mozilla.org>'
EDITORS_EMAIL = 'amo-editors@mozilla.org'
FLIGTAR = 'marketplace-staff+random-goings-on@mozilla.org'
MARKETPLACE_EMAIL = 'marketplace-staff@mozilla.org'
MKT_FEEDBACK_EMAIL = 'apps-feedback@mozilla.com'
MKT_REVIEWERS_EMAIL = 'app-reviewers@mozilla.org'
MKT_SENIOR_EDITORS_EMAIL = 'marketplace-staff+escalations@mozilla.org'
MKT_SUPPORT_EMAIL = 'app-reviewers@mozilla.org'
NOBODY_EMAIL = 'Firefox Marketplace <nobody@mozilla.org>'
SENIOR_EDITORS_EMAIL = 'amo-admin-reviews@mozilla.org'
THEMES_EMAIL = 'theme-reviews@mozilla.org'

###########################################
# Paths
#
# Absolute path to a temporary storage area
TMP_PATH = path('tmp')

# Absolute path to a writable directory shared by all servers. No trailing
# slash.  Example: /data/
NETAPP_STORAGE = TMP_PATH
# Absolute path to a writable directory shared by all servers. No trailing
# slash.
# Example: /data/uploads
UPLOADS_PATH = NETAPP_STORAGE + '/uploads'

PREVIEWS_PATH = UPLOADS_PATH + '/previews'

ADDON_ICONS_DEFAULT_PATH = os.path.join(MEDIA_ROOT, 'img/hub')
ADDON_ICONS_PATH = UPLOADS_PATH + '/addon_icons'

#  File path for storing XPI/JAR files (or any files associated with an
#  add-on). Example: /mnt/netapp_amo/addons.mozilla.org-remora/files
ADDONS_PATH = NETAPP_STORAGE + '/addons'
CA_CERT_BUNDLE_PATH = os.path.join(ROOT, 'apps/amo/certificates/roots.pem')
COLLECTIONS_ICON_PATH = UPLOADS_PATH + '/collection_icons'

# Where dumped apps will be written too.
DUMPED_APPS_PATH = NETAPP_STORAGE + '/dumped-apps'

# Where dumped apps will be written too.
DUMPED_USERS_PATH = NETAPP_STORAGE + '/dumped-users'
FEATURED_APP_BG_PATH = UPLOADS_PATH + '/featured_app_background'

# Like ADDONS_PATH but protected by the app. Used for storing files that should
# not be publicly accessible (like disabled add-ons).
GUARDED_ADDONS_PATH = NETAPP_STORAGE + '/guarded-addons'
IMAGEASSETS_PATH = UPLOADS_PATH + '/imageassets'
LOCAL_MIRROR_URL = 'https://static.addons.mozilla.net/_files'

# File path for add-on files that get rsynced to mirrors.
# /mnt/netapp_amo/addons.mozilla.org-remora/public-staging
MIRROR_STAGE_PATH = NETAPP_STORAGE + '/public-staging'
PREVIEW_FULL_PATH = PREVIEWS_PATH + '/full/%s/%d.%s'
PREVIEW_THUMBNAIL_PATH = PREVIEWS_PATH + '/thumbs/%s/%d.png'

# Path to store webpay product icons.
PRODUCT_ICON_PATH = NETAPP_STORAGE + '/product-icons'

REVIEWER_ATTACHMENTS_PATH = UPLOADS_PATH + '/reviewer_attachment'

# When True, create a URL root /tmp that serves files in your temp path.
# This is useful for development to view upload pics, etc.
# NOTE: This only works when DEBUG is also True.
SERVE_TMP_PATH = False

# Used for storing signed webapps.
SIGNED_APPS_PATH = NETAPP_STORAGE + '/signed-apps'

# Special reviewer signed ones for special people.
SIGNED_APPS_REVIEWER_PATH = NETAPP_STORAGE + '/signed-apps-reviewer'
USERPICS_PATH = UPLOADS_PATH + '/userpics'

###########################################
# URLs
#
# URLs other things depend upon.
SITE_URL = 'http://%s' % DOMAIN
STATIC_URL = SITE_URL + '/'
VAMO_URL = 'https://versioncheck.addons.mozilla.org'

# TODO: Remove me when ADDON_ICON_URL goes away.
DEFAULT_APP = 'firefox'

ADDON_ICONS_DEFAULT_URL = MEDIA_URL + '/img/hub'
ADDON_ICON_URL = (STATIC_URL +
                  'img/uploads/addon_icons/%s/%s-%s.png?modified=%s')
ADDON_ICON_BASE_URL = MEDIA_URL + 'img/icons/'

COLLECTION_ICON_URL = (STATIC_URL +
                       'img/uploads/collection_icons/%s/%s.png?m=%s')

MIRROR_URL = 'http://releases.mozilla.org/pub/mozilla.org/addons'
NEW_PERSONAS_IMAGE_URL = STATIC_URL + 'img/uploads/themes/%(id)d/%(file)s'
NEW_PERSONAS_UPDATE_URL = VAMO_URL + '/%(locale)s/themes/update-check/%(id)d'
PERSONAS_IMAGE_URL = ('http://getpersonas.cdn.mozilla.net/static/'
                      '%(tens)d/%(units)d/%(id)d/%(file)s')
PERSONAS_IMAGE_URL_SSL = ('https://getpersonas.cdn.mozilla.net/static/'
                          '%(tens)d/%(units)d/%(id)d/%(file)s')
PERSONAS_UPDATE_URL = VAMO_URL + '/%(locale)s/themes/update-check/%(id)d'
PREVIEW_THUMBNAIL_URL = (STATIC_URL +
                         'img/uploads/previews/thumbs/%s/%d.png?modified=%d')
PREVIEW_FULL_URL = (STATIC_URL +
                    'img/uploads/previews/full/%s/%d.%s?modified=%d')
PRIVATE_MIRROR_URL = '/_privatefiles'

# Base URL where webpay product icons are served from.
PRODUCT_ICON_URL = MEDIA_URL + '/product-icons'
USERPICS_URL = STATIC_URL + 'img/uploads/userpics/%s/%s/%s.png?modified=%d'

# The verification URL, the addon id will be appended to this. This will
# have to be altered to the right domain for each server, eg:
# https://receiptcheck.addons.mozilla.org/verify/
WEBAPPS_RECEIPT_URL = SITE_URL + '/verify/'

###########################################
# Celery
BROKER_URL = 'amqp://zamboni:zamboni@localhost:5672/zamboni'
BROKER_CONNECTION_TIMEOUT = 0.1

CEF_PRODUCT = "amo"

# Testing responsiveness without rate limits.
CELERY_DISABLE_RATE_LIMITS = True

CELERY_IGNORE_RESULT = True
CELERY_IMPORTS = ('lib.video.tasks', 'lib.metrics',
                  'lib.es.management.commands.reindex_mkt')
CELERY_RESULT_BACKEND = 'amqp'

# We have separate celeryds for processing devhub & images as fast as possible
# Some notes:
# - always add routes here instead of @task(queue=<name>)
# - when adding a queue, be sure to update deploy.py so that it gets restarted
CELERY_ROUTES = {
    # Priority.
    # If your tasks need to be run as soon as possible, add them here so they
    # are routed to the priority queue.
    'lib.crypto.packaged.sign': {'queue': 'priority'},
    'mkt.inapp_pay.tasks.fetch_product_image': {'queue': 'priority'},
    'mkt.webapps.tasks.index_webapps': {'queue': 'priority'},
    'mkt.webapps.tasks.unindex_webapps': {'queue': 'priority'},
    'stats.tasks.update_monolith_stats': {'queue': 'priority'},
    'versions.tasks.update_supported_locales_single': {'queue': 'priority'},
    # And the rest.
    'mkt.developers.tasks.validator': {'queue': 'devhub'},
    'mkt.developers.tasks.file_validator': {'queue': 'devhub'},
    'mkt.developers.tasks.resize_icon': {'queue': 'images'},
    'mkt.developers.tasks.resize_preview': {'queue': 'images'},
    'mkt.developers.tasks.fetch_icon': {'queue': 'devhub'},
    'mkt.developers.tasks.fetch_manifest': {'queue': 'devhub'},
    'lib.video.tasks.resize_video': {'queue': 'devhub'},
    'mkt.webapps.tasks.regenerate_icons_and_thumbnails': {'queue': 'images'},
    'mkt.comm.tasks.migrate_activity_log': {'queue': 'limited'},
    'mkt.webapps.tasks.pre_generate_apk': {'queue': 'devhub'},
}

CELERY_SEND_TASK_ERROR_EMAILS = True

# This is just a place to store these values, you apply them in your
# task decorator, for example:
#   @task(time_limit=CELERY_TIME_LIMITS['lib...']['hard'])
# Otherwise your task will use the default settings.
CELERY_TIME_LIMITS = {
    'lib.video.tasks.resize_video': {'soft': 360, 'hard': 600},
    'lib.es.management.commands.reindex_mkt.run_indexing': {
        'soft': 60 * 20,  # 20 mins to reindex.
        'hard': 60 * 120,  # 120 mins hard limit.
    },
}

# When testing, we always want tasks to raise exceptions. Good for sanity.
CELERY_EAGER_PROPAGATES_EXCEPTIONS = True

CELERYD_HIJACK_ROOT_LOGGER = False

# Time in seconds before celery.exceptions.SoftTimeLimitExceeded is raised.
# The task can catch that and recover but should exit ASAP. Note that there is
# a separate, shorter timeout for validation tasks.
CELERYD_TASK_SOFT_TIME_LIMIT = 60 * 2


###########################################
# General
#
# This is a sample AES_KEY, we will override this on each server.
AES_KEYS = {
    'api:access:secret': os.path.join(ROOT, 'mkt/api/sample-aes.key'),
}

# If you want to allow self-reviews for add-ons/apps, then enable this.
# In production we do not want to allow this.
ALLOW_SELF_REVIEWS = False

# A smaller range of languages for the Marketplace.
AMO_LANGUAGES = (
    'bg', 'bn-BD', 'ca', 'cs', 'da', 'de', 'el', 'en-US', 'es', 'fr', 'ga-IE',
    'hr', 'hu', 'it', 'ja', 'ko', 'mk', 'nb-NO', 'nl', 'pl', 'pt-BR', 'ro',
    'ru', 'sk', 'sq', 'sr', 'sr-Latn', 'tr', 'zh-CN', 'zh-TW',
)


def lazy_langs(languages):
    from product_details import product_details
    if not product_details.languages:
        return {}
    return dict([(i.lower(), product_details.languages[i]['native'])
                 for i in languages])

# Override Django's built-in with our native names, this is a Django setting
# but we are putting it here because its being overridden.
LANGUAGES = lazy(lazy_langs, dict)(AMO_LANGUAGES)

# The currently-recommended version of the API. Any requests to versions older
# than this will include the `API-Status: Deprecated` header.
API_CURRENT_VERSION = 1

# When True, the API will return a full traceback when an exception occurs.
API_SHOW_TRACEBACKS = False

# Whether to throttle API requests. Default is True. Disable where appropriate.
API_THROTTLE = True

# The version we append to the app feature profile. Bump when we add new app
# features to the `AppFeatures` model.
APP_FEATURES_VERSION = 4

# Temporary variables for the app-preview server, set this to True
# if you want to experience app-preview.mozilla.org.
APP_PREVIEW = True

# This is the aud (audience) for app purchase JWTs.
# It must match that of the pay server that processes nav.mozPay().
# In webpay this is the DOMAIN setting and on B2G this must match
# what's in the provider whitelist.
APP_PURCHASE_AUD = 'marketplace-dev.allizom.org'

# This is the iss (issuer) for app purchase JWTs.
# It must match that of the pay server that processes nav.mozPay().
# In webpay this is the ISSUER setting.
APP_PURCHASE_KEY = 'marketplace-dev.allizom.org'

# This is the shared secret key for signing app purchase JWTs.
# It must match that of the pay server that processes nav.mozPay().
# In webpay this is the SECRET setting.
APP_PURCHASE_SECRET = ''

# This is the typ for app purchase JWTs.
# It must match that of the pay server that processes nav.mozPay().
# On B2G this must match a provider in the whitelist.
APP_PURCHASE_TYP = 'mozilla/payments/pay/v1'

# Base URL to the Bango Vendor Portal (keep the trailing question mark).
BANGO_BASE_PORTAL_URL = 'http://mozilla.com.test.bango.org/login/al.aspx?'

# A solitude specific settings that allows you to send fake refunds to
# solitude. The matching setting will have to be on in solitude, otherwise
# it will just laugh at your request.
BANGO_FAKE_REFUNDS = False

# Basket subscription url for newsletter signups
BASKET_URL = 'https://basket.mozilla.com'

# URL to Boku signup flow, this will change per server.
# See https://mana.mozilla.org/wiki/display/MARKET/Boku for more.
#
# This a good test one that developers can use.
BOKU_SIGNUP_URL = ('https://merchants.boku.com/signup/signup_business?'
                   'params=jEHWaTM7zm5cbPpheT2iS4xB1mkzO85uxVAo7rs7LVgy'
                   '5JYGMWnUYDvxyEk8lxalYW56b6hrqfw%3D')
BOKU_PORTAL = 'https://merchants.boku.com/merchant_product_statistics'

# Domain to allow cross-frame requests from for privacy policy and TOS.
BROWSERID_DOMAIN = 'login.persona.org'

# Adjust these settings if you need to use a custom verifier.
BROWSERID_JS_URL = 'https://login.persona.org/include.js'
BROWSERID_VERIFICATION_URL = 'https://verifier.login.persona.org/verify'

# Number of seconds a count() query should be cached.  Keep it short because
# it's not possible to invalidate these queries.
CACHE_COUNT_TIMEOUT = 60

# A Django cache machine setting, that hasn't been updated to use the
# new PREFIX in the CACHE setttings.
CACHE_PREFIX = 'marketplace:%s' % build_id

# Cache timeout on the /search/featured API.
CACHE_SEARCH_FEATURED_API_TIMEOUT = 60 * 60  # 1 hour.

# jingo-minify settings
CACHEBUST_IMGS = True
try:
    # If we have build ids available, we'll grab them here and add them to our
    # CACHE_PREFIX.  This will let us not have to flush memcache during updates
    # and it will let us preload data into it before a production push.
    from build import BUILD_ID_CSS, BUILD_ID_JS
    build_id = "%s%s" % (BUILD_ID_CSS[:2], BUILD_ID_JS[:2])
except ImportError:
    build_id = ""

# Path to cleancss (our CSS minifier).
CLEANCSS_BIN = 'cleancss'

# Name of our Commonplace repositories on GitHub.
COMMONPLACE_REPOS = ['commbadge', 'fireplace', 'marketplace-stats',
                     'rocketfuel']
COMMONPLACE_REPOS_APPCACHED = []

# CSP Settings
CSP_REPORT_URI = '/services/csp/report'
CSP_POLICY_URI = '/services/csp/policy?build=%s' % build_id
CSP_REPORT_ONLY = True

CSP_ALLOW = ("'self'",)
CSP_IMG_SRC = (
    "'self'", SITE_URL,
    'https://ssl.google-analytics.com',
    'https://www.google-analytics.com',
    'https://*.newrelic.com',
    'data:'
)
CSP_SCRIPT_SRC = (
    "'self'", SITE_URL,
    'https://login.persona.org',
    'https://firefoxos.persona.org',
    'https://ssl.google-analytics.com',
    'https://www.google-analytics.com',
    'https://*.newrelic.com',
)
CSP_STYLE_SRC = ("'self'", SITE_URL,)
CSP_OBJECT_SRC = ("'none'",)
CSP_MEDIA_SRC = ("'none'",)
CSP_FRAME_SRC = (
    'https://s3.amazonaws.com',
    'https://ssl.google-analytics.com',
    'https://login.persona.org',
    'https://firefoxos.persona.org',
    'https://www.youtube.com',
)
CSP_FONT_SRC = ("'self'", 'fonts.mozilla.org', 'www.mozilla.org',)

# jingo-minify: Style sheet media attribute default
CSS_MEDIA_DEFAULT = 'all'

DATABASE_ROUTERS = ('multidb.PinningMasterSlaveRouter',)

# For use django-mysql-pool backend.
DATABASE_POOL_ARGS = {
    'max_overflow': 10,
    'pool_size': 5,
    'recycle': 300
}

# Default file storage mechanism that holds media.
DEFAULT_FILE_STORAGE = 'amo.utils.LocalFileStorage'

# If you need to get a payment provider, which one will be the default?
DEFAULT_PAYMENT_PROVIDER = 'bango'

# When the dev. agreement gets updated and you need users to re-accept it
# change this date. You won't want to do this for minor format changes.
# The tuple is passed through to datetime.date, so please use a valid date
# tuple. If the value is None, then it will just not be used at all.
DEV_AGREEMENT_LAST_UPDATED = datetime.date(2012, 2, 23)

# Tells the extract script what files to look for l10n in and what function
# handles the extraction.  The Tower library expects this.
DOMAIN_METHODS = {
    'messages': [
        ('apps/**.py',
            'tower.management.commands.extract.extract_tower_python'),
        ('apps/**/templates/**.html',
            'tower.management.commands.extract.extract_tower_template'),
        ('templates/**.html',
            'tower.management.commands.extract.extract_tower_template'),
        ('mkt/**.py',
            'tower.management.commands.extract.extract_tower_python'),
        ('mkt/**/templates/**.html',
            'tower.management.commands.extract.extract_tower_template'),
        ('mkt/templates/**.html',
            'tower.management.commands.extract.extract_tower_template'),
        ('**/templates/**.lhtml',
            'tower.management.commands.extract.extract_tower_template'),
    ],
    'javascript': [
        # We can't say **.js because that would dive into mochikit and timeplot
        # and all the other baggage we're carrying.  Timeplot, in particular,
        # crashes the extractor with bad unicode data.
        ('media/js/*.js', 'javascript'),
        ('media/js/common/**.js', 'javascript'),
        ('media/js/impala/**.js', 'javascript'),
        ('media/js/zamboni/**.js', 'javascript'),
        ('media/js/devreg/**.js', 'javascript'),
    ],
}

# Tarballs in DUMPED_APPS_PATH deleted 30 days after they have been written.
DUMPED_APPS_DAYS_DELETE = 3600 * 24 * 30

# Tarballs in DUMPED_USERS_PATH deleted 30 days after they have been written.
DUMPED_USERS_DAYS_DELETE = 3600 * 24 * 30

# Please use all lowercase for the blacklist.
EMAIL_BLACKLIST = (
    'nobody@mozilla.org',
)

# Error generation service. Should *not* be on in production.
ENABLE_API_ERROR_SERVICE = False

ENGAGE_ROBOTS = True

# ElasticSearch
ES_DEFAULT_NUM_REPLICAS = 2
ES_DEFAULT_NUM_SHARDS = 5
ES_HOSTS = ['127.0.0.1:9200']
ES_INDEXES = {'webapp': 'apps'}
ES_URLS = ['http://%s' % h for h in ES_HOSTS]
ES_USE_PLUGINS = False
ES_TIMEOUT = 30

# When True include full tracebacks in JSON. This is useful for QA on preview.
EXPOSE_VALIDATOR_TRACEBACKS = False

# Django cache machine settings.
FETCH_BY_ID = True

# The maximum file size that is shown inside the file viewer.
FILE_VIEWER_SIZE_LIMIT = 1048576

# The maximum file size that you can have inside a zip file.
FILE_UNZIP_SIZE_LIMIT = 104857600

# The origin URL for our Fireplace frontend, from which API requests come.
FIREPLACE_URL = ''

# Where to find ffmpeg and totem if it's not in the PATH.
FFMPEG_BINARY = 'ffmpeg'

# GeoIP server settings
# This flag overrides the GeoIP server functions and will force the
# return of the GEOIP_DEFAULT_VAL
GEOIP_URL = ''
GEOIP_DEFAULT_VAL = 'restofworld'
GEOIP_DEFAULT_TIMEOUT = .2

# Credentials for accessing Google Analytics stats.
GOOGLE_ANALYTICS_CREDENTIALS = {}

# Which domain to access GA stats for. If not set, defaults to DOMAIN.
GOOGLE_ANALYTICS_DOMAIN = None

# Used for general web API access.
GOOGLE_API_CREDENTIALS = ''

# Google translate settings.
GOOGLE_TRANSLATE_API_URL = 'https://www.googleapis.com/language/translate/v2'
GOOGLE_TRANSLATE_REDIRECT_URL = (
    'https://translate.google.com/#auto/{lang}/{text}')

HAS_SYSLOG = True  # syslog is used if HAS_SYSLOG and NOT DEBUG.

HEKA_CONF = {
    'logger': 'zamboni',
    'plugins': {
        'cef': ('heka_cef.cef_plugin:config_plugin', {
            'syslog_facility': 'LOCAL4',
            'syslog_ident': 'http_app_addons_marketplace',
            'syslog_priority': 'ALERT',
            }),

        # Sentry accepts messages over UDP, you'll need to
        # configure this URL so that logstash can relay the message
        # properly
        'raven': ('heka_raven.raven_plugin:config_plugin', {
            'dsn': 'udp://username:password@127.0.0.1:9000/2'}),
        },
    'stream': {
        'class': 'heka.streams.UdpStream',
        'host': '127.0.0.1',
        'port': 5565,
    },
}

HEKA = client_from_dict_config(HEKA_CONF)

# Not shown on the site, but .po files exist and these are available on the
# L10n dashboard.  Generally languages start here and move into AMO_LANGUAGES.
# This list also enables translation edits.
HIDDEN_LANGUAGES = (
    # List of languages from AMO's settings (excluding mkt's active locales).
    'af', 'ar', 'eu', 'fa', 'fi', 'he', 'id', 'mn', 'pt-PT', 'sl', 'sv-SE',
    'uk', 'vi',
    # The hidden list from AMO's settings:
    'cy',
)

# Name of view to use for homepage. AMO uses this. Marketplace has its own.
HOME = 'addons.views.home'

# IARC content ratings.
IARC_ALLOW_CERT_REUSE = False

# Grace period for apps to attain a content rating before they get disabled.
IARC_APP_DISABLE_DATE = datetime.datetime(2014, 4, 15)
IARC_ENV = 'test'
IARC_MOCK = False
IARC_PASSWORD = ''
IARC_PLATFORM = 'Firefox'
IARC_SERVICE_ENDPOINT = ('https://www.globalratings.com'
                         '/IARCDEMOService/IARCServices.svc')
IARC_STOREFRONT_ID = 4
IARC_SUBMISSION_ENDPOINT = ('https://www.globalratings.com'
                            '/IARCDEMORating/Submission.aspx')
IARC_PRIVACY_URL = ('https://www.globalratings.com'
                    '/IARCPRODClient/privacypolicy.aspx')
IARC_TOS_URL = 'https://www.globalratings.com/IARCPRODClient/termsofuse.aspx'


# True when the Django app is running from the test suite.
IN_TEST_SUITE = False

# For YUI compressor.
JAVA_BIN = '/usr/bin/java'

# We don't want jingo's template loaded to pick up templates for third party
# apps that don't use Jinja2. The Following is a list of prefixes for jingo to
# ignore.
JINGO_EXCLUDE_APPS = (
    'djcelery',
    'django_extensions',
    'admin',
    'browserid',
    'toolbar_statsd',
    'registration',
    'debug_toolbar',
    'waffle',
)

JINGO_EXCLUDE_PATHS = (
    'webapps/dump',
    'users/email',
    'reviews/emails',
    'editors/emails',
    'amo/emails',
)

# This saves us when we upgrade jingo-minify (jsocol/jingo-minify@916b054c).
JINGO_MINIFY_USE_STATIC = False


def JINJA_CONFIG():
    import jinja2
    from django.conf import settings
    from django.core.cache import cache
    config = {'extensions': ['tower.template.i18n', 'amo.ext.cache',
                             'jinja2.ext.do',
                             'jinja2.ext.with_', 'jinja2.ext.loopcontrols'],
              'finalize': lambda x: x if x is not None else ''}
    if False and not settings.DEBUG:
        # We're passing the _cache object directly to jinja because
        # Django can't store binary directly; it enforces unicode on it.
        # Details: http://jinja.pocoo.org/2/documentation/api#bytecode-cache
        # and in the errors you get when you try it the other way.
        bc = jinja2.MemcachedBytecodeCache(cache._cache,
                                           "%sj2:" % settings.CACHE_PREFIX)
        config['cache_size'] = -1  # Never clear the cache
        config['bytecode_cache'] = bc
    return config

# IP addresses of servers we use as proxies.
KNOWN_PROXIES = []

LANGUAGE_URL_MAP = dict([(i.lower(), i) for i in AMO_LANGUAGES])

# These domains get `x-frame-options: allow-from` for Privacy Policy / TOS.
UNVERIFIED_ISSUER = 'firefoxos.persona.org'
LEGAL_XFRAME_ALLOW_FROM = [
    BROWSERID_DOMAIN,
    UNVERIFIED_ISSUER,
    'fxos.login.persona.org',
]

# LESS CSS OPTIONS (Debug only).
LESS_PREPROCESS = True  # Compile LESS with Node, rather than client-side JS?
LESS_LIVE_REFRESH = False  # Refresh the CSS on save?
LESS_BIN = 'lessc'

# Handlers and log levels are set up automatically based on LOG_LEVEL.
LOG_LEVEL = logging.DEBUG

LOGIN_RATELIMIT_USER = 5
LOGIN_RATELIMIT_ALL_USERS = '15/m'

# When logging in with browser ID, a username is created automatically.
# In the case of duplicates, the process is recursive up to this number
# of times.
MAX_GEN_USERNAME_TRIES = 50

# Uploaded file limits
MAX_ICON_UPLOAD_SIZE = 4 * 1024 * 1024
MAX_IMAGE_UPLOAD_SIZE = 4 * 1024 * 1024
MAX_PERSONA_UPLOAD_SIZE = 300 * 1024
MAX_PHOTO_UPLOAD_SIZE = MAX_ICON_UPLOAD_SIZE
MAX_REVIEW_ATTACHMENT_UPLOAD_SIZE = 5 * 1024 * 1024
MAX_WEBAPP_UPLOAD_SIZE = 2 * 1024 * 1024
MAX_VIDEO_UPLOAD_SIZE = 4 * 1024 * 1024

# This is the base filename of the `.zip` containing the packaged app for the
# consumer-facing pages of the Marketplace (aka Fireplace). Expected path:
#     /media/packaged-apps/<path>
MARKETPLACE_GUID = 'e6a59937-29e4-456a-b636-b69afa8693b4'

# If the users's Firefox has a version number greater than this we consider it
# a beta.
MIN_BETA_VERSION = '3.7'

# Bundles is a dictionary of two dictionaries, css and js, which list css files
# and js files that can be bundled together by the minify app.
MINIFY_BUNDLES = {
    'css': {
        # CSS files common to the entire site.
        'zamboni/css': (
            'css/legacy/main.css',
            'css/legacy/main-mozilla.css',
            'css/legacy/jquery-lightbox.css',
            'css/legacy/autocomplete.css',
            'css/zamboni/zamboni.css',
            'css/global/headerfooter.css',
            'css/zamboni/tags.css',
            'css/zamboni/tabs.css',
            'css/impala/formset.less',
            'css/impala/suggestions.less',
            'css/impala/header.less',
            'css/impala/moz-tab.css',
            'css/impala/footer.less',
            'css/impala/faux-zamboni.less',
            'css/impala/collection-stats.less',
        ),
        'zamboni/impala': (
            'css/impala/base.css',
            'css/legacy/jquery-lightbox.css',
            'css/impala/site.less',
            'css/impala/typography.less',
            'css/global/headerfooter.css',
            'css/impala/forms.less',
            'css/common/invisible-upload.less',
            'css/impala/header.less',
            'css/impala/footer.less',
            'css/impala/moz-tab.css',
            'css/impala/hovercards.less',
            'css/impala/toplist.less',
            'css/impala/reviews.less',
            'css/impala/buttons.less',
            'css/impala/addon_details.less',
            'css/impala/policy.less',
            'css/impala/expando.less',
            'css/impala/popups.less',
            'css/impala/l10n.less',
            'css/impala/contributions.less',
            'css/impala/lightbox.less',
            'css/impala/prose.less',
            'css/impala/abuse.less',
            'css/impala/paginator.less',
            'css/impala/listing.less',
            'css/impala/versions.less',
            'css/impala/users.less',
            'css/impala/collections.less',
            'css/impala/tooltips.less',
            'css/impala/search.less',
            'css/impala/suggestions.less',
            'css/impala/colorpicker.less',
            'css/impala/login.less',
            'css/impala/dictionaries.less',
            'css/impala/apps.less',
            'css/impala/formset.less',
            'css/impala/tables.less',
        ),
        'zamboni/mobile': (
            'css/zamboni/mobile.css',
            'css/mobile/typography.less',
            'css/mobile/forms.less',
            'css/mobile/header.less',
            'css/mobile/search.less',
            'css/mobile/listing.less',
            'css/mobile/footer.less',
        ),
        'zamboni/admin': (
            'css/zamboni/admin-django.css',
            'css/zamboni/admin-mozilla.css',
            'css/zamboni/admin_features.css',
            # Datepicker styles and jQuery UI core.
            'css/zamboni/jquery-ui/custom-1.7.2.css',
        ),
    },
    'js': {
        # JS files common to the entire site (pre-impala).
        'common': (
            'js/lib/jquery-1.6.4.js',
            'js/lib/underscore.js',
            'js/zamboni/browser.js',
            'js/zamboni/init.js',
            'js/impala/capabilities.js',
            'js/lib/format.js',
            'js/lib/jquery.cookie.js',
            'js/zamboni/storage.js',
            'js/zamboni/apps.js',
            'js/zamboni/buttons.js',
            'js/zamboni/tabs.js',
            'js/common/keys.js',

            # jQuery UI
            'js/lib/jquery-ui/jquery.ui.core.js',
            'js/lib/jquery-ui/jquery.ui.position.js',
            'js/lib/jquery-ui/jquery.ui.widget.js',
            'js/lib/jquery-ui/jquery.ui.mouse.js',
            'js/lib/jquery-ui/jquery.ui.autocomplete.js',
            'js/lib/jquery-ui/jquery.ui.datepicker.js',
            'js/lib/jquery-ui/jquery.ui.sortable.js',

            'js/zamboni/helpers.js',
            'js/zamboni/global.js',
            'js/common/ratingwidget.js',
            'js/lib/jquery-ui/jqModal.js',
            'js/zamboni/l10n.js',
            'js/zamboni/debouncer.js',

            # Homepage
            'js/zamboni/homepage.js',

            # Add-ons details page
            'js/lib/jquery-ui/ui.lightbox.js',
            'js/zamboni/addon_details.js',
            'js/impala/abuse.js',
            'js/zamboni/reviews.js',

            # Users
            'js/zamboni/users.js',

            # Fix-up outgoing links
            'js/zamboni/outgoing_links.js',

            # Hover delay for global header
            'js/global/menu.js',

            # Password length and strength
            'js/zamboni/password-strength.js',

            # Search suggestions
            'js/impala/forms.js',
            'js/impala/ajaxcache.js',
            'js/impala/suggestions.js',
            'js/impala/site_suggestions.js',
        ),

        # Impala and Legacy: Things to be loaded at the top of the page
        'preload': (
            'js/lib/jquery-1.6.4.js',
            'js/impala/preloaded.js',
            'js/zamboni/analytics.js',
        ),
        # Impala: Things to be loaded at the bottom
        'impala': (
            'js/lib/underscore.js',
            'js/zamboni/browser.js',
            'js/zamboni/init.js',
            'js/impala/capabilities.js',
            'js/lib/format.js',
            'js/lib/jquery.cookie.js',
            'js/zamboni/storage.js',
            'js/zamboni/apps.js',
            'js/zamboni/buttons.js',
            'js/lib/jquery.pjax.js',
            'js/impala/footer.js',
            'js/common/keys.js',

            # BrowserID
            'js/zamboni/browserid_support.js',

            # jQuery UI
            'js/lib/jquery-ui/jquery.ui.core.js',
            'js/lib/jquery-ui/jquery.ui.position.js',
            'js/lib/jquery-ui/jquery.ui.widget.js',
            'js/lib/jquery-ui/jquery.ui.mouse.js',
            'js/lib/jquery-ui/jquery.ui.autocomplete.js',
            'js/lib/jquery-ui/jquery.ui.datepicker.js',
            'js/lib/jquery-ui/jquery.ui.sortable.js',

            'js/lib/truncate.js',
            'js/zamboni/truncation.js',
            'js/impala/ajaxcache.js',
            'js/zamboni/helpers.js',
            'js/zamboni/global.js',
            'js/lib/stick.js',
            'js/impala/global.js',
            'js/common/ratingwidget.js',
            'js/lib/jquery-ui/jqModal.js',
            'js/zamboni/l10n.js',
            'js/impala/forms.js',

            # Homepage
            'js/impala/homepage.js',

            # Add-ons details page
            'js/lib/jquery-ui/ui.lightbox.js',
            'js/impala/addon_details.js',
            'js/impala/abuse.js',
            'js/impala/reviews.js',

            # Browse listing pages
            'js/impala/listing.js',

            # Collections
            'js/impala/collections.js',

            # Users
            'js/zamboni/users.js',
            'js/impala/users.js',

            # Search
            'js/impala/serializers.js',
            'js/impala/search.js',
            'js/impala/suggestions.js',
            'js/impala/site_suggestions.js',

            # Login
            'js/impala/login.js',

            # Fix-up outgoing links
            'js/zamboni/outgoing_links.js',
        ),
        'zamboni/files': (
            'js/lib/diff_match_patch_uncompressed.js',
            'js/lib/syntaxhighlighter/xregexp-min.js',
            'js/lib/syntaxhighlighter/shCore.js',
            'js/lib/syntaxhighlighter/shLegacy.js',
            'js/lib/syntaxhighlighter/shBrushAppleScript.js',
            'js/lib/syntaxhighlighter/shBrushAS3.js',
            'js/lib/syntaxhighlighter/shBrushBash.js',
            'js/lib/syntaxhighlighter/shBrushCpp.js',
            'js/lib/syntaxhighlighter/shBrushCSharp.js',
            'js/lib/syntaxhighlighter/shBrushCss.js',
            'js/lib/syntaxhighlighter/shBrushDiff.js',
            'js/lib/syntaxhighlighter/shBrushJava.js',
            'js/lib/syntaxhighlighter/shBrushJScript.js',
            'js/lib/syntaxhighlighter/shBrushPhp.js',
            'js/lib/syntaxhighlighter/shBrushPlain.js',
            'js/lib/syntaxhighlighter/shBrushPython.js',
            'js/lib/syntaxhighlighter/shBrushSass.js',
            'js/lib/syntaxhighlighter/shBrushSql.js',
            'js/lib/syntaxhighlighter/shBrushVb.js',
            'js/lib/syntaxhighlighter/shBrushXml.js',
            'js/zamboni/storage.js',
            'js/zamboni/files.js',
        ),
        'zamboni/mobile': (
            'js/lib/jquery-1.6.4.js',
            'js/lib/underscore.js',
            'js/lib/jqmobile.js',
            'js/lib/jquery.cookie.js',
            'js/zamboni/apps.js',
            'js/zamboni/browser.js',
            'js/zamboni/init.js',
            'js/impala/capabilities.js',
            'js/lib/format.js',
            'js/zamboni/mobile/buttons.js',
            'js/lib/truncate.js',
            'js/zamboni/truncation.js',
            'js/impala/footer.js',
            'js/zamboni/helpers.js',
            'js/zamboni/mobile/general.js',
            'js/common/ratingwidget.js',
            'js/zamboni/browserid_support.js',
        ),
        'zamboni/admin': (
            'js/zamboni/admin.js',
            'js/zamboni/admin_features.js',
            'js/zamboni/admin_validation.js',
        ),
        # This is included when DEBUG is True.  Bundle in <head>.
        'debug': (
            'js/debug/less_setup.js',
            'js/lib/less.js',
            'js/debug/less_live.js',
        ),
    }
}

MINIFY_BUNDLES['css'].update(asset_bundles.CSS)
MINIFY_BUNDLES['js'].update(asset_bundles.JS)

MINIFY_MOZMARKET = True

# Monolith settings.
MONOLITH_SERVER = None
MONOLITH_INDEX = 'time_*'
MONOLITH_MAX_DATE_RANGE = 365

# The issuer for unverified Persona email addresses.
# We only trust one issuer to grant us unverified emails.
# If UNVERIFIED_ISSUER is set to None, forceIssuer will not
# be sent to the client or the verifier.
NATIVE_BROWSERID_DOMAIN = 'firefoxos.persona.org'

# This is a B2G (or other native) verifier. Adjust accordingly.
NATIVE_BROWSERID_JS_URL = ('https://%s/include.js'
                           % NATIVE_BROWSERID_DOMAIN)
NATIVE_BROWSERID_VERIFICATION_URL = ('https://%s/verify'
                                     % NATIVE_BROWSERID_DOMAIN)

# How long to delay tasks relying on file system to cope with NFS lag.
NFS_LAG_DELAY = 3

NOSE_ARGS = [
    '--with-fixture-bundling',
    '--where=%s' % os.path.join(ROOT, 'mkt')
]

# The payment providers supported.
PAYMENT_PROVIDERS = ['bango']

# Auth token required to authorize a postfix host.
POSTFIX_AUTH_TOKEN = 'make-sure-to-override-this-with-a-long-weird-string'

# Domain name of the postfix server.
POSTFIX_DOMAIN = 'marketplace.firefox.com'

PFS_URL = 'https://pfs.mozilla.org/plugins/PluginFinderService.php'

# Path to pngcrush (for image optimization).
PNGCRUSH_BIN = 'pngcrush'

# When True, pre-generate APKs for apps, turn off by default.
PRE_GENERATE_APKS = False

# URL to the APK Factory service.
# See https://github.com/mozilla/apk-factory-service
PRE_GENERATE_APK_URL = (
    'https://apk-controller.dev.mozaws.net/application.apk')


PREINSTALL_CONTACT_EMAIL = 'app-reviewers@mozilla.org'
PREINSTALL_TEST_PLAN_URL = 'docs/app-test-template/v1'
PREINSTALL_TEST_PLAN_PATH = os.path.join(
    MEDIA_ROOT, PREINSTALL_TEST_PLAN_URL + '/en-US.xlsx')
PREINSTALL_TEST_PLAN_LATEST = datetime.datetime.fromtimestamp(
    os.stat(PREINSTALL_TEST_PLAN_PATH).st_mtime)

# Where product details are stored see django-mozilla-product-details
PROD_DETAILS_DIR = path('lib/product_json')

# Number of days the webpay product icon is valid for.
# After this period, the icon will be re-fetched from its external URL.
# If you change this value, update the docs:
# https://developer.mozilla.org/en-US/docs/Web/Apps/Publishing/In-app_payments
PRODUCT_ICON_EXPIRY = 1

# Read-only mode setup.
READ_ONLY = False

# Outgoing URL bouncer
REDIRECT_URL = 'http://outgoing.mozilla.org/v1/'
REDIRECT_SECRET_KEY = ''

REDIS_BACKENDS = {'master': 'redis://localhost:6379?socket_timeout=0.5'}

# Allow URLs from these servers. Use full domain names.
REDIRECT_URL_WHITELIST = ['addons.mozilla.org']

REST_FRAMEWORK = {
    'DEFAULT_MODEL_SERIALIZER_CLASS':
        'rest_framework.serializers.HyperlinkedModelSerializer',
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'mkt.api.authentication.RestOAuthAuthentication',
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'mkt.api.renderers.SuccinctJSONRenderer',
    ),
    'DEFAULT_CONTENT_NEGOTIATION_CLASS': (
        'mkt.api.renderers.FirstAvailableRenderer'
    ),
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        # By default no-one gets anything. You will have to override this
        # in each resource to match your needs.
        'mkt.api.authorization.AllowNone',
    ),
    'DEFAULT_PAGINATION_SERIALIZER_CLASS':
        'mkt.api.paginator.CustomPaginationSerializer',
    'DEFAULT_FILTER_BACKENDS': (
        'rest_framework.filters.DjangoFilterBackend',
    ),
    'EXCEPTION_HANDLER': 'mkt.api.exceptions.custom_exception_handler',
    'PAGINATE_BY': 25,
    'PAGINATE_BY_PARAM': 'limit'
}

RTL_LANGUAGES = ('ar', 'fa', 'fa-IR', 'he')

# Until bug 753421 gets fixed, we're skipping ES tests. Sad times. I know.
# Flip this on in your local settings to experience the joy of ES tests.
RUN_ES_TESTS = False

# If this is False, tasks and other jobs that send non-critical emails should
# use a fake email backend.
SEND_REAL_EMAIL = False

SENTRY_DSN = None

# A database to be used by the services scripts, which does not use Django.
# The settings can be copied from DATABASES, but since its not a full Django
# database connection, only some values are supported.
SERVICES_DATABASE = {
    'NAME': 'zamboni',
    'USER': '',
    'PASSWORD': '',
    'HOST': '',
}

SHORTER_LANGUAGES = {'en': 'en-US', 'ga': 'ga-IE', 'pt': 'pt-PT',
                     'sv': 'sv-SE', 'zh': 'zh-CN'}

# This is the typ for signature checking JWTs.
# This is used to integrate with WebPay.
SIG_CHECK_TYP = 'mozilla/payments/sigcheck/v1'

# A seperate signing server for signing packaged apps. If not set, for example
# on local dev instances, the file will just be copied over unsigned.
SIGNED_APPS_SERVER_ACTIVE = False

# The reviewers equivalent to the above.
SIGNED_APPS_REVIEWER_SERVER_ACTIVE = False

# This is the signing REST server for signing apps.
SIGNED_APPS_SERVER = ''

# This is the signing REST server for signing apps with the reviewers cert.
SIGNED_APPS_REVIEWER_SERVER = ''

# And how long we'll give the server to respond.
SIGNED_APPS_SERVER_TIMEOUT = 10

# Send the more terse manifest signatures to the app signing server.
SIGNED_APPS_OMIT_PER_FILE_SIGS = True

# This is the signing REST server for signing receipts.
SIGNING_SERVER = ''

# Turn on/off the use of the signing server and all the related things. This
# is a temporary flag that we will remove.
SIGNING_SERVER_ACTIVE = False

# And how long we'll give the server to respond.
SIGNING_SERVER_TIMEOUT = 10

# The domains that we will accept certificate issuers for receipts.
SIGNING_VALID_ISSUERS = []

# Put the aliases for your slave databases in this list.
SLAVE_DATABASES = []

# The configuration for the client that speaks to solitude.
# A tuple of the solitude hosts.
SOLITUDE_HOSTS = ('',)

# The oAuth key and secret that solitude needs.
SOLITUDE_KEY = ''
SOLITUDE_SECRET = ''

# The timeout we'll give solitude.
SOLITUDE_TIMEOUT = 10

# The OAuth keys to connect to the solitude host specified above.
SOLITUDE_OAUTH = {'key': '', 'secret': ''}

# Full path or executable path (relative to $PATH) of the spidermonkey js
# binary.  It must be a version compatible with amo-validator
SPIDERMONKEY = None

# Tower
TEXT_DOMAIN = 'messages'
STANDALONE_DOMAINS = [TEXT_DOMAIN, 'javascript']

STATSD_HOST = 'localhost'
STATSD_PORT = 8125
STATSD_PREFIX = 'amo'

STATSD_RECORD_KEYS = [
    'window.performance.timing.domComplete',
    'window.performance.timing.domInteractive',
    'window.performance.timing.domLoading',
    'window.performance.timing.loadEventEnd',
    'window.performance.timing.responseStart',
    'window.performance.timing.fragment.loaded',
    'window.performance.navigation.redirectCount',
    'window.performance.navigation.type',
]

# The django statsd client to use, see django-statsd for more.
STATSD_CLIENT = 'django_statsd.clients.normal'

# Path to stylus (to compile .styl files).
STYLUS_BIN = 'stylus'
SYSLOG_TAG = "http_app_addons"
SYSLOG_TAG2 = "http_app_addons2"

# Default AMO user id to use for tasks.
TASK_USER_ID = 4757633

# These apps are only needed in a testing environment. They are added to
# INSTALLED_APPS by the RadicalTestSuiteRunnerWithExtraApps test runner.
TEST_INSTALLED_APPS = (
    'translations.tests.testapp',
)

# Tests
TEST_RUNNER = 'amo.runner.RadicalTestSuiteRunnerWithExtraApps'

TOTEM_BINARIES = {'thumbnailer': 'totem-video-thumbnailer',
                  'indexer': 'totem-video-indexer'}

TOWER_KEYWORDS = {
    '_lazy': None,
}
TOWER_ADD_HEADERS = True

# Path to uglifyjs (our JS minifier).
UGLIFY_BIN = 'uglifyjs'  # Set as None to use YUI instead (at your risk).

# Feature flags
UNLINK_SITE_STATS = True

# Allow URL style format override. eg. "?format=json"
URL_FORMAT_OVERRIDE = 'format'

USE_HEKA_FOR_CEF = False

VALIDATE_ADDONS = True

# URL for Add-on Validation FAQ.
VALIDATION_FAQ_URL = ('https://wiki.mozilla.org/AMO:Editors/EditorGuide/'
                      'AddonReviews#Step_2:_Automatic_validation')

# Allowed `installs_allowed_from` values for manifest validator.
VALIDATOR_IAF_URLS = ['https://marketplace.firefox.com']

# Max number of warnings/errors to show from validator. Set to None for no
# limit.
VALIDATOR_MESSAGE_LIMIT = 500

# Number of seconds before celery tasks will abort addon validation:
VALIDATOR_TIMEOUT = 110

VIDEO_LIBRARIES = ['lib.video.totem', 'lib.video.ffmpeg']

# Default app name for our webapp as specified in `manifest.webapp`.
WEBAPP_MANIFEST_NAME = 'Marketplace'

# Send a new receipt back when it expires.
WEBAPPS_RECEIPT_EXPIRED_SEND = False

# The expiry that we will add into the receipt.
# Set to 6 months for the next little while.
WEBAPPS_RECEIPT_EXPIRY_SECONDS = 60 * 60 * 24 * 182

# The key we'll use to sign webapp receipts.
WEBAPPS_RECEIPT_KEY = ''

# Whitelist IP addresses of the allowed clients that can post email
# through the API.
WHITELISTED_CLIENTS_EMAIL_API = []

# Set to True if we're allowed to use X-SENDFILE.
XSENDFILE = True
XSENDFILE_HEADER = 'X-SENDFILE'

# The UUID for Yogafire (Tarako Marketplace).
YOGAFIRE_GUID = 'f34d3c22-3efe-47ca-803d-6c740da1a851'
