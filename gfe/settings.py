"""
Django settings for gfe project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import sys

PROJECT_ROOT = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(PROJECT_ROOT, '../Spirit'))

from spirit.settings import *
from settings_local import *
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Application definition

INSTALLED_APPS = ('django.contrib.sites', 'sorl.thumbnail', 'django_extensions', 'server', 'member', 'page', 'pipeline', 'newsletter', 'oauth2_provider', 'corsheaders') + INSTALLED_APPS

MIDDLEWARE_CLASSES = ('corsheaders.middleware.CorsMiddleware','oauth2_provider.middleware.OAuth2TokenMiddleware') + MIDDLEWARE_CLASSES

AUTHENTICATION_BACKENDS =('oauth2_provider.backends.OAuth2Backend',) + AUTHENTICATION_BACKENDS

TEMPLATE_CONTEXT_PROCESSORS += ("server.context.context",)

ROOT_URLCONF = 'gfe.urls'

WSGI_APPLICATION = 'gfe.wsgi.application'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

AUTH_USER_MODEL = "member.Member"

STATICFILES_STORAGE = 'pipeline.storage.PipelineCachedStorage'

PIPELINE_JS = {
	'main': {
		'source_filenames': ("servers/js/jquery.min.js",
		'servers/js/bootstrap.min.js',
		'servers/js/jquery.cookie.js',
		'spirit/scripts/vendors/highlightjs/highlight.min.js',
		'spirit/scripts/util.js',
		'spirit/scripts/tab.js',
		'spirit/scripts/postify.js',
		'spirit/scripts/social_share.js',
		'spirit/scripts/vendors/atwho/jquery.caret.min.js', # if logged in
		'spirit/scripts/vendors/atwho/jquery.atwho.min.js',
		'spirit/scripts/vendors/marked/marked.min.js',
		'spirit/scripts/vendors/waypoints/waypoints.min.js'
		'spirit/scripts/store.js',
		'spirit/scripts/editor_image_upload.js',
		'spirit/scripts/editor.js',
		'spirit/scripts/emoji_list.js',
		'spirit/scripts/like.js',
		'spirit/scripts/bookmark.js',
		'spirit/scripts/notification.js',
		'spirit/scripts/move_comments.js',
		'servers/js/docs.min.js',), #if is moderator
		'output_filename': 'js/main.js'
	}
}

PIPELINE_CSS = {
	'main': {
		'source_filenames': ('servers/css/bootstrap.min.css',
			'servers/css/dashboard.css',
			'spirit/stylesheets/vendors/font-awesome.min.css',
			'spirit/stylesheets/vendors/github.min.css',
			'spirit/stylesheets/vendors/jquery.atwho.min.css',
			'spirit/stylesheets/styles.css'
			),
		'output_filename': 'css/main.css'
	}
}

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'pipeline.finders.PipelineFinder',
)

PIPELINE_YUGLIFY_BINARY = "/usr/bin/env yuglify"
PIPELINE_DISABLE_WRAPPER = True
PIPELINE_CSS_COMPRESSOR = 'pipeline.compressors.NoopCompressor'
PIPELINE_JS_COMPRESSOR = 'pipeline.compressors.NoopCompressor'

SITE_ID = 1
TIMEZONE = 'Europe/Stockholm'

CORS_ORIGIN_ALLOW_ALL = True
