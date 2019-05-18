import requests


def returnCountryCode(apiKey, ipAddr):
    try:
        data = requests.get(
            "http://api.ipinfodb.com/v3/ip-country/?key="+apiKey+"&ip="+ipAddr+"&format=json").json()
        if (data['statusCode'] == "OK"):
            return(data['countryCode'])
        else:
            return("None")
    except:
        return("None")
