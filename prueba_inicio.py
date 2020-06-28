import time
import json
from WebServiceReq import WebRequest
from WebScrapper import WebScrapper

start_time = time.time()

alumnoNoControl = '17130854'

req = WebRequest(alumnoNoControl=alumnoNoControl)
req.load()

scrapper = WebScrapper(req, alumnoNoControl)
scrapper.load()


print("--- %s seconds ---" % (time.time() - start_time))