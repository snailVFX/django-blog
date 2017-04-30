# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-29 18:31
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30, unique=True, verbose_name='\u6807\u9898')),
                ('abstract', models.CharField(blank=True, help_text='\u53ef\u9009\uff0c\u5982\u82e5\u4e3a\u7a7a\u5c06\u6458\u53d6\u6b63\u6587\u7684\u524d70\u4e2a\u5b57\u7b26', max_length=70, null=True, verbose_name='\u6458\u8981')),
                ('status', models.CharField(choices=[('D', '\u8349\u7a3f'), ('P', '\u53d1\u5e03')], default='D', max_length=1, verbose_name='\u72b6\u6001')),
                ('content', models.TextField(max_length=10000, verbose_name='\u5185\u5bb9')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='\u521b\u5efa\u65f6\u95f4')),
                ('updated_time', models.DateTimeField(auto_now=True, verbose_name='\u66f4\u65b0\u65f6\u95f4')),
                ('click_count', models.PositiveIntegerField(default=0, verbose_name='\u70b9\u51fb\u6b21\u6570')),
                ('likes', models.PositiveIntegerField(default=0, verbose_name='\u70b9\u8d5e\u6570')),
                ('is_top', models.BooleanField(default=False, verbose_name='\u662f\u5426\u7f6e\u9876')),
                ('is_active', models.BooleanField(default=True, verbose_name='\u662f\u5426\u53ef\u7528')),
            ],
            options={
                'ordering': ('-created_time', '-updated_time'),
                'verbose_name': '\u6587\u7ae0',
                'verbose_name_plural': '\u6587\u7ae0',
            },
        ),
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, verbose_name='\u59d3\u540d')),
                ('date_of_birth', models.DateField(blank=True, null=True, verbose_name='\u51fa\u751f\u65e5\u671f')),
                ('gender', models.CharField(choices=[('M', '\u7537\u6027'), ('F', '\u5973\u6027')], default='M', max_length=1, verbose_name='\u6027\u522b')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='\u521b\u5efa\u65f6\u95f4')),
                ('updated_time', models.DateTimeField(auto_now=True, verbose_name='\u66f4\u65b0\u65f6\u95f4')),
                ('is_active', models.BooleanField(default=True, verbose_name='\u662f\u5426\u53ef\u7528')),
                ('creator', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='\u521b\u5efa\u4eba')),
            ],
            options={
                'ordering': ('name',),
                'verbose_name': '\u4f5c\u8005',
                'verbose_name_plural': '\u4f5c\u8005',
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, unique=True, verbose_name='\u540d\u79f0')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='\u521b\u5efa\u65f6\u95f4')),
                ('updated_time', models.DateTimeField(auto_now=True, verbose_name='\u66f4\u65b0\u65f6\u95f4')),
            ],
            options={
                'verbose_name': '\u5206\u7c7b',
                'verbose_name_plural': '\u5206\u7c7b',
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, unique=True, verbose_name='\u540d\u79f0')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='\u521b\u5efa\u65f6\u95f4')),
                ('updated_time', models.DateTimeField(auto_now=True, verbose_name='\u66f4\u65b0\u65f6\u95f4')),
            ],
            options={
                'verbose_name': '\u6807\u7b7e',
                'verbose_name_plural': '\u6807\u7b7e',
            },
        ),
        migrations.AddField(
            model_name='article',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='article', to='posts.Author', verbose_name='\u4f5c\u8005'),
        ),
        migrations.AddField(
            model_name='article',
            name='category',
            field=models.ManyToManyField(related_name='article', to='posts.Category', verbose_name='\u5206\u7c7b'),
        ),
        migrations.AddField(
            model_name='article',
            name='tag',
            field=models.ManyToManyField(related_name='article', to='posts.Tag', verbose_name='\u6807\u7b7e'),
        ),
    ]
