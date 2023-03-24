from boto3.dynamodb.types import TypeSerializer, TypeDeserializer
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError
from dataclasses import dataclass


class ObjectModel():

    def _deserialize(self, d: dict, key='Items') -> dict:
        
        r = { key: [TypeDeserializer().deserialize(v) for v in d.get(key)]}
        return r


    def _serialize(self, d: dict):
        
        return TypeSerializer().serialize(d)
  
    @staticmethod
    def list_items(table=None, filter: dict=None) -> list:

        if not filter:
            resp = table.scan()
            return resp.get('Items')
        else: 
            queryParams = {
                'IndexName': filter.get('indexName'),
                'Select': 'ALL_ATTRIBUTES',
                'KeyConditionExpression': Key(filter.get('attributeKey')).eq(filter.get('attributeValue'))
            }
            resp = table.query(**queryParams)
            return resp.get('Items')

    def create(self, table=None) -> dict:
        
        item = { "Item": self.item() }
        if table:
            return table.put_item(**item)
        else:
            return item

    def get(self, attributeKey: str, attributeValue: str, table=None) -> dict:
        
        resp = table.get_item(Key={attributeKey: attributeValue})
        return resp

    def update(self, key: dict, attributeKey: str, attributeValue: str, table=None) -> dict:

        table.update_item(
            Key=key,
            UpdateExpression=f"set {attributeKey} = :v",
            ExpressionAttributeValues={
                ':v': attributeValue
            }
        )
    
    def delete(self, table=None) -> dict:
        raise NotImplementedError

    def item(self) -> dict:

        return self.__dict__
    
@dataclass
class MysfitModel(ObjectModel):

    GOODEVILINDEX="GoodEvilIndex"
    LAWCHAOSINDEX="LawChaosIndex"

    Name: str = ""
    Species: str = ""
    Description: str = ""
    Age: int = 0
    GoodEvil: str = ""
    LawChaos: str = ""
    ThumbImageUri: str = ""
    ProfileImageUri: str = ""
    Likes: int = 0
    Adopted: bool = False