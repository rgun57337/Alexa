import boto3

def invokeLambda(lambdaARN):
    client = boto3.client('lambda')
    response = client.invoke(
        FunctionName=lambdaARN,
        InvocationType='RequestResponse'
    )
    t = response['Payload']
    rtnLamResponce = t.read()
    return rtnLamResponce

print(invokeLambda('arn:aws:lambda:us-east-1:909388439755:function:backupIntentFunction'))
