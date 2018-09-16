from flask import Flask, request
import requests
import parser

app = Flask(__name__)

#===============================================================================
# Asks the AXA API for the full drug usage description
# @param swissMedId the swiss medic id
# @returns the fulls description as HTML text
# @raises Exception when the status code is not 200
#===============================================================================
def askAxaBackend(swissMedId):
    url = 'https://health.axa.ch/hack/api/drugs/' + swissMedId + '/info/patient'
    header = {'Authorization': 'real receipt'}
    r = requests.get(url, headers=header)
    if 200 != r.status_code:
        raise Exception("Error status code %s" % (r.status_code))
    return r.text

#===============================================================================
# Returns a mocked response from a JSON file
# @returns the mocked response as JSON
#===============================================================================
def getMockedResponse(swissMedId):
    responseFilePath = 'easypill/mocked_response_' + swissMedId + '.json'
    f = open(responseFilePath, 'r')
    mockedResponse = f.read()
    f.close()
    return mockedResponse

#===============================================================================
# Asks the AXA backend for the full pill usage description
# @param swissMedId the swiss medical id
# @returns the summary as JSON
#===============================================================================
def getDoseSummary(swissMedId):
    #fullText = askAxaBackend(swissMedId)
    fullText = getMockedResponse(swissMedId)
    return fullText

@app.route("/")
def hello():
    return '<img src="https://o.aolcdn.com/hss/storage/midas/37e0050ee936a68e680564854b0c7fb5/201853233/putinmeme02.jpg">'

#===============================================================================
# Routing handler for the pill usage summary request
# Requests should be sent to /api/v1/pills/summary/<swissMedId>
# @returns the summary of the usage info
#===============================================================================
@app.route('/api/v1/pills/summary', methods=['get'])
def routeHandler():
    swissMedId = request.args.get('swissMedId')
    print('Got request for swissMedId %s' % (swissMedId))
    return getDoseSummary(swissMedId)

if __name__ == "__main__":
    app.run(host='0.0.0.0')