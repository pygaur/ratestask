"""
"""
from decimal import Decimal

import requests

from django.conf import settings


def exchange_rates(amount, currency_code):
    """
    :param amount:
    :param currency_code:
    :return:
    """
    params = {'app_id': settings.EXCHANGE_RATE_APP_ID}

    response = requests.get(url=settings.EXCHANGE_RATE_URL,
                            params=params)
    data = response.json()
    usd_rate = data['rates'][currency_code.upper()]
    usd_amount = Decimal(amount)/Decimal(usd_rate)
    return usd_amount
