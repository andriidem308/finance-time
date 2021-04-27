from datetime import date
from decimal import Decimal

import requests
from celery import shared_task
from requests.exceptions import HTTPError
from currency.models import Currency

from datetime import timedelta
from yahoofinancials import YahooFinancials

# from django.conf import settings


def save_currency(cur, src, buy, sale):
    last = Currency.objects.filter(currency=cur, source=src).last()
    d_buy, d_sale = Decimal(buy), Decimal(sale)
    if last is None or (last.buy != d_buy or last.sale != d_sale):
        Currency.objects.create(currency=cur, source=src, buy=d_buy, sale=d_sale)


@shared_task
def parse_monobank():
    src = 1
    url = "https://api.monobank.ua/bank/currency"
    response = requests.get(url)

    try:
        response = requests.get(url)
        response.raise_for_status()
    except HTTPError as http_err:
        # TODO: log http_error
        pass
    except Exception as err:
        # TODO: log error
        pass

    currency_codes = {840: 1, 978: 2}
    data = response.json()
    print(data)

    for row in data:
        if row['currencyCodeA'] in currency_codes and row['currencyCodeB'] == 980:
            buy = round(Decimal(row['rateBuy']), 2)
            sale = round(Decimal(row['rateSell']), 2)
            cur = currency_codes[row['currencyCodeA']]

            save_currency(cur, src, buy, sale)


@shared_task
def parse_yahoo():
    currencies = ['EURUAH=X', 'USDUAH=X']
    source = 2
    currency_codes = {'USDUAH=X': 1, 'EURUAH=X': 2}
    for cur in currencies:
        yahoo_financials_currencies = YahooFinancials(cur)
        yesterday = date.today() - timedelta(days=1)
        buy = round(Decimal(yahoo_financials_currencies.get_historical_price_data(str(yesterday), str(yesterday), "daily")[cur][
            'prices'][0]['close']), 2)
        sale = round(Decimal(yahoo_financials_currencies.get_historical_price_data(str(yesterday), str(yesterday), "daily")[cur][
            'prices'][0]['close']), )
        ccy = currency_codes[cur]
        save_currency(ccy, source, buy, sale)


@shared_task
def parse_vkurse():
    url = "http://vkurse.dp.ua/course.json"
    response = requests.get(url)

    try:
        response = requests.get(url)
        response.raise_for_status()
    except HTTPError as http_err:
        # TODO: log http_error
        pass
    except Exception as err:
        # TODO: log error
        pass

    currency_codes = {"Dollar": 1, "Euro": 2}

    data = response.json()
    source = 3
    for row in data:
        if row in currency_codes:
            buy = data[row]["buy"]
            sale = data[row]["sale"]
            ccy = currency_codes[row]
            save_currency(ccy, source, buy, sale)

