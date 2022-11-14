import requests
import json
from currencies import keys

class APIException(Exception):
    pass

class CurrencyConverter:
    @staticmethod
    def convert(quote: str, base: str, amount: str):
        if quote == base:
            raise APIException('Введены одинаковые валюты')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise APIException(f'Введена недопустимая валюта {quote}')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise APIException(f'Введена недопустимая валюта {base}')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не корректное количество {amount}')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
        total_base = json.loads(r.content)[keys[base]]

        return round(total_base * amount, 2)