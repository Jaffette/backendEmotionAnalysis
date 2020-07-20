import pyodbc
import json

server_address = 'localhost\sqlexpress'
database = 'emotion_analysis'
username = 'sa'
password = '12345'

try:
    cnxn = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + server_address + ';DATABASE=' + database + ';UID=' + username + ';PWD=' + password)

except Exception as ex:
    print("An error has occurred when connecting to SQL: ", ex)


def get_users_login(user, passw):
    try:
        cursor = cnxn.cursor()
        cursor.execute("""EXEC users_login @username=?,  @password=?, @success=0;""", user, passw)
        rol = cursor.fetchone()
        cursor.close()
        response = {"rol": rol[0], "identification": rol[1], "user_id": rol[2], "first_time": rol[3]}
        response = json.dumps(response)
        return response
    except Exception as login_error:
        return 'An error occurred while loggin in %s' % login_error


def get_professors():
    try:
        cursor = cnxn.cursor()
        cursor.execute("""EXEC get_professors @success = 0;""")
        professors = []
        for res in cursor.fetchall():
            course = {'id': res[0], 'identificacion': res[1], 'nombre': res[2], 'apellidos': res[3]}
            professors.append(course)
        cursor.close()
        response = {'response': professors}
        res = json.dumps(response)
        return res

    except Exception as error_professors:
        return 'An error occurred getting the professors %s' % error_professors


def register_user(user, passw, identification, name, last_name, phone_number, rol, first_time):
    try:
        cursor = cnxn.cursor()
        cursor.execute("""EXEC insert_users @username=?,  @password=?, @identification=?, @name=?, @last_name=?, 
        @phone_number=?, @rol=?, @first_time=?, @success=0;""",
                       user, passw, identification, name, last_name, phone_number, rol, first_time)
        cursor.commit()
        response = {'response': "ok"}
        res = json.dumps(response)
        cursor.close()
        return res
    except Exception as error_register_users:
        return 'An error occurred while registering %s' % error_register_users


def get_courses():
    try:
        cursor = cnxn.cursor()
        cursor.execute("""EXEC get_courses @success=0;""")
        courses = []
        for res in cursor.fetchall():
            course = {'id': res[0], 'codigo': res[1], 'nombre': res[2], 'creditos': res[3]}
            courses.append(course)
        cursor.close()
        response = {'response': courses}
        res = json.dumps(response)
        return res
    except Exception as error_courses:
        return 'An error occurred getting the courses %s' % error_courses


def insert_professors(identification, name, last_name):
    print(identification, name, last_name)
    try:
        cursor = cnxn.cursor()
        cursor.execute("""EXEC insert_profesors @identification = ?, @name = ?, @last_name = ?, @success = 0;""",
                       identification, name, last_name)
        cursor.commit()
        cursor.close()
        response = {'response': 'ok'}
        print(response)
        res = json.dumps(response)
        return res
    except Exception as error_register_professor:
        return 'An error occurred while registering %s' % error_register_professor


def insert_courses(course_code, course_name, credits):
    try:
        cursor = cnxn.cursor()
        cursor.execute("""insert_courses @course_code= ?, @course_name= ?, @credits=?, @success=0;""",
                       course_code, course_name, credits)
        cursor.commit()
        cursor.close()
        response = {'response': 'ok'}
        print(response)
        res = json.dumps(response)
        return res
    except Exception as error_register_professor:
        return 'An error occurred while registering %s' % error_register_professor


def get_courses_student(identification):
    try:
        cursor = cnxn.cursor()
        cursor.execute("""EXEC get_courses_student @identification = ?, @success = 0;""", identification)
        courses = []
        for res in cursor.fetchall():
            course = {'id': res[0], 'nombre': res[1], 'creditos': res[2], 'codigo': res[3], 'grupo': res[4]}
            courses.append(course)
        cursor.close()
        response = {'response': courses}
        print(response)
        res = json.dumps(response)
        return res
    except Exception as error_courses_student:
        return 'An error occurred getting the courses %s' % error_courses_student


def get_student_emotion(identification):
    try:
        cursor = cnxn.cursor()
        cursor.execute("""EXEC get_emotions_student @identification = ?, @success = 0;""", identification)
        courses = []
        for res in cursor.fetchall():
            course = {'emocion': res[0], 'curso': res[1], 'fecha': res[2].strftime("%y-%m-%d")}
            courses.append(course)
        cursor.close()
        response = {'response': courses}
        print(response)
        res = json.dumps(response)
        return res
    except Exception as error_emotions_course:
        return 'An error occurred getting the courses %s' % error_emotions_course


def get_course_emotion(course):
    try:
        cursor = cnxn.cursor()
        cursor.execute("""EXEC get_emotions_course @course_name = ?, @success = 0;""", course)
        courses = []
        for res in cursor.fetchall():
            course = {'emocion': res[1], 'reincidencia': res[0], }
            courses.append(course)
        cursor.close()
        response = {'response': courses}
        print(response)
        res = json.dumps(response)
        return res
    except Exception as error_emotions_course:
        return 'An error occurred getting the emotions of a course %s' % error_emotions_course


def register_emotions(emocion, fecha, id_student, course_id):
    try:
        cursor = cnxn.cursor()
        res = cursor.execute("""EXEC insert_emotions @emotion=?,@date=?,@student_id=?,@course_id = ?, @success = 0;""",
                             emocion, fecha, id_student, course_id)
        cursor.commit()
        cursor.close()
        response = {'response': "ok"}
        print(response)
        res = json.dumps(response)
        return res
    except Exception as error_emotions_course:
        return 'An error occurred getting the emotions of a course %s' % error_emotions_course


def insert_courses_students_professors(student_id, course_id, professor_id, group_number):
    try:
        cursor = cnxn.cursor()
        cursor.execute("""EXEC insert_courses_students_professors @student_id=?, @course_id=?, @professor_id=?, 
        @group_number=?, @success=0;""", student_id, course_id, professor_id, group_number)
        cursor.commit()
        cursor.close()
        response = {'response': 'ok'}
        print(response)
        res = json.dumps(response)
        return res
    except Exception as error_inserting:
        return 'An error occurred inserting the data %s' % error_inserting


def get_avg_emotions_student(student_id, start_date, end_date):
    try:
        cursor = cnxn.cursor()
        cursor.execute("""EXEC get_avg_emotions_student @student_id=?, @start_date=?, @end_date =?, @success=0;""",
                       student_id, start_date, end_date)
        courses = []
        for res in cursor.fetchall():
            course = {'emocion': res[0], 'reincidencia': res[1], }
            courses.append(course)
        cursor.close()
        response = {'response': courses}
        print(response)
        res = json.dumps(response)
        return res
    except Exception as avg_emotions_student:
        return 'An error occurred getting the avg of emotions of a student %s' % avg_emotions_student


def get_avg_emotions_courses(course_name,start_date,end_date):
    try:
        cursor = cnxn.cursor()
        cursor.execute("""EXEC get_avg_emotions_courses @course_name=?, @start_date=?, @end_date =?, @success=0;""", course_name,start_date,end_date)
        courses = []
        for res in cursor.fetchall():
            course = {'emocion': res[0], 'reincidencia': res[1], }
            courses.append(course)
        cursor.close()
        response = {'response': courses}
        print(response)
        res = json.dumps(response)
        return res
    except Exception as get_avg_emotions_courses:
        return 'An error occurred getting the avg of emotions of a course %s' %get_avg_emotions_courses