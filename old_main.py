import DbHelper
import json
from WebServiceReq import WebRequest
from WebScrapper import WebScrapper
from HorariosScrapper import HorariosScrapper
from operator import itemgetter
import time

from flask import Flask


def setConfiguration(db, _updateGrupos, _updateAlumnos):
    configCollection = db['Config']
    config = configCollection.find({})
    if config[0]:
        config = config[0]
        if config['updateGrupos'] == _updateGrupos and config['updateAlumnos'] == _updateAlumnos:
            return
        config['updateGrupos'] = _updateGrupos
        config['updateAlumnos'] = _updateAlumnos
        configCollection.update_one(
            {'_id': config['_id']}, {'$set': config})


def configuration(db, stopUpdateGrupos=None, stopUpdateAlumnos=None):
    configCollection = db['Config']
    config = configCollection.find({})
    results = {'updateGrupos': False, 'updateAlumnos': False}

    if config[0]:
        config = config[0]
        results['updateGrupos'] = config['updateGrupos']
        results['updateAlumnos'] = config['updateAlumnos']
    return results


def updateGrupos(db):
    gruposCollection = db['Grupos']
    req = WebRequest()
    req.loadHorarios()

    horariosScrapper = HorariosScrapper(req)
    horariosScrapper.extractAll()

    horariosFromWeb = sorted(horariosScrapper.horarios,
                             key=itemgetter('grupo'), reverse=False)

    # N^2 operation

    horariosDB = sorted(gruposCollection.find(),
                        key=itemgetter('grupo'), reverse=False)
    print(len(horariosFromWeb))

    for horarioDB in horariosDB:
        for horarioToFind in horariosFromWeb:
            if horarioToFind['grupo'] == horarioDB['grupo']:
                horariosFromWeb.remove(horarioToFind)

    print(len(horariosFromWeb))
    if len(horariosFromWeb):
        gruposCollection.insert_many(horariosFromWeb)


def updateAlumnos(db, noControl=None):
    alumnosCollection = db['Alumnos']
    fetchUnupdatedAlumnosQuery = {'requireUpdate': True}

    if noControl is not None:
        fetchUnupdatedAlumnosQuery['numeroControl'] = noControl

    alumnosUnupdated = alumnosCollection.find(fetchUnupdatedAlumnosQuery)

    for alumno in alumnosUnupdated:
        req = WebRequest(alumnoNoControl=alumno['numeroControl'])
        req.load()
        scrapper = WebScrapper(req, alumno['numeroControl'])
        scrapper.load()

        # UPDATE CARGA
        gruposCollection = db['Grupos']

        grupos = []
        # Check si los grupos existen, si no, insertarlos
        for grupo in scrapper.carga:
            # Retorna solamente el _id si lo encuentra
            _grupo = gruposCollection.find_one(
                {'grupo': grupo['grupo']}, {'_id': 1})

            if _grupo:
                _grupo['_id']
                _grupo['grade'] = grupo['calif']
                grupos.append(_grupo)

        alumno['carga'] = grupos
        alumno['kardex'] = scrapper.kardex
        alumno['nombre'] = scrapper.alumno
        alumno['especialidad'] = scrapper.especialidad
        alumno['inscrito'] = scrapper.inscrito
        alumno['semestre'] = scrapper.semestre
        alumno['ingreso'] = scrapper.ingreso
        alumno['creditosTotales'] = scrapper.creditosTotales
        alumno['creditosActuales'] = scrapper.creditosActuales
        alumno['sexo'] = scrapper.sexo
        alumno['promedio'] = scrapper.promedio
        alumno['estadoActual'] = scrapper.estadoActual

        alumno['requireUpdate'] = False
        alumnosCollection.update_one({'_id': alumno['_id']}, {'$set': alumno})
        # # No hay necesidad de guardar con insert_one

        # print(scrapper.promedio)


app = Flask(__name__)


@app.route("/reload")
def reload():
    database = DbHelper.connect()
    results = configuration(database)

    if results['updateGrupos'] == True:
        updateGrupos(database)
    if results['updateAlumnos'] == True:
        updateAlumnos(database)
    setConfiguration(database, False, False)

    return 'loaded OK'


@app.route('/reload/alumnos/<noControl>')
def reloadAlumno(noControl):
    database = DbHelper.connect()
    updateAlumnos(database, noControl)
    return 'ok'


@app.route('/reload/grupos')
def reloadGrupos():
    database = DbHelper.connect()

    updateGrupos(database)

    return 'Done'


@app.route('/')
def hi():
    return 'Hello world!'


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
