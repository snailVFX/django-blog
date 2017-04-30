# -*- coding: utf-8 -*-
from django.db import models

from posts.querysets import AuthorQuerySet, ArticleQuerySet


class AuthorManager(models.Manager):
    def get_queryset(self, supers=False, *args, **kwargs):
        if supers:
            return AuthorQuerySet(self.model, using=self._db)
        else:
            return AuthorQuerySet(self.model, using=self._db).filter(
                is_active=True)


class ArticleManager(models.Manager):
    def get_queryset(self, supers=False, *args, **kwargs):
        if supers:
            return ArticleQuerySet(self.model, using=self._db)
        else:
            return ArticleQuerySet(self.model, using=self._db).filter(
                is_active=True, author__is_active=True)
