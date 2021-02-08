from MainWebService import MainWebService
import json
from bs4 import BeautifulSoup


class MainScraper:
    def __init__(self, noControl, password):
        self.webReq = MainWebService()
        self.noControl = noControl
        self.password = password
        self.load()

    def load(self):
        hiddenLoginValues = self.webReq.extractLoginHiddenValues()
        res = self.webReq.doLogin(
            hiddenLoginValues, self.noControl, self.password)
        if res.status_code != 200:
            return Exception('Invalid credentials')

    def getStudentName(self):
        cargaScraper = BeautifulSoup(self.webReq.getCarga(), 'html.parser')
        self.studentName = cargaScraper.find_all(
            'span',  id='MainContent_lblNombre')[0]
        return {'name': self.studentName.text}

    def getKardex(self):
        kardexHtml = self.webReq.getKardex()
        scraper = BeautifulSoup(kardexHtml, 'html.parser')

        self.studentName = scraper.find_all('a', id='studentName')
        kardexTable = scraper.find('table', id='MainContent_GridView1')
        kardexRows = self.getTableRows(kardexTable)
        # print(json.dumps(kardexRows))
        return kardexRows

    def getKardexProperties(self, key):
        key = key.replace(' ', '')
        tableDict = {'Calificación': 'grade', 'Clave': 'key',
                     'Materia': 'subject', 'Periodo1': 'date', 'Semestre1': 'semester', }
        if not key in tableDict:
            # print(key)
            return None
        return tableDict[key]

    def getTableRows(self, tableScraper):
        rows = []
        tableRows = tableScraper.find_all('tr')
        tableHeader = tableRows[0]
        headerValues = tableHeader.find_all('th')

        # print(tableHeader)
        for tableRow in tableRows[1:]:
            rowValues = tableRow.find_all('td')
            row = {}
            colId = 0
            for header in headerValues:
                key = self.getKardexProperties(header.text)

                if key == 'grade' or key == 'semester':
                    row[key] = int(rowValues[colId].text)
                elif key is not None:
                    row[key] = rowValues[colId].text

                colId = colId + 1

            rows.append(row)

        return rows

    def getCarga(self):
        cargaHtml = self.webReq.getCarga()
        scrapper = BeautifulSoup(cargaHtml, 'html.parser')

        cargaTable = scrapper.find('table', id='MainContent_GridView1')
        if not cargaTable:
            return {'carga': []}
        cargaRows = self.getTableRows(cargaTable)

        return {'carga': cargaRows}
