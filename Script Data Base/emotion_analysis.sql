CREATE DATABASE emotion_analysis;
GO

USE emotion_analysis
GO

CREATE TABLE users(
	user_id               INT IDENTITY(1,2)       NOT NULL,
	username              VARCHAR(50)             NOT NULL,
	password              VARCHAR(50)             NOT NULL,
	identification        VARCHAR(10)             NOT NULL,
	name                  VARCHAR(50)             NOT NULL,
	last_name             VARCHAR(100)            NOT NULL,
	phone_number          VARCHAR(8)              NOT NULL,
	rol                   CHAR(1)                 NOT NULL,
	first_time            BIT                     NOT NULL,
	UNIQUE(identification),
	PRIMARY KEY(user_id),
	CHECK  (identification LIKE '[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]'),
	CHECK  (phone_number   LIKE '[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]')
);
GO

CREATE TABLE professors(
	professor_id    INT IDENTITY(1,1) NOT NULL,
	identification  VARCHAR(9)        NOT NULL,
	name            VARCHAR(50)       NOT NULL,
	last_name       VARCHAR(100)      NOT NULL,

	PRIMARY KEY(professor_id)
);
GO

CREATE TABLE courses(
	course_id        INT IDENTITY(1,1) NOT NULL,
	course_code      VARCHAR(10) NOT NULL,
	course_name      VARCHAR(100) NOT NULL,
	credits          TINYINT NOT NULL,

	PRIMARY KEY (course_id)
);
GO

CREATE TABLE courses_students_professors(
	id_courses_students        INT IDENTITY(1,1)  NOT NULL,
	student_id                 INT                NOT NULL,
	course_id                  INT                NOT NULL,
	professor_id               INT                NOT NULL,
	group_number               TINYINT            NOT NULL,

	PRIMARY KEY (id_courses_students),
	FOREIGN KEY (student_id)   REFERENCES users(user_id),
	FOREIGN KEY (course_id)    REFERENCES  courses(course_id),
	FOREIGN KEY (professor_id) REFERENCES professors(professor_id)

);
GO

CREATE TABLE emotions(
	emotion_id         INT IDENTITY(1,1) NOT NULL,
	emotion            VARCHAR(20)       NOT NULL,
	date                VARCHAR(10)       NOT NULL,
	student_id         INT               NOT NULL,
	course_id          INT               NOT NULL,

	PRIMARY KEY (emotion_id),
	FOREIGN KEY (student_id) REFERENCES users(user_id),
	FOREIGN KEY (course_id) REFERENCES courses_students_professors(id_courses_students)
)
GO

-------------------------------------------------------------------------------------------------
CREATE PROC insert_users
(
       @username                   VARCHAR(50)   ,
       @password                   VARCHAR(50)   ,
       @identification             VARCHAR(50)   ,
       @name                       VARCHAR(50)   ,
	   @last_name                  VARCHAR(100)  ,
	   @phone_number               VARCHAR(9)    ,
	   @rol						   CHAR(1)       ,
	   @first_time                 BIT           ,
	   @success					   BIT OUTPUT
)

AS
BEGIN
	 BEGIN TRY
		 INSERT INTO dbo.users (username, password, identification, name, last_name, phone_number, rol, first_time) VALUES (@username, @password, @identification, @name, @last_name, @phone_number, @rol, @first_time)
		 SET @success = 1
	 END TRY
	 BEGIN CATCH
		SET @success = 0
	END CATCH
END
GO

-------------------------------------------------------------------------------------------------
CREATE PROC insert_profesors
(
       @identification             VARCHAR(9)   ,
       @name                       VARCHAR(50)   ,
	   @last_name                  VARCHAR(100)  ,
	   @success					   BIT OUTPUT

)

AS
BEGIN
	 BEGIN TRY
		 INSERT INTO dbo.professors(identification, name, last_name) VALUES (@identification, @name, @last_name)
		 SET @success = 1
	 END TRY
	 BEGIN CATCH
		SET @success = 0
	END CATCH
END
GO
-------------------------------------------------------------------------------------------------
CREATE PROC insert_courses
(
       @course_code             VARCHAR(10)   ,
       @course_name             VARCHAR(100)  ,
	   @credits                 TINYINT       ,
	   @success					BIT OUTPUT

)

AS
BEGIN
	 BEGIN TRY
		 INSERT INTO dbo.courses(course_code, course_name, credits) VALUES (@course_code, @course_name, @credits)
		 SET @success = 1
	 END TRY
	 BEGIN CATCH
		SET @success = 0
	END CATCH
