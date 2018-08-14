# -*- coding: utf-8 -*-

# https://simpleisbetterthancomplex.com/tutorial/2016/08/01/how-to-upload-files-with-django.html

from __future__ import absolute_import, division, print_function, unicode_literals

from django.contrib.gis.db import models
from django.contrib.postgres.fields import JSONField


class Task(models.Model):
    uploaded_at = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to='uploads/%Y/%m/%d/')
    webuser = models.ForeignKey('webusers.WebUser', on_delete=models.DO_NOTHING)


class TaskHistory(models.Model):
    STATE_UPLOADED = 'u'
    STATE_INSERTED = 'i'
    STATE_NONE = 'n'

    STATE_CHOICES = ((STATE_UPLOADED, 'Uploaded and analysed'),
                     (STATE_INSERTED, 'Inserted in database'),
                     (STATE_NONE, 'None'))

    changed_at = models.DateTimeField(auto_now_add=True)
    old_state = models.CharField(max_length=2, choices=STATE_CHOICES, default='n')
    new_state = models.CharField(max_length=2, choices=STATE_CHOICES)
    file_name = models.CharField(max_length=200)
    webuser = models.ForeignKey('webusers.WebUser', on_delete=models.DO_NOTHING)
    error_msgs = models.TextField(default='none')
    warning_msgs = models.TextField(default='none')
    report_dict = JSONField()
    task = models.ForeignKey(Task, on_delete=models.DO_NOTHING)
