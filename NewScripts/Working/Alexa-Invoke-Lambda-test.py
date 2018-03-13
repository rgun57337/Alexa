import boto3
import json

def invokeLambda(lambdaARN):
    client = boto3.client('lambda')
    event_value = { "key3": "rajesh", "key2": "gundeti" }
    response = client.invoke(
        FunctionName=lambdaARN,
        InvocationType='RequestResponse',
        Payload=json.dumps(event_value),
    )
    t = response['Payload']
    rtnLamResponce = t.read()
    return rtnLamResponce

print(invokeLambda('arn:aws:lambda:us-east-1:909388439755:function:backupIntentFunction'))