END
GO
-------------------------------------------------------------------------------------------------
CREATE PROC insert_courses_students_professors
(
       @student_id              INT        ,
       @course_id               INT        ,
	   @professor_id            INT        ,
	   @group_number            TINYINT    ,
	   @success					BIT OUTPUT

)


AS
BEGIN
			IF((SELECT COUNT(*) FROM users WHERE user_id = @student_id AND rol='E')>0 AND (SELECT COUNT(*) FROM courses WHERE course_id = @course_id)>0 AND (SELECT COUNT(*) FROM professors WHERE professor_id = @professor_id)>0)
				BEGIN
					INSERT INTO dbo.courses_students_professors(student_id,course_id, professor_id,group_number) VALUES (@student_id,@course_id,@professor_id, @group_number)
					SET @success = 1
				END
			ELSE
				SET @success = 0

END
GO
-------------------------------------------------------------------------------------------------
CREATE OR ALTER PROC insert_emotions
(
     @emotion                 VARCHAR(20) ,
     @date                    VARCHAR(10) ,
	   @student_id              INT         ,
	   @course_id               INT         ,
	   @success					BIT OUTPUT

)

AS
BEGIN
			IF((SELECT COUNT(*) FROM users WHERE user_id = @student_id AND rol='E')>0 AND (SELECT COUNT(*) FROM courses_students_professors WHERE course_id = @course_id)>0 )
				BEGIN
					INSERT INTO dbo.emotions(emotion,date,student_id,course_id) VALUES (@emotion,@date,@student_id,@course_id)
					SET @success = 1
				END
			ELSE
				SET @success = 0

END
GO

-------------------------------------------------------------------------------------------------
CREATE PROC get_courses
@success BIT OUTPUT
AS
BEGIN
	SET @success=1
	SELECT * from courses;
END
GO
-------------------------------------------------------------------------------------------------
CREATE PROC users_login
(
	@username VARCHAR(50),
	@password VARCHAR(50),
	@success BIT OUTPUT
)

AS
BEGIN
	IF EXISTS (SELECT * from users WHERE username = @username and password = @password)
	BEGIN
		SET @success = 1
		SELECT rol, identification, user_id, first_time from users where username = @username and password = @password
	END

END
GO
-------------------------------------------------------------------------------------------------
CREATE OR ALTER PROC get_courses_student
(
	@identification  VARCHAR(10),
	@success		 BIT OUTPUT
)
AS
BEGIN
	BEGIN TRY

		SET @success = 1
		SELECT courses.course_id, courses.course_name,courses.credits, course_code, courses_students_professors.group_number
		FROM courses  INNER JOIN courses_students_professors
		ON (courses.course_id = courses_students_professors.course_id) INNER JOIN users
		ON (users.user_id = courses_students_professors.student_id)
		WHERE users.identification = @identification

	END TRY
	BEGIN CATCH
		SET @success = 0
	END CATCH
END
GO
-------------------------------------------------------------------------------------------------
CREATE PROC get_emotions_student
(
	@identification  VARCHAR(10),
	@success		 BIT OUTPUT
)
AS
BEGIN
	BEGIN TRY

		SET @success = 1
		SELECT emotions.emotion, courses.course_name, CAST(emotions.date AS DATE) AS date
		FROM EMOTIONS INNER JOIN users
		ON (users.user_id = emotionS.student_id) INNER JOIN courses
		ON (emotions.course_id = courses.course_id)
		WHERE users.identification = @identification

	END TRY
	BEGIN CATCH
		SET @success = 0
	END CATCH
END
GO
-------------------------------------------------------------------------------------------------
CREATE PROC get_emotions_course
(
	@course_name     VARCHAR(100),
	@success		 BIT OUTPUT
)
AS
BEGIN
	BEGIN TRY

		SET @success = 1
		SELECT count(emotions.emotion) as emotion_records, emotions.emotion
		FROM EMOTIONS INNER JOIN users
		ON (users.user_id = emotionS.student_id) INNER JOIN courses
		ON (emotions.course_id = courses.course_id)
		WHERE courses.course_name LIKE @course_name+'%' GROUP BY emotions.emotion

	END TRY
	BEGIN CATCH
		SET @success = 0
	END CATCH
