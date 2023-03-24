from models import MysfitModel
import os
import simplejson as json


def load(data_file, table=None):
    with open(data_file) as f:
        json_data = json.loads(f.read())
        for item in json_data:
            mysfit=MysfitModel(**item)
            mysfit.create(table=table)
    return 200

def precheck(table, force=False):
    
    if force:
        try:
            resp_code = load(f'{os.path.dirname(__file__)}/mysfit_data.json', table=table)
            assert resp_code == 200
        except Exception as e: 
            raise Exception(f"Something went wrong in Precheck.  Details: {e}")

    if not (SEEDED := table.item_count > 0):
        try:
            resp_code = load(f'{os.path.dirname(__file__)}/mysfit_data.json', table=table)
            assert resp_code == 200
        except Exception as e: 
            raise Exception(f"Something went wrong in Precheck.  Details: {e}")

def gateway_response(data):
    return {
        "statusCode": 200,
        "headers": {
            "Content-type": "application/json",
            "Access-Control-Allow-Origin": "*"},
        "body": json.dumps(data)
    }

