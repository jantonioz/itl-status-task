import requests


class WebRequest:
    def __init__(self, alumnoNoControl=0):
        self.homeURL = 'http://apps.itlalaguna.edu.mx/servicios/escolares/estatus_alumno/prepcon.asp'
        self.direccionaURL = 'http://apps.itlalaguna.edu.mx/servicios/escolares/estatus_alumno/direcciona.asp'
        self.kardexURL = 'http://apps.itlalaguna.edu.mx/servicios/escolares/estatus_alumno/kardex.asp'
        self.horarioURL = 'http://apps.itlalaguna.edu.mx/servicios/academicos/horario_materias/horarios.asp'
        self.session = requests.Session()
        self.home_body = {'cCONTROL': alumnoNoControl,
                          'cCONTRASENA': '', 'BotConsultar': 'Consultar'}
        self.cursando_body = {'DOPCIONES': 'cursando'}
        self.kardex_body = {'DOPCIONES': 'kardex'}
        
        self.horariosEspecialidades = [1, 2, 3, 4, 5, 6, 7, 8, 9, 'Z']

    def load(self):
        self.home = self.session.post(self.homeURL, data=self.home_body)
        self.cursando = self.session.post(
            self.direccionaURL, data=self.cursando_body)
        self.kardex = self.session.get(self.kardexURL)

    def horarioGetBody(self, especialidad):
        return {'ESPECIALIDAD': especialidad, 'BotConsultar': 'Consultar'}

    def loadHorarios(self):
        self.horariosList = []
        for especialidadCode in self.horariosEspecialidades:
            horarioEspecialidad = self.session.post(
                self.horarioURL, data=self.horarioGetBody(especialidadCode)).text
            self.horariosList.append(
                {'code': especialidadCode, 'text': horarioEspecialidad})

        return self.horariosList

    def getKardexData(self):
        return self.kardex.text

    def getHomeData(self):
        return self.home.text

    def getCursandoData(self):
        return self.cursando.text
