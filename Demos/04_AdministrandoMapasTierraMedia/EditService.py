# Demonstrates how to modify the min and max instances for a service

# For Http calls
import httplib, urllib, json
from getToken import *

# Ask for admin/publisher user name and password
username = "adminGis"
password = "admingis2016"
serverName = "cginca.cgfm.col"
serverPort = 6443
adminServices = "https://cginca.cgfm.col:6443/arcgis/admin/services/"
services = ["CGFM_J3/AccionesTerroristas.MapServer"]
folderURL = "https://cginca.cgfm.col:6443/arcgis/admin/services/CGFM_J3"

minInstancesNum = 1
maxInstancesNum = 2
maxRecordCount = 1000

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
            service = ""
            try:
                service = "%s/%s.%s" % (item["folderName"], item["serviceName"], item["type"])
                serviceURL = adminServices + service
                httpConn.request("POST", serviceURL, params, headers)

                # Read response
                response = httpConn.getresponse()
                if (response.status != 200):
                    httpConn.close()
                    print "Could not read service information."
                else:
                    data = response.read()

                    # Check that data returned is not an error object
                    if not assertJsonSuccess(data):
                        print "Error when reading service information. " + str(data)
                    else:
                        #print "Service information read successfully. Now changing properties..."
                        pass

                    # Deserialize response into Python object
                    dataObj = json.loads(data)
                    httpConn.close()

                    # Edit desired properties of the service
                    dataObj["minInstancesPerNode"] = minInstancesNum
                    dataObj["maxInstancesPerNode"] = maxInstancesNum
                    dataObj["properties"]["maxRecordCount"] = maxRecordCount

                    # Serialize back into JSON
                    updatedSvcJson = json.dumps(dataObj)

                    # Call the edit operation on the service. Pass in modified JSON.
                    params = urllib.urlencode({'token': token, 'f': 'json', 'service': updatedSvcJson})
                    editSvcURL = adminServices + service + "/edit"
                    httpConn.request("POST", editSvcURL, params, headers)

                    # Read service edit response
                    editResponse = httpConn.getresponse()
                    if (editResponse.status != 200):
                        httpConn.close()
                        print "Error while executing edit."

                    else:
                        editData = editResponse.read()

                        # Check that data returned is not an error object
                        if not assertJsonSuccess(editData):
                            print "Error returned while editing service" + str(editData)
                        else:
                            print "Service %s edited successfully." % service

            except:
                print "Error al procesar el servicio %s" % service

        httpConn.close()


