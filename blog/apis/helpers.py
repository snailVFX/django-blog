# -*- coding: utf-8 -*-
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination


class CustomPagination(PageNumberPagination):
    page_size = 10
    max_page_size = 100
    page_size_query_param = 'page_size'

    def get_paginated_response(self, data):
        data['paging'] = {
           'next': None,
           'previous': None,
           'count': None
        }
        if data['msg'] is None:
            paging = data['paging']
            paging['next'] = self.get_next_link()
            paging['previous'] = self.get_previous_link()
            paging['count'] = self.page.paginator.count
        return Response(data)
