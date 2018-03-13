
def getInitExecFunction(rg_intentName):
    import boto3
    import json
    from boto3.dynamodb.conditions import Key, Attr
    # Get the service resource.
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('intentTable')
    response = table.query(
        KeyConditionExpression=Key('Intent').eq(rg_intentName)
        #FilterExpression=Attr('Slot').eq(rg_filterData)
    )
    items = response['Items'] #[0]['Slot']
    if len(items) == 1:
        rtngetExecFunction = items[0]['initExecFunction']
    else:
        rtngetExecFunction = False
    return rtngetExecFunction

print(getInitExecFunction('backupIntent'))

"""
def getAllInitFunction():
    import boto3
    import json
    from boto3.dynamodb.conditions import Key, Attr
    # Get the service resource.
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('intentTable')
    response = table.query(
        #KeyConditionExpression=Key('Intent').eq(rg_intentName)
        FilterExpression=Attr('Slot').eq(*)
    )
    items = response['Items'] #[0]['Slot']
    if len(items) == 1:
        rtngetExecFunction = items[0]['initExecFunction']
    else:
        rtngetExecFunction = "Sorry, I did not get that. Please try later."
    return rtngetExecFunction

print(getAllInitFunction())
"""
