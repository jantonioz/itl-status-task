''' import time
import json
from WebServiceReq import WebRequest
from WebScrapper import WebScrapper

start_time = time.time()

alumnoNoControl = '17130854'

req = WebRequest(alumnoNoControl=alumnoNoControl)
req.load()

scrapper = WebScrapper(req, alumnoNoControl)
scrapper.load()


print("--- %s seconds ---" % (time.time() - start_time)) '''


from MainWebService import MainWebService

print('Starting')

webService = MainWebService()
hiddenValues = webService.extractLoginHiddenValues()
result = webService.doLogin(hiddenValues, '17130854', 'tc5120lag')
kardex = webService.getKardex()

# print(hiddenValues)
# print(result.text)
print(kardex)