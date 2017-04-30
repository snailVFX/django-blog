# -*- encoding: utf-8 -*-
# from django.conf.urls import url

from rest_framework.routers import DefaultRouter

from posts.rest.views import (
    AuthorViewSet, ArticleViewSet, TagViewSet, CategoryViewSet
)

router = DefaultRouter()
router.register(r'authors', AuthorViewSet)
router.register(r'articles', ArticleViewSet)
router.register(r'tags', TagViewSet)
router.register(r'categories', CategoryViewSet)


urlpatterns = [
]


urlpatterns += router.urls
