# -*- coding: utf-8 -*-
from rest_framework import serializers


class DateField(serializers.DateField):
    """
    date格式
    """
    def to_representation(self, value):
        if value:
            return value.strftime('%F')


class DateTimeField(serializers.DateTimeField):
    """
    datetime格式
    """
    def to_representation(self, value):
        if value:
            return value.strftime('%F %H:%M')


class GetChoiceDisplayField(serializers.ChoiceField):
    """
    choice格式
    """
    def to_representation(self, value):
        return {
            'type': value,
            'name': self.choices[value]
            }


class UserField(serializers.RelatedField):
    """
    Model User
    """
    def to_representation(self, value):
        return {
            'id': value.id,
            'name': value.username
            }
