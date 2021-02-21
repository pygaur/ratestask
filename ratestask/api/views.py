"""
"""
from django.db.models import Avg, Count, Q
from django.db.models.functions import Round
from django.db import connection

from .serializers import RateSerializer

from core.models import Price

from rest_framework.views import APIView
from rest_framework.response import Response


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

            """ SQL Query 1 """
            with connection.cursor() as cursor:
                query = """
                        SELECT "prices"."day", ROUND(AVG("prices"."price"),2)
                            AS "total" FROM "prices"
                        INNER JOIN "ports" ON ("prices"."orig_code" =
                            "ports"."code")
                        INNER JOIN "ports" T4 ON ("prices"."dest_code" =
                            T4."code")
                        WHERE (("prices"."orig_code" = %s)
                                        OR
                            ("ports"."parent_slug" = %s))
                        AND
                            (("prices"."dest_code" = %s
                                    OR
                            (T4."parent_slug" = %s)) 
                        AND "prices"."day" BETWEEN %s::date AND %s::date)
                        GROUP BY "prices"."day"
                        """
                cursor.execute(query, (origin, origin, destination, destination, date_from, date_to))
                result = cursor.fetchall()
                return Response(result)


            # Django ORM way
            prices = Price.objects.\
                filter(orig_code_lookup, dest_code_lookup,
                       day__gte=date_from, day__lte=date_to)\
                .values('day',)\
                .annotate(total=Avg('price'),
                          count=Count('price')
                          )\
                .order_by()

            return Response(prices)

        return Response(serializer.errors)

