"""Base de Datos SQL - Uso de múltiples tablas"""

import datetime, sqlite3

from ejercicio_02 import agregar_persona
from ejercicio_04 import buscar_persona
from ejercicio_06 import reset_tabla


def agregar_peso(id_persona, fecha, peso):
    """Implementar la funcion agregar_peso, que inserte un registro en la tabla 
    PersonaPeso.

    Debe validar:
    - Que el ID de la persona ingresada existe (reutilizando las funciones ya 
        implementadas).
    - Que no existe de esa persona un registro de fecha posterior al que 
        queremos ingresar.

    Debe devolver:
    - ID del peso registrado.
    - False en caso de no cumplir con alguna validacion."""

    if buscar_persona(id_persona)==False:
        return False
    db = sqlite3.connect("mybase.db")
    cursor = db.cursor()
    sql='SELECT id, fecha FROM PersonaPeso WHERE IdPersona=?'
    cursor.execute(sql, [id_persona,])
    for row in cursor.fetchall():
        if datetime.datetime.strptime(row[1], '%Y-%m-%d %H:%M:%S')>= fecha:
            return False
    sql='INSERT INTO PersonaPeso (id, IdPersona, fecha, peso) VALUES (null, ?, ?, ?)'
    cursor.execute(sql, (id_persona, fecha, peso))
    db.commit()
    sql = 'SELECT id FROM PersonaPeso WHERE IdPersona=? and fecha=?'
    cursor.execute(sql, [id_persona, fecha])
    rs=cursor.fetchone()
    id= rs[0]
    cursor.close()
    db.close()
    return id


# NO MODIFICAR - INICIO
@reset_tabla
def pruebas():
    id_juan = agregar_persona('juan perez', datetime.datetime(1988, 5, 15), 32165498, 180)
    assert agregar_peso(id_juan, datetime.datetime(2018, 5, 26), 80) > 0
    # Test Id incorrecto
    assert agregar_peso(200, datetime.datetime(1988, 5, 15), 80) == False
    # Test Registro previo al 2018-05-26
    assert agregar_peso(id_juan, datetime.datetime(2018, 5, 16), 80) == False

if __name__ == '__main__':
    pruebas()
# NO MODIFICAR - FIN
