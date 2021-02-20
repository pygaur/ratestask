"""
"""
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
        return Response([])


