from django.urls import include, path
from django.conf.urls import url
from . import views

urlpatterns = [
    # url(r'counter/$', views.Counter.as_view()),
    url(r"$", views.FinancialList.as_view()),
    url(r"stocks", views.StocklList.as_view()),
    # url(r'$', views.CatalogRecordsView.as_view()),
]
