"""
"""
from django.urls import path, include
from .views import RateList


urlpatterns = [
    path('rates/', RateList.as_view(), name='rate'),
]

