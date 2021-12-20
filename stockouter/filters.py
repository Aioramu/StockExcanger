import django_filters
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Max,Min
from .models import *

class FinanceFilter(django_filters.FilterSet):
    min_price = django_filters.NumberFilter(field_name="stock__price", lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name="stock__price", lookup_expr='lte')
    pe = django_filters.NumberFilter(field_name="stock__pe", lookup_expr='lte')
    ps = django_filters.NumberFilter(field_name="stock__ps", lookup_expr='lte')
    pb = django_filters.NumberFilter(field_name="stock__pb", lookup_expr='lte')
    ebitda = django_filters.NumberFilter(field_name="stock__ebitda", lookup_expr='lte')
    env = django_filters.NumberFilter(field_name="stock__env", lookup_expr='lte')
    net_worth = django_filters.NumberFilter(field_name="stock__net_worth", lookup_expr='lte')
    roe = django_filters.NumberFilter(field_name="stock__roe", lookup_expr='lte')
    debt_eq = django_filters.NumberFilter(field_name="stock__debt_eq", lookup_expr='lte')
    roa = django_filters.NumberFilter(field_name="stock__roa", lookup_expr='lte')
    roi = django_filters.NumberFilter(field_name="stock__roi", lookup_expr='lte')
    last_divident = django_filters.NumberFilter(field_name="stock__last_divident", lookup_expr='lte')
    ticket=django_filters.CharFilter(field_name="stock__ticket")
    name=django_filters.CharFilter(field_name="stock__name")
    order_by = django_filters.OrderingFilter(
    fields=(('price', 'stock__price'),('pe','stock__pe')),
    field_labels={
            'stock__price': 'Цена по убыванию','-price':'Цена по возрастанию','stock__pe':'Год от старых к новым',
            '-pe':'Год от новых к старым','stock__ps':'Пробег от меньшего','-ps':'Пробег от большего'
        })
    class Meta:
        model = Financial
        fields = ['debt','stock','net_income','income_after_taxes','gross_profit','revenue',
        'last_divident','roi','roa','debt_eq','roe','net_worth','env','ebitda','pb','ps',
        'pe','min_price','max_price','name','ticket']
