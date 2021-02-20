"""
"""
from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import RateSerializer


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
            return Response([])

        return Response(serializer.errors)

