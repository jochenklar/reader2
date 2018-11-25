from rest_framework import pagination


class PageNumberPagination(pagination.PageNumberPagination):
    page_size = 30
    page_size_query_param = 'page_size'
