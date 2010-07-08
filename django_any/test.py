# -*- coding: utf-8 -*-
from django import forms
from django_any import any_form
from django.test.client import Client as DjangoClient
from django_any.contrib.auth import any_user
from django_any import xunit


class Client(DjangoClient):
    def login_as(self, **kwargs):
        password = xunit.any_string()
        user = any_user(password=password, **kwargs)
        
        if self.login(username=user.username, password=password):
            return user
        raise AssertionError('Can''t login with autogenerated user')

    def post_any_data(self, url, extra=None, **kwargs):
        request = self.get(url)

        post_data = {}

        for context in request.context.dicts:
            for _, inst in context.items():
                if isinstance(inst, forms.Form):
                    form_data, form_files = any_form(inst.__class__) #TODO support form instance
                    post_data.update(form_data) #TODO support form prefix

        if extra:
            post_data.update(extra)

        return self.post(url, post_data)

