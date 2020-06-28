from WebServiceReq import WebRequest
import json
from bs4 import BeautifulSoup


class WebScrapper:
    def __init__(self, req: WebRequest, noControl):
        self.homeScreapper = BeautifulSoup(req.getHomeData(), 'html.parser')
        self.cursandoScrapper = BeautifulSoup(
            req.getCursandoData(), 'html.parser')
        self.kardexScrapper = BeautifulSoup(req.getKardexData(), 'html.parser')
        self.noControl = noControl.strip()

    def load(self):
        kardexTable = self.kardexScrapper.findAll('table')[1].findAll('tr')[0].find(
            'td', {'style': 'text-align:left'}).find('center').find('table')

        tablaPrincipal = self.cursandoScrapper.findAll('table')[1]
        tableData2 = tablaPrincipal.findAll('td')[1]
        detalles = tableData2.findAll('pre')

        self.alumno = tableData2.findAll(
            'font')[0].find('h3').find('font').text[17:].strip()
        self.especialidad = tableData2.find('b').text[14:].strip()
        self.inscrito, self.semestre = detalles[0].find(
            'b').text[10:11], detalles[0].find('b').text[-1:].strip()

        ingresoCretidosTextRow = detalles[1].find('b').text
        estadoActualTextRow = detalles[2].find('b').text
        self.ingreso = ' '.join(ingresoCretidosTextRow[9: 21].split()).strip()

        self.creditosTotales = ingresoCretidosTextRow[-3:].strip()
        self.creditosActuales = ingresoCretidosTextRow[ingresoCretidosTextRow.index(
            'Con')+4: ingresoCretidosTextRow.index('Con')+7].strip()

        self.sexo = estadoActualTextRow[7:8].strip()
        self.estadoActual = estadoActualTextRow.split(':')[2].strip()
        self.carga = self.extractCarga(table=tableData2)
        self.kardex = self.extractKardex(table=kardexTable)

    def extractKardex(self, table: BeautifulSoup):
        tabla = []
        mtableRows = table.findAll('tr')[1:]
        calis = []

        for tableRow in mtableRows:
            columns = tableRow.findAll('td')
            clave, materia, creditos, semestre, cali, oportunidad = [
                col.find('center').text.strip() for col in columns]
            calis.append(int(cali))
            tabla.append({'clave': clave, 'materia': materia, 'creditos': creditos, 'semestre': semestre,
                          'calificacion': cali, 'oportunidad': oportunidad})
        self.promedio = sum(calis) / len(calis)
        return tabla

    def extractCarga(self, table: BeautifulSoup):
        tabla = []
        mtable = table.find('table')
        mtablerows = mtable.findAll('tr')[1:]

        for tableRow in mtablerows:
            columns = tableRow.findAll('td')
            grupo = columns[0].find('font').text.strip()
            materia = columns[1].find('font').find('font').text.strip()
            calif = columns[2].find('font').find('font').text.strip()
            semana = {'l': {}, 'm': {}, 'x': {}, 'j': {}, 'v': {}}

            colSemanaIndex = 3
            for dia in semana:
                horaStr, aula = columns[colSemanaIndex].find(
                    'font').find('font').text.split('/')
                if len(horaStr) == 1 and not aula:
                    semana[dia] = "LIBRE"
                    continue

                horaStr = ('0'+horaStr, horaStr)[len(horaStr) == 4]

                horas = [horaStr[i:i+2] + ':00' for i in range(0, 4, 2)]
                
                semana[dia] = {'inicio': horas[0],
                               'fin': horas[1], 'aula': aula}
                colSemanaIndex = colSemanaIndex + 1

            tabla.append({'grupo': grupo, 'materia': materia,
                          'calif': calif, 'semana': semana})
        return tabla

    def getJSON(self):
        return {'nombre': self.alumno, 'no. control': self.noControl, 'especialidad': self.especialidad,
                'inscrito': self.inscrito, 'semestre': self.semestre, 'ingreso': self.ingreso,
                'creditos': self.creditosActuales, 'creditosTotales': self.creditosTotales,
                'sexo': self.sexo, 'estado': self.estadoActual, 'promedio': self.promedio, 'kardex': self.kardex, 'cursando': self.carga}
