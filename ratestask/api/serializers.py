"""
"""
from rest_framework import serializers


class RateSerializer(serializers.Serializer):
    """
    """
    date_from = serializers.DateField(format='%Y-%m-%d')
    date_to = serializers.DateField(format='%Y-%m-%d')
    origin = serializers.CharField()
    destination = serializers.CharField()

    def validate(self, attrs):
        """
        Check that date_from is less than date_to
        """
        if attrs['date_from'] > attrs['date_to']:
            raise serializers.ValidationError("date_from must be less than "
                                              "or equal to date_to.")
        return attrs
