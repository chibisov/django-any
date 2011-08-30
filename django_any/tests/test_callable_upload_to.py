# -*- coding: utf-8; mode: django -*-
from django.db import models
from django.test import TestCase
from django_any import any_model

def upload_to_generator(some_param):
    return lambda: some_param

class Man(models.Model):
    photo = models.FileField(upload_to=upload_to_generator("django_any"))

    class Meta:
        app_label = 'django_any'

class TestUploadTo(TestCase):
    def test_callable_upload_to(self):
        man = any_model(Man)
        self.assertTrue(bool(man.photo))