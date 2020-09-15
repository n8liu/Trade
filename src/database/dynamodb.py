""" This file abstracts the api used to access our AWS DynamoDB NoSQL database
"""
import boto3
from decouple import config

db_access_id = config('AWS_ACCESS_KEY_ID')
db_access_key = config('AWS_SECRET_ACCESS_KEY')

dynamodb = boto3.resource('dynamodb', aws_access_key_id=db_access_id, aws_secret_access_key=db_access_key, region_name='us-east-1')

def get_trade(table, pair, strategy):
    """
    get_strategy('Currency', 'EUR_USD', 'sample strategy')
    """
    db_table = dynamodb.Table(table)
    response = db_table.get_item(Key={"Pair": pair, "Strategy": strategy})
    return response['Item']

def post_trade(pair, strategy, position):
    """
    """
    assert position in ["long", "short"], "position must be 'long' or 'short' (case-sensitive)."
    db_table = dynamodb.Table('Currency')
    response = db_table.put_item(Item=
        {
            "Pair": pair, 
            "Strategy": strategy,
            "Position": position
        })

def delete_trade(pair, strategy):
    """
    """
    db_table = dynamodb.Table('Currency')
    response = db_table.delete_item(Key={"Pair": pair, "Strategy": strategy})



