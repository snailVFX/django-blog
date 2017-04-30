# -*- coding: utf-8 -*-
from rest_framework import serializers

from posts.models import Author, Article, Tag, Category
from apis.rest.serializers import (
    DateTimeField, GetChoiceDisplayField, UserField
)


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name')


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name')


class AuthorSerializer(serializers.ModelSerializer):
    created_time = DateTimeField(read_only=True)
    updated_time = DateTimeField(read_only=True)
    gender = GetChoiceDisplayField(Author.GENDER_CHOICES)
    creator = UserField(read_only=True)

    class Meta:
        model = Author
        fields = ('id', 'name', 'date_of_birth', 'gender', 'creator',
                  'created_time', 'updated_time')


class ArticleSerializer(serializers.ModelSerializer):
    created_time = DateTimeField(read_only=True)
    updated_time = DateTimeField(read_only=True)
    author = AuthorSerializer()
    tag = TagSerializer(many=True)
    category = CategorySerializer(many=True)
    status = GetChoiceDisplayField(Article.STATUS_CHOICES, required=False)

    class Meta:
        model = Article
        fields = ('id', 'author', 'title', 'abstract', 'status', 'content',
                  'tag', 'category', 'created_time', 'updated_time',
                  'click_count', 'likes', 'is_top')
