import requests
from bs4 import BeautifulSoup
import json

class MainWebService:
    def __init__(self):
        self.loginUrl = 'http://apps2.itlalaguna.edu.mx/StatusAlumno/login.aspx'
        self.seleccionaFormUrl = 'http://apps2.itlalaguna.edu.mx/StatusAlumno/frmSelecciona.aspx'
        self.cargaFormUrl = 'http://apps2.itlalaguna.edu.mx/StatusAlumno/alumnos/frmCargaAcademica.aspx'
        self.kardexUrl = 'http://apps2.itlalaguna.edu.mx/StatusAlumno/alumnos/frmKardex.aspx'
        self.session = requests.Session()

    def getLogin(self):
        return self.session.get(self.loginUrl)

    def extractLoginHiddenValues(self):
        loginHtmlText = self.getLogin()
        loginPage = BeautifulSoup(loginHtmlText.text, 'html.parser')

        inputs = loginPage.body.find('form').findAll('input')

        viewState = inputs[0].get('value')
        viewStateGenerator = inputs[1].get('value')
        eventValidation = inputs[2].get('value')

        return {'viewState': viewState, 'viewStateGenerator': viewStateGenerator, 'eventValidation': eventValidation}

    def doLogin(self, hiddenValues, noControl, password):
        body = {"__EVENTTARGET": "", "__EVENTARGUMENT": "",
                "__VIEWSTATE": hiddenValues['viewState'],
                "__VIEWSTATEGENERATOR": hiddenValues['viewStateGenerator'],
                "__EVENTVALIDATION": hiddenValues['eventValidation'],
                "tbLogin": noControl, "tbPassword": password,
                "Button2": "Ingresar"}
        headers = {'Content-Type': 'application/x-www-form-urlencoded',
                   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'}
        result = self.session.post(
            self.loginUrl, headers=headers, data=body)
        return result

    def getKardex(self):
        result = self.session.get(self.kardexUrl)
        return result.text

    def getCarga(self): 
        result = self.session.get(self.cargaFormUrl)
        return result.text
