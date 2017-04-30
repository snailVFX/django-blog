# -*- coding: utf-8 -*-
from django.db import models


class AuthorQuerySet(models.query.QuerySet):
    def delete(self, **kwargs):
        supers = kwargs.get('supers', False)
        if supers:
            data = super(AuthorQuerySet, self).delete(**kwargs)
        else:
            data = self.update(is_active=False)
        return data

    def undelete(self, **kwargs):
        data = self.update(is_active=True)
        return data


class ArticleQuerySet(models.query.QuerySet):
    def delete(self, **kwargs):
        supers = kwargs.get('supers', False)
        if supers:
            data = super(ArticleQuerySet, self).delete(**kwargs)
        else:
            data = self.update(is_active=False)
        return data

    def undelete(self, **kwargs):
        data = self.update(is_active=True)
        return data