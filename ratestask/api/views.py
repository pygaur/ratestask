"""
"""
from django.db.models import Avg, Count
from django.db.models import Q

from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import RateSerializer
from core.models import Price


class RateList(APIView):
    """
    """
    def get(self, request, *args, **kwargs):
        """
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        serializer = RateSerializer(data=request.query_params)

        if serializer.is_valid():

            data = serializer.validated_data

            date_from = data['date_from']
            date_to = data['date_to']
            origin = data['origin']
            destination = data['destination']

            orig_code_lookup = Q(orig_code=origin) | Q(orig_code__region=origin)
            dest_code_lookup = Q(dest_code=destination) | Q(dest_code__region=destination)

            prices = Price.objects.\
                filter(orig_code_lookup, dest_code_lookup,
                       day__gte=date_from, day__lte=date_to)\
                .values('day',)\
                .annotate(total=Avg('price'),
                          #count=Count('price')
                          )\
                .order_by()

            return Response(prices)

        return Response(serializer.errors)

