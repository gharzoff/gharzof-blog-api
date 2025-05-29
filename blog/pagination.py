# pagination.py

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
import math

class CustomPagination(PageNumberPagination):
    page_size = 6

    def get_paginated_response(self, data):
        total_items = self.page.paginator.count
        page_size = self.page_size
        current_page = self.page.number
        total_pages = math.ceil(total_items / page_size)

        return Response({
            'count': total_items,
            'current_page': current_page,
            'total_pages': total_pages,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data,
        })
