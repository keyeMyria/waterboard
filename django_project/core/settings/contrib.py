# -*- coding: utf-8 -*-
from .base import *  # noqa
import os


# Extra installed apps
INSTALLED_APPS += (
    'raven.contrib.django.raven_compat',  # enable Raven plugin
    'rest_framework',
    'pipeline',
    'celery',
    'sms'
)


MIDDLEWARE_CLASSES += (
    'django.middleware.gzip.GZipMiddleware',
)
TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.request',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.media',
)

LEAFLET_CONFIG = {
    'TILES': [
        (
            'OpenStreetMap',
            'http://{s}.tile.openstreetmap.fr/hot/{z}/{x}/{y}.png',
            ('© <a href="http://www.openstreetmap.org" '
             'target="_parent">OpenStreetMap</a> and contributors, under an '
             '<a href="http://www.openstreetmap.org/copyright" '
             'target="_parent">open license</a>')
        )]

}

# enable cached storage - requires uglify.js (node.js)
STATICFILES_STORAGE = 'pipeline.storage.PipelineCachedStorage'
PIPELINE_JS = {
    'contrib': {
        'source_filenames': (
            'js/jquery-1.11.2.js',
            'js/bootstrap.js',
            'js/moment.js',
            'event_mapper/js/bootstrap-datetimepicker.js',
            'js/csrf-ajax.js'
        ),
        'output_filename': 'js/contrib.js',
        },
    'event_mapper_js': {
        'source_filenames': (
            'event_mapper/js/leaflet.js',
            'event_mapper/js/material.js',
            'event_mapper/js/ripples.js',
            'event_mapper/js/jquery.flot.min.js',
            'event_mapper/js/jquery.flot.time.min.js',
            'event_mapper/js/jquery-ui.js',
            'event_mapper/js/bootstrap-multiselect.js',
            'event_mapper/js/Chart.js',
            'event_mapper/js/leaflet.draw.js',
            'event_mapper/js/event_mapper.js',
            'event_mapper/js/add_event.js',
            'event_mapper/js/update_movement.js',
            'event_mapper/js/event_dashboard.js',
        ),
        'output_filename': 'js/event_mapper_js.js'
    }
}

PIPELINE_CSS = {
    'contrib': {
        'source_filenames': (
            'css/bootstrap.css',
            'event_mapper/css/bootstrap-datetimepicker.css',
        ),
        'output_filename': 'css/contrib.css',
        'extra_context': {
            'media': 'screen, projection',
            }
    },
    'event_mapper_css': {
        'source_filenames': (
            'event_mapper/css/leaflet.css',
            'event_mapper/css/material-wfont.min.css',
            'event_mapper/css/ripples.min.css',
            'event_mapper/css/bootstrap-multiselect.css',
            'event_mapper/css/jquery-ui.css',
            'event_mapper/css/leaflet.draw.css',
            'event_mapper/css/event_mapper.css',
        ),
        'output_filename': 'css/event_mapper_css.css',
    }
}
#
# RABBIT_HOSTNAME = os.environ.get('RABBITMQ_PORT_5672_TCP', 'localhost:5672')
# if RABBIT_HOSTNAME.startswith('tcp://'):
#     RABBIT_HOSTNAME = RABBIT_HOSTNAME.split('//')[1]

# BROKER_URL = 'amqp://%s:%s@%s//' % (
#     'admin',  # os.environ['RABBIT_ENV_USER'],
#     'BU9QWf0P5nsR',  # os.environ['RABBITMQ_ENV_RABBIT_PASSWORD'],
#     RABBIT_HOSTNAME)

# We don't want to have dead connections stored on rabbitmq
# BROKER_HEARTBEAT = '?heartbeat=30'
# BROKER_URL += BROKER_HEARTBEAT

BROKER_URL = 'amqp://guest:guest@%s:5672//' % os.environ.get('RABBITMQ_HOST', 'rabbitmq')

CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
