
def getExecFunction(rg_intentName, rg_filterData):
    import boto3
    import json
    from boto3.dynamodb.conditions import Key, Attr
    # Get the service resource.
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('intentSlotTable')
    response = table.query(
        KeyConditionExpression=Key('Intent').eq(rg_intentName) & Key('Slot').eq(rg_filterData)
        #FilterExpression=Attr('Slot').eq(rg_filterData)
    )
    items = response['Items'] #['Slot']
    if len(items) == 1:
        rtngetExecFunction = items[0]['execFunction']
    else:
        rtngetExecFunction = "Sorry, I did not get that. Please try later."
    return rtngetExecFunction

print(getExecFunction('backupIntent','stage'))
