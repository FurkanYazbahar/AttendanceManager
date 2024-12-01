from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

class DataTablePagination(PageNumberPagination):
    page_size = 10

    def get_paginated_response(self, data):
        return Response({
            'draw': int(self.request.GET.get('draw', 0)),
            'recordsTotal': self.page.paginator.count,
            'recordsFiltered': self.page.paginator.count,
            'data': data
        })