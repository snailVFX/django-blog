# -*- coding: utf-8 -*-
from posts.models import Author, Article, Tag, Category
from posts.rest.serializers import (
    AuthorSerializer, ArticleSerializer, TagSerializer, CategorySerializer
)

from django.db import transaction
from django.db.models import Q
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly

# Create your views here.


class AuthorViewSet(viewsets.ModelViewSet):
    """
    作者 增删改查
    """
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def list(self, request):
        success = 1
        data = None
        msg = None
        try:
            search = request.GET.get('search', None)
            gender = request.GET.get('gender', None)
            search_q = Q()
            gender_q = Q()
            if search:
                search_q = Q(name__icontains=search)
            if gender == 'M':
                gender_q = Q(gender=Author.MALE)
            elif gender == 'F':
                gender_q = Q(gender=Author.FEMALE)
            queryset = self.queryset.filter(search_q, gender_q).distinct()
            serializer = self.get_serializer(queryset, many=True)
            data = serializer.data
        except Exception, e:
            success = 0
            msg = unicode(e)
        return Response({'success': success, 'data': data, 'msg': msg})

    def create(self, request):
        """
        {
            "name": 姓名,
            "date_of_birth": 出生日期(optional),
            "gender": 性别,
        }
        """
        success = 1
        data = None
        msg = None
        try:
            user = request.user
            req_data = request.data
            with transaction.atomic():
                req_data['creator'] = user.id
                serializer = self.get_serializer(data=req_data)
                if serializer.is_valid():
                    serializer.save()
                    data = serializer.data
                else:
                    msg = serializer.errors
        except Exception, e:
            success = 0
            msg = unicode(e)
            transaction.rollback()
        return Response({'success': success, 'data': data, 'msg': msg})

    def partial_update(self, request, pk=None):
        """
        {
            "name": 姓名,
            "date_of_birth": 出生日期(optional),
            "gender": 性别,
            "creator_id": 创建人
        }
        """
        success = 1
        data = None
        msg = None
        try:
            req_data = request.data
            with transaction.atomic():
                author = Author.objects.get(id=pk)
                if 'creator_id' in req_data.keys():
                    req_data['creator'] = req_data['creator_id']
                serializer = self.get_serializer(author,
                                                 data=req_data,
                                                 partial=True)
                if serializer.is_valid():
                    serializer.save()
                    data = serializer.data
                else:
                    msg = serializer.errors
        except Exception, e:
            success = 0
            msg = unicode(e)
            transaction.rollback()
        return Response({'success': success, 'data': data, 'msg': msg})

    def retrieve(self, request, pk=None):
        success = 1
        data = None
        msg = None
        try:
            author = Author.objects.get(id=pk)
            serializer = self.get_serializer(author)
            data = serializer.data
        except Exception, e:
            success = 0
            msg = unicode(e)
        return Response({'success': success, 'data': data, 'msg': msg})

    def destroy(self, request, pk=None):
        success = 1
        data = None
        msg = None
        try:
            author = Author.objects.get(id=pk)
            author.is_active = False
            author.save()
        except Exception, e:
            success = 0
            msg = unicode(e)
        return Response({'success': success, 'data': data, 'msg': msg})


