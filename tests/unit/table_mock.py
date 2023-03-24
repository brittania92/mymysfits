import sys, os, json
from boto3.dynamodb.conditions import Key
sys.path.append(os.path.join(os.path.dirname(__file__), '../../src'))


print(os.path.dirname(__file__))
with open(f'{os.path.dirname(__file__)}/../../src/mysfit_data.json') as jsonf:
    data = json.loads(jsonf.read())

    
class MockTable():

    def __init__(self) -> None:
        pass

    def scan(self):

        return { "Items": data }
    
    def put_item(*args, **kwargs):

        return True

    def get_item(*args, **kwargs):
        
        return data[0]
    
        