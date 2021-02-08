from flask import request, Flask

from MainWebService import MainWebService
from MainScraper import MainScraper

app = Flask(__name__)


def getCredentials(request):
    if request.json:
        return request.json['noControl'], request.json['password']
    elif request.args:
        return request.args['noControl'], request.args['password']


@app.route('/api/kardex', methods=['POST', 'GET'])
def getKardex():
    if request.method != 'POST':
        return {'code': 400, 'message': 'Invalid method'}
    noControl, password = getCredentials(request)
    scrapper = MainScraper(noControl, password)
    kardex = scrapper.getKardex()
    return {'kardex': kardex}


@app.route('/api/carga', methods=['POST'])
def getCarga():
    if request.method != 'POST':
        return {'code': 400, 'message': 'Invalid method'}
    noControl, password = getCredentials(request)
    scrapper = MainScraper(noControl, password)
    carga = scrapper.getCarga()
    return carga


@app.route('/api/name', methods=['POST'])
def getName():
    if request.method != 'POST':
        return {'code': 400, 'message': 'Invalid method'}
    noControl, password = getCredentials(request)
    scrapper = MainScraper(noControl, password)
    name = scrapper.getStudentName()
    return name


@app.route('/test/hw')
def test_hw():
    return 'Hello world'


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)