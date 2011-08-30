# -*- coding: utf-8; mode: django -*-
from django.db import models
from django.test import TestCase
from django_any import any_model

def upload_to_generator_with_params(some_param):
    def create_file_upload_path(instance, filename):
        return file_name

    create_file_upload_path.folder_path_for_django_any = "./"
    return create_file_upload_path

class Woman(models.Model):
    photo = models.FileField(upload_to=upload_to_generator_with_params("django_any"))

    class Meta:
        app_label = 'django_any'

class TestUploadTo(TestCase):
    def test_callable_upload_to_with_params(self):
        woman = any_model(Woman)

        self.assertTrue(bool(woman.photo))

