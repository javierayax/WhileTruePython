# Demonstrates how to modify the min and max instances for a service

# For Http calls
import httplib, urllib, json
from getToken import *

# Ask for admin/publisher user name and password
username = "siteadmin"
password = "siteadmin"
serverName = "jescudero"
serverPort = 6443
adminServices = "https://jescudero:6443/arcgis/admin/"


folder = "Python/"
stopOrStart = "STOP" # START-STOP
folderURL = "%s/%s" % (adminServices, folder)

"""
# Check to make sure the minimum and maximum are numerical
try:
    minInstancesNum = int(minInstances)
    maxInstancesNum = int(maxInstances)
except ValueError:
    print "Numerical value not entered for minimum, maximum, or both."

# Check to make sure that the minimum is not greater than the maximum
if minInstancesNum > maxInstancesNum:
    print "Maximum number of instances must be greater or equal to minimum number."
"""

# Get a token
token = getToken(username, password, serverName, serverPort)
if token == "":
    print "Could not generate a token with the username and password provided."

else:

    # This request only needs the token and the response formatting parameter
    params = urllib.urlencode({'token': token, 'f': 'json'})

    headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}

    # Connect to service to get its current JSON definition
    #httpConn = httplib.HTTPConnection(serverName, serverPort)

    httpConn = httplib.HTTPSConnection(serverName, serverPort)

    httpConn.request("POST", folderURL, params, headers)
    response = httpConn.getresponse()

    if (response.status != 200):
        httpConn.close()
        print "Could not read folder information."
    else:
        data = response.read()

        # Check that data returned is not an error object
        if not assertJsonSuccess(data):
            print "Error when reading folder information. " + str(data)
        else:
            print "Processed folder information successfully. Now processing services..."

        # Deserialize response into Python object
        dataObj = json.loads(data)
        httpConn.close()

        # Loop through each service in the folder and stop or start it
        for item in dataObj['services']:

            fullSvcName = item['serviceName'] + "." + item['type']

            # Construct URL to stop or start service, then make the request
            stopOrStartURL = adminServices + folder + fullSvcName + "/" + stopOrStart
            httpConn.request("POST", stopOrStartURL, params, headers)

            # Read stop or start response
            stopStartResponse = httpConn.getresponse()
            if (stopStartResponse.status != 200):
                httpConn.close()
                print "Error while executing stop or start. Please check the URL and try again."
            else:
                stopStartData = stopStartResponse.read()

                # Check that data returned is not an error object
                if not assertJsonSuccess(stopStartData):
                    if str.upper(stopOrStart) == "START":
                        print "Error returned when starting service " + fullSvcName + "."
                    else:
                        print "Error returned when stopping service " + fullSvcName + "."

                    print str(stopStartData)

                else:
                    print "Service " + fullSvcName + " processed successfully."

        httpConn.close()


