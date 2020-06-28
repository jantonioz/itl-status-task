from WebServiceReq import WebRequest
import json
from bs4 import BeautifulSoup


class HorariosScrapper:
    def __init__(self, req: WebRequest):
        self.horariosScrapperList = []
        self.horarios = []
        for horarioItemText in req.loadHorarios():
            scrapper = BeautifulSoup(horarioItemText['text'], 'html.parser')
            self.horariosScrapperList.append(scrapper)

    def getHours(self, str):
        if "/" in str:  # DATE FORMAT
            horaStr, aula = str.split('/')
            if len(horaStr) == 1 and not aula:
                return {"inicio": 0, "fin": 0, "aula": ""}

            horaStr = ('0'+horaStr, horaStr)[len(horaStr) == 4]

            horas = [horaStr[i:i+2] + ':00' for i in range(0, 4, 2)]

            return {'inicio': horas[0], 'fin': horas[1], 'aula': aula}

    def extractAll(self):
        for scrapper in self.horariosScrapperList:
            carrera = scrapper.find('body').findAll(
                'pre')[1].find('b').find('font').text.strip()[9:]
            table = scrapper.find('body').find('table')
            tableFullData = table.findAll('tr')
            tableHeadersData = tableFullData[0].findAll('td')
            tableData = tableFullData[1:]

            headers = [col.text.strip() for col in tableHeadersData]

            for rows in tableData:
                colIdx = 0
                dataRow = {}
                for col in rows.findAll('td'):
                    col = col.text.strip()
                    if '/' in col:
                        dataRow[headers[colIdx].lower()] = self.getHours(col)
                    else:
                        dataRow[headers[colIdx].lower()] = col
                    colIdx += 1
                dataRow['carrera'] = carrera
                self.horarios.append(dataRow)

            # self.horarios.append({'carrera': carrera, 'horarios': data})
        # print(json.dumps(self.horarios))
        # fileData = open('horarios.json', 'w')
        # fileData.write(json.dumps(self.horarios))
        # fileData.close()
        # print('done')
