def create_snow_incident():
    #Need to install requests package for python
    #easy_install requests
    import requests
    import json

    # Set the request parameters
    url = 'https://dev33601.service-now.com/api/now/v1/table/incident'

    # Eg. User name="admin", Password="admin" for this code sample.
    user = 'admin'
    pwd = 'Password@123'

    # Set proper headers
    headers = {"Content-Type":"application/json","Accept":"application/json"}
    data = {"short_description" : "This is the short description", "description":"This is the description"}
    data_json = json.dumps(data)
    # Do the HTTP request
    #response = requests.get(url, auth=(user, pwd), headers=headers  )
    response = requests.post(url, data=data_json, auth=(user, pwd), headers=headers)
    print(response)
    # Check for HTTP codes other than 200
    if response.status_code != 201:
        #print('Status:', response.status_code, 'Headers:', response.headers, 'Error Response:',response.json())
        #exit()
        snowResponse = "Faild to create an incident. Please contact administrator"
    else:
        snowResponse = "Created an incident. " + response.json()['result']['number'] + " "
    # Decode the JSON response into a dictionary and use the data
    data = response
    print(data)
    return snowResponse

print(create_snow_incident())
