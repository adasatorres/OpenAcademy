import xmlrpc.client as conn

HOST = '127.0.0.1'
PORT = 8069
DB = "odoo"
USER = "a.torres@binhex.es"
PASS = "d031da64c5f17370da606e5a1db9c6f38e0f7ed5"


root =  'http://{0}:{1}/xmlrpc/'.format(HOST,PORT)
uid = conn.ServerProxy(root + 'common').login(DB, USER, PASS)
sock = conn.ServerProxy(root + 'object')
sesiones = sock.execute_kw(DB, uid, PASS, 'openacademy.sesiones','search_read', [[]])

for sesion in sesiones:
    print('Nombre: {0:2}, Numero de asientos: {1:2}'.format(sesion['nombre'], sesion['numero_asientos'])
)

curso = sock.execute_kw(DB, uid, PASS, 'openacademy.cursos','search_read',[[('titulo', '=', 'pruebas')]])
print(curso)
args = {
    'nombre': 'PruebaWebservice',
    'numero_asientos': 40,
    'duracion': 10.5,
    'fecha_inicio': '2023-10-10',
    'fecha_fin': '2023-11-10',
    'num_asientos_ocupado' : 30,
    'curso_id' : curso[0]['id']
}

sock.execute(DB, uid, PASS, 'openacademy.sesiones','create',args)