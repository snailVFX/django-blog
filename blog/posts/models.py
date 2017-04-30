# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from posts.managers import AuthorManager, ArticleManager


# Create your models here.
class Author(models.Model):
    """
    author: chen
    create_date: 2017/03/26
    """
    MALE = 'M'
    FEMALE = 'F'

    GENDER_CHOICES = (
        (MALE, u'男性'),
        (FEMALE, u'女性')
    )
    name = models.CharField(max_length=20, verbose_name=u'姓名')
    date_of_birth = models.DateField(blank=True, null=True, verbose_name=u'出生日期')
    gender = models.CharField(
        max_length=1, choices=GENDER_CHOICES, default=MALE, verbose_name=u'性别')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name=u'创建时间')
    updated_time = models.DateTimeField(auto_now=True, verbose_name=u'更新时间')
    creator = models.OneToOneField(settings.AUTH_USER_MODEL, verbose_name=u'创建人')
    is_active = models.BooleanField(default=True, verbose_name=u'是否可用')

    objects = AuthorManager()

    def delete(self, supers=False):
        if not supers:
            self.is_active = supers
            self.save()
        else:
            super(Author, self).delete()

    def undelete(self):
        self.is_active = True
        self.save()

    def __unicode__(self):
        return u'%s' % self.name

    class Meta:
        verbose_name = u'作者'
        verbose_name_plural = u'作者'
        ordering = ('name',)


class Article(models.Model):
    """
    author: chen
    create_date: 2017/03/26
    """
    DRAFT = "D"
    PUBLISHED = "P"

    STATUS_CHOICES = (
        (DRAFT, u'草稿'),
        (PUBLISHED, u'发布')
    )

    author = models.ForeignKey(Author, related_name='article', verbose_name=u'作者')
    title = models.CharField(max_length=30, unique=True, verbose_name=u'标题')
    # help_text 在该 field 被渲染成 form 是显示帮助信息
    abstract = models.CharField(
        max_length=70, blank=True, null=True,
        help_text="可选，如若为空将摘取正文的前70个字符", verbose_name=u'摘要')
    status = models.CharField(
        max_length=1, choices=STATUS_CHOICES, default=DRAFT, verbose_name=u'状态')
    content = models.TextField(max_length=10000, verbose_name=u'内容')
    tag = models.ManyToManyField('Tag', related_name='article', verbose_name=u'标签')
    category = models.ManyToManyField('Category', related_name='article', verbose_name=u'分类')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name=u'创建时间')
    updated_time = models.DateTimeField(auto_now=True, verbose_name=u'更新时间')
    # PositiveIntegerField存储非负整数
    click_count = models.PositiveIntegerField(default=0, verbose_name='点击次数')
    likes = models.PositiveIntegerField(default=0, verbose_name='点赞数')
    is_top = models.BooleanField(default=False, verbose_name='是否置顶')
    is_active = models.BooleanField(default=True, verbose_name=u'是否可用')

    objects = ArticleManager()

    def delete(self, supers=False):
        if not supers:
            self.is_active = supers
            self.save()
        else:
            super(Article, self).delete()

    def undelete(self):
        self.is_active = True
        self.save()

    def update_click_count(self):
        """更新点击次数
        """
        self.click_count += 1
        self.save()

    def update_likes(self):
        """更新点赞数
        """
        self.likes += 1
        self.save()

    def __unicode__(self):
        return u'%s %s' % (self.title, self.get_status_display())

    class Meta:
        verbose_name = u'文章'
        verbose_name_plural = u'文章'
        ordering = ('-created_time', '-updated_time')


class Tag(models.Model):
    """
    author: chen
    create_date: 2017/03/26
    """
    name = models.CharField(max_length=30, unique=True, verbose_name=u'名称')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name=u'创建时间')
    updated_time = models.DateTimeField(auto_now=True, verbose_name=u'更新时间')

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u'标签'
        verbose_name_plural = u'标签'


class Category(models.Model):
    """
    author: chen
    create_date: 2017/03/26
    """
    name = models.CharField(max_length=30, unique=True, verbose_name=u'名称')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name=u'创建时间')
    updated_time = models.DateTimeField(auto_now=True, verbose_name=u'更新时间')

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u'分类'
        verbose_name_plural = u'分类'