class ArticleViewSet(viewsets.ModelViewSet):
    """
    文章 增删改查
    """
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def list(self, request):
        success = 1
        data = None
        msg = None
        try:
            search = request.GET.get('search', None)
            ordering = request.GET.get('ordering', None)
            search_q = Q()
            if search:
                search_q = Q(Q(title__icontains=search)
                             | Q(tag__name__icontains=search)
                             | Q(category__name__icontains=search))
            queryset = self.queryset.filter(search_q).distinct()
            # likes click_count 排序
            if ordering:
                queryset = queryset.order_by('-%s' % ordering)
            else:
                queryset = queryset.order_by('-is_top', '-created_time')
            serializer = self.get_serializer(queryset, many=True)
            data = serializer.data
        except Exception, e:
            success = 0
            msg = unicode(e)
        return Response({'success': success, 'data': data, 'msg': msg})

    def create(self, request):
        """
        {
            "author_id": 作者id,
            "title": 标题,
            "abstract": 摘要(optional),
            "status": 状态,
            "content": 内容,
            "tag_id":[标签id],
            "category_id": [分类id],
            "click_count": 点击次数,
            "likes": 点赞数,
            "is_top": 是否置顶
        }
        """
        success = 1
        data = None
        msg = None
        try:
            req_data = request.data
            with transaction.atomic():
                article = Article()
                for key, value in req_data.iteritems():
                    setattr(article, key, value)
                if 'abstract' not in req_data.keys():
                    setattr(article, 'abstract', req_data['content'][:70])
                article.save()
                # 多对多关系 Tag
                if 'tag_id' in req_data.keys():
                    for tag_id in req_data['tag_id']:
                        article.tag.add(tag_id)
                # 多对多关系 Category
                if 'category_id' in req_data.keys():
                    for category_id in req_data['category_id']:
                        article.category.add(category_id)
                serializer = self.get_serializer(article)
                data = serializer.data
        except Exception, e:
            success = 0
            msg = unicode(e)
            transaction.rollback()
        return Response({'success': success, 'data': data, 'msg': msg})

    def partial_update(self, request, pk=None):
        """
        {
            "author_id": 作者id,
            "title": 标题,
            "abstract": 摘要(optional),
            "status": 状态,
            "content": 内容,
            "tag_id":[标签id],
            "category_id": [分类id],
            "click_count": 点击次数,
            "likes": 点赞数,
            "is_top": 是否置顶
        }
        """
        success = 1
        data = None
        msg = None
        try:
            req_data = request.data
            with transaction.atomic():
                article = Article.objects.get(id=pk)
                for key, value in req_data.iteritems():
                    setattr(article, key, value)
                article.save()
                # 多对多关系 Tag
                if 'tag_id' in req_data.keys():
                    article.tag.clear()
                    for tag_id in req_data['tag_id']:
                        article.tag.add(tag_id)
                # 多对多关系 Category
                if 'category_id' in req_data.keys():
                    article.category.clear()
                    for category_id in req_data['category_id']:
                        article.category.add(category_id)
                serializer = self.get_serializer(article)
                data = serializer.data
        except Exception, e:
            success = 0
            msg = unicode(e)
            transaction.rollback()
        return Response({'success': success, 'data': data, 'msg': msg})

    def retrieve(self, request, pk=None):
        success = 1
        data = None
        msg = None
        try:
            article = Article.objects.get(id=pk)
            serializer = self.get_serializer(article)
            data = serializer.data
        except Exception, e:
            success = 0
            msg = unicode(e)
        return Response({'success': success, 'data': data, 'msg': msg})

    def destroy(self, request, pk=None):
        success = 1
        data = None
        msg = None
        try:
            article = Article.objects.get(id=pk)
            article.is_active = False
            article.save()
        except Exception, e:
            success = 0
            msg = unicode(e)
        return Response({'success': success, 'data': data, 'msg': msg})


