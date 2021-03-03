"""
"""
from rest_framework import serializers


class RateBaseSerializer(serializers.Serializer):
    """
    """
    def validate(self, attrs):
        """
        Check that date_from is less than date_to
        """
        if attrs['date_from'] > attrs['date_to']:
            raise serializers.ValidationError("date_from must be less than "
                                              "or equal to date_to.")
        return attrs


class RateCreateSerializer(RateBaseSerializer):
    """
    """
    date_from = serializers.DateField(format='%Y-%m-%d')
    date_to = serializers.DateField(format='%Y-%m-%d')

    origin_code = serializers.CharField(max_length=5)
    destination_code = serializers.CharField(max_length=5)

    prices = serializers.ListField(child=
                                   serializers.DecimalField(max_digits=10,
                                                            decimal_places=2,
                                                            required=False))
    currency_code = serializers.CharField(required=False)


class RateListSerializer(RateBaseSerializer):
    """
    """
    date_from = serializers.DateField(format='%Y-%m-%d')
    date_to = serializers.DateField(format='%Y-%m-%d')

    origin = serializers.CharField()
    destination = serializers.CharField()

