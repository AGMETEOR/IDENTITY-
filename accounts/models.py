# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.conf import settings

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    phone_number= models.CharField(max_length=255)
    location = models.CharField(max_length=255)

    def __str__(self):
        return 'Details for user {}'.format(self.user.username)

