"""
"""
import logging
from datetime import datetime

from django.db import connection

from api.serializers import RateListSerializer,\
    RateCreateSerializer
from api.query import rate_list_query, port_check_query, price_insert_query
from core.utils import exchange_rates

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

import pandas as pd

logger = logging.getLogger(__name__)


class RateList(APIView):
    """
    """
    null_rates = False

    def post(self, request, *args, **kwargs):
        """
        Implement an API endpoint where you can upload a price,
        including the following parameters:
            date_from
            date_to
            origin_code,
            destination_code
            price
            currency_code  ( OPTIONAL)
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        serializer = RateCreateSerializer(data=request.data)
        if not serializer.is_valid():
            response = {'error_message': serializer.errors}
            return Response(response,
                            status=status.HTTP_400_BAD_REQUEST)

        data = serializer.data

        date_from = data['date_from']
        date_to = data['date_to']
        prices = data['prices']
        origin_code = data['origin_code']
        destination_code = data['destination_code']

        currency_code = data.get('currency_code')

        if date_from != date_to:
            date_range = pd.date_range(start=date_from,
                                       end=date_to).date.tolist()
        else:
            date_range = [datetime.strptime(date_to, "%Y-%m-%d")]

        if len(date_range) != len(prices):
            response = {'error_message': "price and generated date"
                                         "length does not match."}
            return Response(response,
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            with connection.cursor() as cursor:
                cursor.execute(port_check_query, (origin_code, destination_code))
                result = cursor.fetchall()
                if len(result) != 2:
                    response = {"error_message": "One of the port does not exist."}
                    return Response(response, status=status.HTTP_400_BAD_REQUEST)

                for day, price in zip(date_range, prices):
                    if currency_code:
                        price = exchange_rates(price, currency_code)
                    cursor.execute(price_insert_query,
                                   (origin_code, destination_code, day, price))
                return Response("Successful data upload.",
                                status=status.HTTP_201_CREATED)
        except Exception as exc:
            logger.error(str(exc))
            response = {"error_message": "Failed data upload."}
            return Response(response, status.HTTP_422_UNPROCESSABLE_ENTITY)

    @staticmethod
    def filtered_result(result, null_rates):
        """
        :param result:
        :param null_rates:
        :return:
        """
        response = []
        for rate in result:
            if null_rates and rate[2] < 3:
                average_price = None
            else:
                average_price = rate[1]
            response.append({'day': rate[0],
                             'average_price': average_price})
        return response

    def get(self, request, *args, **kwargs):
        """
        Implement an API endpoint that takes the following parameters:

            date_from
            date_to
            origin
            destination
        and returns a list with the average prices for each day
        on a route between port codes origin and destination.
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        serializer = RateListSerializer(data=request.query_params)

        if not serializer.is_valid():
            response = {'error_message': serializer.errors}
            return Response(response,
                            status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data

        date_from = data['date_from']
        date_to = data['date_to']
        origin = data['origin']
        destination = data['destination']

        try:
            with connection.cursor() as cursor:
                cursor.execute(rate_list_query, (origin, origin, destination,
                                                 destination, date_from,
                                                 date_to))
                result = cursor.fetchall()
                response = RateList.filtered_result(result, self.null_rates)
                return Response(response, status.HTTP_200_OK)
        except Exception as exc:
            logger.error(str(exc))
            response = {"error_message": "Internal Server Error."}
            return Response(response, status.HTTP_500_INTERNAL_SERVER_ERROR)
        """
        # ORM QUERY
        from django.db.models import Avg, Count, Q
        from core.models import Price, Port
        from core.models import Price
        try:
            orig_code_lookup = Q(orig_code=origin) | Q(orig_code__region=origin)
            dest_code_lookup = Q(dest_code=destination) | Q(dest_code__region=destination)

            prices = Price.objects.\
                filter(orig_code_lookup, dest_code_lookup,
                       day__gte=date_from, day__lte=date_to)\
                .values('day',)\
                .annotate(total=Avg('price'),
                          times=Count('price')
                          )
            return Response(prices)
        except Exception as exc:
            logger.error(str(exc))
            response = {"error_message": "Something went wrong."}
            return Response(response, status.HTTP_500_INTERNAL_SERVER_ERROR)
        """
