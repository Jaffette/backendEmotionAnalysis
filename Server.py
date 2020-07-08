from http.server import HTTPServer, BaseHTTPRequestHandler
import cgi
import conexionBaseDatos

class echoHandler(BaseHTTPRequestHandler):

    def do_OPTIONS(self):
        self.send_response(200, "ok")
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header("Access-Control-Allow-Headers", "X-Requested-With")

    def do_GET(self):

        ctype, pdict = cgi.parse_header(self.headers.get('content-type'))
        pdict['boundary'] = bytes(pdict['boundary'], "utf-8")
        content_len = int(self.headers.get('content-length'))
        pdict["CONTENT-LENGTH"] = content_len

        if self.path.endswith('/getCursos'):
            response = conexionBaseDatos.get_courses()
            self.send_response(200,'ok')
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header('content-type', 'application/json')

            self.end_headers()
            self.wfile.write(response.encode())

        if self.path.endswith('/getCursosEstudiate'):
            if ctype == 'multipart/form-data':
                fields = cgi.parse_multipart(self.rfile, pdict)  # En pdict se encuentran todos los atributos enviados
                identification = fields.get('identification')[0]
                response = conexionBaseDatos.get_courses_student(identification)
                self.send_response(200)
                self.send_header('content-type', 'application/json')
                self.end_headers()
                self.wfile.write(response.encode())

        if self.path.endswith('/filtrarEstudiante'):
            if ctype == 'multipart/form-data':
                fields = cgi.parse_multipart(self.rfile, pdict)  # En pdict se encuentran todos los atributos enviados
                identification = fields.get('identification')[0]
                response = conexionBaseDatos.get_student_emotion(identification)
                print(response)
                self.send_response(200)
                self.send_header('content-type', 'application/json')
                self.end_headers()
                self.wfile.write(response.encode())

        if self.path.endswith('/getEmocionesCurso'):
            if ctype == 'multipart/form-data':
                fields = cgi.parse_multipart(self.rfile, pdict)  # En pdict se encuentran todos los atributos enviados
                curso = fields.get('curso')[0]
                response = conexionBaseDatos.get_course_emotion(curso)
                print(response)
                self.send_response(200)
                self.send_header('content-type', 'application/json')
                self.end_headers()
                self.wfile.write(response.encode())



    def do_POST(self):
        ctype, pdict = cgi.parse_header(self.headers.get('content-type'))
        pdict['boundary'] = bytes(pdict['boundary'], "utf-8")
        content_len = int(self.headers.get('content-length'))
        pdict["CONTENT-LENGTH"] = content_len

        if self.path.endswith('/iniciarSesion'):
            if ctype == 'multipart/form-data':
                fields = cgi.parse_multipart(self.rfile, pdict) #En pdict se encuentran todos los atributos enviados
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




def main():
    PORT = 8080
    server_address = ('0.0.0.0', PORT)
    server = HTTPServer(server_address, echoHandler)
    print ('server running on port %s' %PORT)
    server.serve_forever()

if __name__ == '__main__':
    main()