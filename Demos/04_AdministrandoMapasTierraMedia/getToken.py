import httplib, urllib, json

# A function to generate a token given username, password and the adminURL.

def getToken(username, password, serverName, serverPort):
    # Token URL is typically http://server[:port]/arcgis/admin/generateToken
    tokenURL = "https://jescudero:6443/arcgis/admin/generateToken"

    params = urllib.urlencode({'username': username, 'password': password, 'client': 'requestip', 'f': 'json'})

    headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}

    # Connect to URL and post parameters
    #httpConn = httplib.HTTPConnection(serverName, serverPort)
    httpConn = httplib.HTTPSConnection(serverName, serverPort)
    httpConn.request("POST", tokenURL, params, headers)

    # Read response
    response = httpConn.getresponse()
    if (response.status != 200):
        httpConn.close()
        print "Error while fetching tokens from admin URL. Please check the URL and try again."
        return
    else:
        data = response.read()
        httpConn.close()

        # Check that data returned is not an error object
        if not assertJsonSuccess(data):
            return

        # Extract the token from it
        token = json.loads(data)
        return token['token']
        return token['token']


# A function that checks that the input JSON object
#  is not an error object.
def assertJsonSuccess(data):
    obj = json.loads(data)
    if 'status' in obj and obj['status'] == "error":
        print "Error: JSON object returns an error. " + str(obj)
        return False
    else:
        return True