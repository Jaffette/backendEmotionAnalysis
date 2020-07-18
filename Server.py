from http.server import HTTPServer, BaseHTTPRequestHandler
import cgi
import conexionBaseDatos
import json
from urllib.parse import parse_qs
import datetime

class EchoHandler(BaseHTTPRequestHandler):

    def _send_cors_headers(self):
        """ Sets headers required for CORS """
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET,POST,OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "x-api-key,Content-Type")

    def do_OPTIONS(self):
        self.send_response(200)
        self._send_cors_headers()
        self.end_headers()


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

            if path == '/getProfessors':
                response = conexionBaseDatos.get_professors()
                self.send_response(200, 'ok')
                self.send_header("Access-Control-Allow-Origin", "*")
                self.send_header('content-type', 'application/json')
                self.end_headers()
                self.wfile.write(response.encode())

            if path == '/getCursosEstudiante':
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

        if self.path.endswith('/iniciarSesion'):
            info_received = json.loads(self.rfile.read(length))
            username = info_received['username']
            password = info_received['password']
            rol = conexionBaseDatos.get_users_login(username, password)
            self.send_response(200)
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header('content-type', 'application/json')
            self.end_headers()
            self.wfile.write(rol.encode())

        if self.path.endswith('/registro'):
            info_received = json.loads(self.rfile.read(length))
            print(info_received)
            #info_received = info_received['params']
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
            self.send_header("Access-Control-Allow-Origin", "*")
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
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header('content-type', 'text')
            self.end_headers()
            self.wfile.write('registrado'.encode())

        if self.path.endswith('/registrarEmociones'):
            info_received = json.loads(self.rfile.read(length))
            print(info_received)
            student_id = info_received['student_id']
            emotion = info_received['emotion']
            course_id = info_received['course_id']
            fecha = info_received['fecha']
            date_object = datetime.date.today()
            print("tipo",type(fecha))
            course_id = info_received['course_id']
            response = conexionBaseDatos.register_emotions(emotion,fecha,student_id,course_id,)
            
            self.send_response(200, 'ok')
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header('content-type', 'application/json')
            self.end_headers()
            self.wfile.write(response.encode())

        if self.path.endswith('/registrarCursoEstudiante'):
            info_received = json.loads(self.rfile.read(length))
            print("Aloha")
            student_id = info_received['student_id']
            course_id = info_received['course_id']
            professor_id = info_received['professor_id']
            group_number = info_received['group_number']
            response = conexionBaseDatos.insert_courses_students_professors(student_id, course_id, professor_id, group_number)
            self.send_response(200, 'ok')
            self.send_header("Access-Control-Allow-Origin", "*")
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