END
GO
------------------------------------------------------------------------------------
CREATE PROC get_emotions_professor
(
	@professor     VARCHAR(100),
	@success		 BIT OUTPUT
)
AS
BEGIN
	BEGIN TRY

		SET @success = 1
		SELECT count( emotions.emotion)/2 as emotion_records, emotions.emotion
		FROM emotions INNER JOIN courses_students_professors
		ON (emotions.student_id = courses_students_professors.student_id) INNER JOIN professors
		ON (courses_students_professors.professor_id = professors.professor_id)
		WHERE professors.name LIKE @professor+'%' GROUP BY emotions.emotion

	END TRY
	BEGIN CATCH
		SET @success = 0
	END CATCH
END
GO
------------------------------------------------------------------------------------
CREATE PROC get_professors
@success BIT OUTPUT
AS
BEGIN
	SET @success=1
	SELECT * from professors;
END
GO
-------------------------------------------------------------------------------------------------
CREATE PROC get_avg_emotions_student
(
	@student_id     VARCHAR(10),
	@start_date     VARCHAR(10),
	@end_date       VARCHAR(10),
	@success		 BIT OUTPUT
)
AS
BEGIN
	BEGIN TRY

		SET @success = 1
		SELECT emotions.emotion,count(*) as Mayor
		FROM emotions INNER JOIN users
		ON (users.user_id = emotionS.student_id) INNER JOIN courses
		ON (emotions.course_id = courses.course_id)
		WHERE users.identification = @student_id and emotions.date between @start_date and 	@end_date GROUP BY emotions.emotion ORDER BY Mayor desc

	END TRY
	BEGIN CATCH
		SET @success = 0
	END CATCH
END
GO
-------------------------------------------------------------------------------------------------
CREATE PROC get_avg_emotions_courses
(
	@course_name     VARCHAR(10),
	@start_date     VARCHAR(10),
	@end_date       VARCHAR(10),
	@success		 BIT OUTPUT
)
AS
BEGIN
	BEGIN TRY

		SET @success = 1
		SELECT emotions.emotion,count(*) as Mayor
		FROM emotions INNER JOIN courses
		ON (emotions.course_id = courses.course_id)
		WHERE courses.course_name LIKE @course_name and emotions.date between @start_date and 	@end_date GROUP BY emotions.emotion ORDER BY Mayor desc

	END TRY
	BEGIN CATCH
		SET @success = 0
	END CATCH
END
GO
 ------------------------------------------------------------------------------------------------ PRUEBAS DE PROCEDURES -------------------------------------------------------------------------------------
EXEC insert_users @username='jaffo98',@password='123',@identification= '0504200129',@name='Jaffette',@last_name='Solano Arias', @phone_number='72974674',@rol='E', @first_time=1, @success=0;
GO
EXEC insert_profesors @identification='504200128', @name='Marvin', @last_name = 'Campos', @success=0;
GO
EXEC insert_courses @course_code='IC-1403',@course_name='POO',@credits=4,@success=0;
GO
EXEC insert_courses_students_professors @student_id=1, @course_id=1, @professor_id=1, @group_number=50, @success=0;
GO
EXEC insert_emotions @emotion='Triste',@date='2020-07-10',@student_id=1,@course_id = 1, @success = 0;
GO
EXEC insert_emotions @emotion='Feliz',@date='2020-07-10',@student_id=1,@course_id = 1, @success = 0;
GO
EXEC insert_emotions @emotion='neutral',@date='2020-07-10',@student_id=1,@course_id = 1, @success = 0;
GO
EXEC insert_emotions @emotion='neutral',@date='2020-07-10',@student_id=1,@course_id = 1, @success = 0;
GO
EXEC insert_emotions @emotion='neutral',@date='2020-07-11',@student_id=1,@course_id = 1, @success = 0;
GO
EXEC insert_emotions @emotion='neutral',@date='2020-07-12',@student_id=1,@course_id = 1, @success = 0;
GO
EXEC users_login @username='jaffo98',  @password='123', @success=1;
GO
EXEC get_courses_student @identification = '0504200129', @success = 0;
GO
EXEC get_emotions_student @identification = '0504200129', @success = 0;
GO
EXEC get_emotions_course @course_name = 'es', @success = 0;
GO
EXEC get_emotions_professor @professor= 'Marv', @success = 0;
GO
EXEC get_professors @success = 0;
GO
EXEC  get_avg_emotions_student @student_id='0504200129', @start_date='2020-07-11', @end_date = '2020-07-12', @success=0;
GO
EXEC  get_avg_emotions_courses @course_name='POO', @start_date='2020-07-10', @end_date = '2020-07-12', @success=0;
GO

use emotion_analysis
SELECT * FROM users
SELECT * FROM professors
SELECT * FROM courses
SELECT * FROM courses_students_professors
SELECT * FROM emotions



