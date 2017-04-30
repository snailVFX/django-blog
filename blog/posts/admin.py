# -*- coding: utf-8 -*-
from django.contrib import admin

from posts.models import (
    Author, Article, Tag, Category
)
# Register your models here.


class AuthorAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    list_filter = ('gender',)
    list_display = ('name', 'date_of_birth', 'gender', 'created_time',
                    'updated_time')


class ArticleAdmin(admin.ModelAdmin):
    search_fields = ('author__name',)
    list_filter = ('status', 'is_top',)
    list_display = ('author', 'title', 'status', 'created_time',
                    'updated_time', 'click_count', 'likes', 'is_top')


admin.site.register(Author, AuthorAdmin)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Tag)
admin.site.register(Category)
