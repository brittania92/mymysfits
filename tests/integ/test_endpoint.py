from os import environ as env
import requests
import time

ENDPOINT=env.get('API_ENDPOINT')

def test_list_all(retry=3):
    for r in range(retry):
        try:
            resp = requests.get(f'{ENDPOINT}/mysfits')
            assert len(resp.json()) == 12
            return True
        except AssertionError:
            time.sleep(10)
        except Exception:
            raise Exception('Test Failed')


def test_get_filtered(retry=3):
    
    for r in range(retry):
        try:
            resp = requests.get(f'{ENDPOINT}/mysfits', params={
                'filter': 'GoodEvil',
                'value': 'Evil'})
            assert len(resp.json()) == 4
            return True
        except AssertionError:
            time.sleep(10)
        except Exception:
            raise Exception('Test Failed')