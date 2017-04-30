# -*- encoding: utf-8 -*-
from django.conf.urls import url, include


urlpatterns = [
    url(r'^posts/', include('posts.rest.urls')),
]