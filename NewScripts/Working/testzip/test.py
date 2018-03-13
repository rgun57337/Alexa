import boto3

def invoke_lambda(lambdaARN):
    client = boto3.client('lambda')
    r = client.invoke(
        FunctionName=lambdaARN,
        InvocationType='RequestResponse',
        #Payload=bytes(payload)
    )
    t = r['Payload']
    j = t.read()
    print j

invoke_lambda('arn:aws:lambda:us-east-1:909388439755:function:backupIntentFunction')
