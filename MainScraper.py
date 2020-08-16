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
        return self.studentName.text

    def getKardex(self):
        kardexHtml = self.webReq.getKardex()
        scraper = BeautifulSoup(kardexHtml, 'html.parser')

        self.studentName = scraper.find_all('a', id='studentName')
        kardexTable = scraper.find('table', id='MainContent_GridView1')
        kardexRows = self.getKardexRows(kardexTable)
        # print(json.dumps(kardexRows))
        return kardexRows

    def getKardexRows(self, tableScraper):
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
                row[header.text] = rowValues[colId].text
                colId = colId + 1
            
            rows.append(row)

        return rows
