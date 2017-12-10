# -*- coding: utf-8 -*-
from .dev import *  # noqa
import os

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'hcid_dev',
        'USER': 'knek',
        'PASSWORD': 'knek',
        'HOST': '127.0.0.1',
        'PORT': 5432
    }
}

GOOGLE_MAPS_API_KEY = ''


GEOS_LIBRARY_PATH='/usr/local/lib/libgeos_c.so.1'