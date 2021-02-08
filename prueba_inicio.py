''' 
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

import time
from MainWebService import MainWebService
from MainScraper import MainScraper

# print('Starting')

# webService = MainWebService()
# hiddenValues = webService.extractLoginHiddenValues()
# result = webService.doLogin(hiddenValues, '17130854', 'tc5120lag')
# kardex = webService.getKardex()
# carga = webService.getCarga()

# print(hiddenValues)
# print(result.text)
# print(kardex)

print('Test scraper')
start = time.time()
mainScraper = MainScraper('17130854', 'tc5120lag')
name = mainScraper.getStudentName()

kardex = mainScraper.getKardex()
carga = mainScraper.getCarga()

print('Tiempo: ', (time.time() - start) * 1000)
print(name)

print('Finish')