class TagViewSet(viewsets.ModelViewSet):
    """
    标签 增删改查
    """
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def list(self, request):
        success = 1
        data = None
        msg = None
        try:
            search = request.GET.get('search', None)
            search_q = Q()
            if search:
                search_q = Q(name__icontains=search)
            queryset = self.queryset.filter(search_q).distinct()
            serializer = self.get_serializer(queryset, many=True)
            data = serializer.data
        except Exception, e:
            success = 0
            msg = unicode(e)
        return Response({'success': success, 'data': data, 'msg': msg})

    def create(self, request):
        """
        {
            "name": 名称
        }
        """
        success = 1
        data = None
        msg = None
        try:
            req_data = request.data
            with transaction.atomic():
                serializer = self.get_serializer(data=req_data)
                if serializer.is_valid():
                    serializer.save()
                    data = serializer.data
                else:
                    msg = serializer.errors
        except Exception, e:
            success = 0
            msg = unicode(e)
            transaction.rollback()
        return Response({'success': success, 'data': data, 'msg': msg})

    def partial_update(self, request, pk=None):
        """
        {
            "name": 名称
        }
        """
        success = 1
        data = None
        msg = None
        try:
            req_data = request.data
            with transaction.atomic():
                tag = Tag.objects.get(id=pk)
                serializer = self.get_serializer(tag,
                                                 data=req_data,
                                                 partial=True)
                if serializer.is_valid():
                    serializer.save()
                    data = serializer.data
                else:
                    msg = serializer.errors
        except Exception, e:
            success = 0
            msg = unicode(e)
            transaction.rollback()
        return Response({'success': success, 'data': data, 'msg': msg})

    def retrieve(self, request, pk=None):
        success = 1
        data = None
        msg = None
        try:
            tag = Tag.objects.get(id=pk)
            serializer = self.get_serializer(tag)
            data = serializer.data
        except Exception, e:
            success = 0
            msg = unicode(e)
        return Response({'success': success, 'data': data, 'msg': msg})

    def destroy(self, request, pk=None):
        success = 1
        data = None
        msg = None
        try:
            tag = Tag.objects.get(id=pk)
            tag.delete()
        except Exception, e:
            success = 0
            msg = unicode(e)
        return Response({'success': success, 'data': data, 'msg': msg})


class CategoryViewSet(viewsets.ModelViewSet):
    """
    分类 增删改查
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def list(self, request):
        success = 1
        data = None
        msg = None
        try:
            search = request.GET.get('search', None)
            search_q = Q()
            if search:
                search_q = Q(name__icontains=search)
            queryset = self.queryset.filter(search_q).distinct()
            serializer = self.get_serializer(queryset, many=True)
            data = serializer.data
        except Exception, e:
            success = 0
            msg = unicode(e)
        return Response({'success': success, 'data': data, 'msg': msg})

    def create(self, request):
        """
        {
            "name": 名称
        }
        """
        success = 1
        data = None
        msg = None
        try:
            req_data = request.data
            with transaction.atomic():
                serializer = self.get_serializer(data=req_data)
                if serializer.is_valid():
                    serializer.save()
                    data = serializer.data
                else:
                    msg = serializer.errors
        except Exception, e:
            success = 0
            msg = unicode(e)
            transaction.rollback()
        return Response({'success': success, 'data': data, 'msg': msg})

    def partial_update(self, request, pk=None):
        """
        {
            "name": 名称
        }
        """
        success = 1
        data = None
        msg = None
        try:
            req_data = request.data
            with transaction.atomic():
                category = Category.objects.get(id=pk)
                serializer = self.get_serializer(category,
                                                 data=req_data,
                                                 partial=True)
                if serializer.is_valid():
                    serializer.save()
                    data = serializer.data
                else:
                    msg = serializer.errors
        except Exception, e:
            success = 0
            msg = unicode(e)
            transaction.rollback()
        return Response({'success': success, 'data': data, 'msg': msg})

    def retrieve(self, request, pk=None):
        success = 1
        data = None
        msg = None
        try:
            category = Category.objects.get(id=pk)
            serializer = self.get_serializer(category)
            data = serializer.data
        except Exception, e:
            success = 0
            msg = unicode(e)
        return Response({'success': success, 'data': data, 'msg': msg})

    def destroy(self, request, pk=None):
        success = 1
        data = None
        msg = None
        try:
            category = Category.objects.get(id=pk)
            category.delete()
        except Exception, e:
            success = 0
            msg = unicode(e)
        return Response({'success': success, 'data': data, 'msg': msg})
