import boto3
from models import MysfitModel
from os import environ as env
from utils import precheck, gateway_response

_ = boto3.resource('dynamodb')

TABLE = _.Table(env.get('APPNAME'))

force_load = 'FORCE_UPDATE' in env.keys()

precheck(table=TABLE, force=force_load)

def app_router(path, queryParams=None):

    router = {
        '/mysfits': get_all_mysfits
    }

    filter_router = {
        '/mysfits': get_filtered_mysfits
    }

    if queryParams:
        filter = {}
        attributeName=queryParams.get('filter')
        if attributeName == "GoodEvil":
            filter['indexName'] = MysfitModel.GOODEVILINDEX
        elif attributeName == "LawChaos":
            filter['indexName'] = MysfitModel.LAWCHAOSINDEX
        else:
            raise Exception("Unknown FilterExpression Key")
        filter['attributeKey'] = attributeName
        filter['attributeValue'] = queryParams.get('value')
        return filter_router[path](filter)
    else:
        return router[path]()

def get_all_mysfits():
    model = MysfitModel()
    resp = model.list_items(table=TABLE)
    return resp

def get_filtered_mysfits(filter):
    model = MysfitModel()
    resp = model.list_items(table=TABLE, filter=filter)
    return resp

def get_myfit(name):
    model = MysfitModel()
    resp = model.get('Name', name, table=TABLE )
    return resp

def update_mysfit(name, attributeKey, attributeValue):
    model = MysfitModel()
    resp = model.update({'name':name}, attributeKey, attributeValue)

def handler(event, ctx):
    print(event)
    return gateway_response(app_router(
        event.get('rawPath'), 
        event.get('queryStringParameters')))