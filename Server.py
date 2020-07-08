from http.server import HTTPServer, BaseHTTPRequestHandler
import cgi
import conexionBaseDatos
import json
from urllib.parse import parse_qs


class EchoHandler(BaseHTTPRequestHandler):

    def do_OPTIONS(self):
        self.send_response(200, "ok")
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header("Access-Control-Allow-Headers", "X-Requested-With")

    def query_get(self, queryData, key, default=""):
        """Helper for getting values from a pre-parsed query string"""
        return queryData.get(key, [default])[0]

    def do_GET(self):
        path, _, query_string = self.path.partition('?')
        query = parse_qs(query_string)
        response = None
        print(u"[START]: Received GET for %s with query: %s" % (path, query))

        try:
            if path == '/getCursos':
                response = conexionBaseDatos.get_courses()
                self.send_response(200, 'ok')
                self.send_header("Access-Control-Allow-Origin", "*")
                self.send_header('content-type', 'application/json')
                self.end_headers()
                self.wfile.write(response.encode())

            if path == '/getCursosEstudiate':
                identification = query['identification'][0]
                response = conexionBaseDatos.get_courses_student(identification)
                self.send_response(200, 'ok')
                self.send_header("Access-Control-Allow-Origin", "*")
                self.send_header('content-type', 'application/json')
                self.end_headers()
                self.wfile.write(response.encode())

            if path == '/filtrarEstudiante':
                identification = query['identification'][0]
                response = conexionBaseDatos.get_student_emotion(identification)
                self.send_response(200, 'ok')
                self.send_header("Access-Control-Allow-Origin", "*")
                self.send_header('content-type', 'application/json')
                self.end_headers()
                self.wfile.write(response.encode())

            if path == '/getEmocionesCurso':
                curso = query['curso'][0]
                response = conexionBaseDatos.get_course_emotion(curso)
                print(response)
                self.send_response(200, 'ok')
                self.send_header("Access-Control-Allow-Origin", "*")
                self.send_header('content-type', 'application/json')
                self.end_headers()
                self.wfile.write(response.encode())

        except Exception as err:
            self.send_error(err)

    def do_POST(self):

        ctype, pdict = cgi.parse_header(self.headers.get('content-type'))
        length = int(self.headers.get('content-length'))
        # refuse to receive non-json content

        if ctype != 'application/json':
            print("not a json")
            self.send_response(400)
            self.end_headers()
            return

        if self.path.endswith('/test'):
            info_received = json.loads(self.rfile.read(length))
            # add a property to the object, just to mess with data
            info_received['received'] = 'ok'
            # send the info_received back
            self.send_response(200)
            self.send_header('content-type', 'application/json')
            self.end_headers()
            self.wfile.write(info_received['received'].encode())

        if self.path.endswith('/iniciarSesion'):
            info_received = json.loads(self.rfile.read(length))
            username = info_received['username']
            password = info_received['password']
            rol = conexionBaseDatos.get_users_login(username, password)
            self.send_response(200)
            self.send_header('content-type', 'application/json')
            self.end_headers()
            self.wfile.write(rol.encode())

        if self.path.endswith('/registro'):
            info_received = json.loads(self.rfile.read(length))
            username = info_received['username']
            password = info_received['password']
            identification = info_received['identification']
            name = info_received['name']
            last_name = info_received['last_name']
            phone_number = info_received['phone_number']
            rol = info_received['rol']
            first_time = True
            response = conexionBaseDatos.register_user(username, password, identification, name,
                                                       last_name, phone_number, rol, first_time)
            self.send_response(200)
            self.send_header('content-type', 'text')
            self.end_headers()
            self.wfile.write(response.encode())

        if self.path.endswith('/registrarProfesor'):
            info_received = json.loads(self.rfile.read(length))
            identification = info_received['identification']
            name = info_received['name']
            last_name = info_received['last_name']
            conexionBaseDatos.insert_professors(identification, name, last_name)
            self.send_response(200)
            self.send_header('content-type', 'text')
            self.end_headers()
            self.wfile.write('registrado'.encode())

        if self.path.endswith('/registrarEmociones'):
            info_received = json.loads(self.rfile.read(length))
            id_student = info_received['id_student']
            emocion = info_received['emocion']
            profesor_curso = info_received['profesor']
            fecha = info_received['fecha']
            course_id = info_received['course_id']
            response = conexionBaseDatos.register_emotions(emocion,id_student,profesor_curso,course_id,fecha)
            self.send_response(200, 'ok')
            self.send_header('content-type', 'application/json')
            self.end_headers()
            self.wfile.write(response.encode())


def main():
    PORT = 8080
    server_address = ('0.0.0.0', PORT)
    server = HTTPServer(server_address, EchoHandler)
    print('server running on port %s' % PORT)
    server.serve_forever()


if __name__ == '__main__':
    main()
