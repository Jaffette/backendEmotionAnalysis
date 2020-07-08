from http.server import HTTPServer, BaseHTTPRequestHandler
import cgi
import conexionBaseDatos
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
        pdict['boundary'] = bytes(pdict['boundary'], "utf-8")
        content_len = int(self.headers.get('content-length'))
        pdict["CONTENT-LENGTH"] = content_len

        if self.path.endswith('/iniciarSesion'):
            if ctype == 'multipart/form-data':
                fields = cgi.parse_multipart(self.rfile, pdict)  # En pdict se encuentran todos los atributos enviados
                username = fields.get('username')[0]
                password = fields.get('password')[0]
                rol = conexionBaseDatos.get_users_login(username, password)
                self.send_response(200)
                self.send_header('content-type', 'application/json')
                self.end_headers()
                self.wfile.write(rol.encode())

        if self.path.endswith('/registro'):
            if ctype == 'multipart/form-data':
                fields = cgi.parse_multipart(self.rfile, pdict)  # En pdict se encuentran todos los atributos enviados
                username = fields.get('username')[0]
                password = fields.get('password')[0]
                identification = fields.get('identification')[0]
                name = fields.get('name')[0]
                last_name = fields.get('last_name')[0]
                phone_number = fields.get('phone_number')[0]
                rol = fields.get('rol')[0]
                first_time = True
                response = conexionBaseDatos.register_user(username, password, identification, name,
                                                           last_name, phone_number, rol, first_time)
                self.send_response(200)
                self.send_header('content-type', 'text')
                self.end_headers()
                self.wfile.write(response.encode())

        if self.path.endswith('/registrarProfesor'):
            if ctype == 'multipart/form-data':
                fields = cgi.parse_multipart(self.rfile, pdict)  # En pdict se encuentran todos los atributos enviados
                identification = fields.get('identification')[0]
                name = fields.get('name')[0]
                last_name = fields.get('last_name')[0]
                conexionBaseDatos.insert_professors(identification, name, last_name)
                self.send_response(200)
                self.send_header('content-type', 'text')
                self.end_headers()
                self.wfile.write('registrado'.encode())

        if self.path.endswith('/registrarEmociones'):
            if ctype == 'multipart/form-data':
                fields = cgi.parse_multipart(self.rfile, pdict)  # En pdict se encuentran todos los atributos enviados
                id_student = fields.get('id_student')[0]
                emocion = fields.get('emocion')[0]
                profesor_curso = fields.get('profesor')[0]
                fecha = fields.get('fecha')[0]

                response = conexionBaseDatos.register_emotions(emocion,id_student,profesor_curso,fecha)
                self.send_response(200, 'ok')
                self.send_header('content-type', 'application/json')
                self.end_headers()
                self.wfile.write(rol.encode())


def main():
    PORT = 8080
    server_address = ('0.0.0.0', PORT)
    server = HTTPServer(server_address, EchoHandler)
    print('server running on port %s' % PORT)
    server.serve_forever()


if __name__ == '__main__':
    main()
