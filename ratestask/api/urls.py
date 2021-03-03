"""
"""
from django.urls import path
from .views import RateList


urlpatterns = [
    path('rates/', RateList.as_view(), name='rates'),
    path('rates_null/', RateList.as_view(null_rates=True),
         name='rates_null'),
]

