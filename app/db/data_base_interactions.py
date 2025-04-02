import psycopg

def get_connection():
    """Создаёт и возвращает подключение к базе данных"""
    return psycopg.connect(
    dbname="schooldb",
    user="sylv",
    password="Selessal",
    host="localhost",
    port="5432"
    )

def create_tables(conn):

    cur = conn.cursor()

    # Создание таблицы

    
    tables_sql = """

CREATE TABLE IF NOT EXISTS Subjects (
    subject_id SERIAL PRIMARY KEY,
    subject_name VARCHAR(100) NOT NULL UNIQUE
);

    CREATE TABLE IF NOT EXISTS Teachers (
    teacher_id SERIAL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    subject_id INT REFERENCES Subjects(subject_id) ON DELETE SET NULL
);


CREATE TABLE IF NOT EXISTS Classes (
    class_id SERIAL PRIMARY KEY,
    class_name VARCHAR(10) NOT NULL,
    teacher_id INT REFERENCES Teachers(teacher_id) ON DELETE SET NULL
);

    CREATE TABLE IF NOT EXISTS Students (
    student_id SERIAL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    birth_date DATE NOT NULL,
    gender VARCHAR(10) CHECK (gender IN ('Male', 'Female', 'Other')),
    class_id INT REFERENCES Classes(class_id) ON DELETE SET NULL
);



CREATE TABLE IF NOT EXISTS Grades (
    grade_id SERIAL PRIMARY KEY,
    student_id INT REFERENCES Students(student_id) ON DELETE CASCADE,
    subject_id INT REFERENCES Subjects(subject_id) ON DELETE CASCADE,
    grade DECIMAL(3,1) CHECK (grade >= 0 AND grade <= 10),
    date_received DATE NOT NULL
);
"""

    cur.execute(tables_sql)

    conn.commit()
    
    # Закрытие соединения
    cur.close()
    conn.close()

def add_student(conn, first_name, last_name, birth_date, gender, class_id):
    """Добавляет студента в базу данных и возвращает его ID"""
    request_text = """
    INSERT INTO Students (first_name, last_name, birth_date, gender, class_id)
    VALUES (%s, %s, %s, %s, %s) RETURNING student_id;
    """
    with conn.cursor() as cur:
        cur.execute(request_text, (first_name, last_name, birth_date, gender, class_id))
        student_id = cur.fetchone()[0]
        conn.commit()  # Фиксируем изменения
    return student_id
    
def get_students(conn):
    """Получает список студентов"""
    with conn.cursor() as cur:
        cur.execute("SELECT student_id, first_name, last_name, birth_date, gender FROM Students")
        return cur.fetchall()


def get_students_in_definite_class(conn, class_id):
    """Получает список студентов"""
    with conn.cursor() as cur:
        cur.execute("SELECT student_id, first_name, last_name, birth_date, gender FROM Students WHERE class_id = %s", (class_id,))
        return cur.fetchall()

    
def add_class(conn, class_name, teacher_id):
    """Добавляет класс в базу данных"""
    with conn.cursor() as cur:
        cur.execute("INSERT INTO Classes (class_name, teacher_id) VALUES (%s, %s) RETURNING class_id;", (class_name, teacher_id))
        class_id = cur.fetchone()[0]
        conn.commit()
    return class_id

def get_classes(conn):
    """Получает список классов с их ID и полным именем преподавателя"""

    with conn.cursor() as cur:
        cur.execute("""
            SELECT c.class_id, 
                   c.class_name, 
                   COALESCE(t.first_name || ' ' || t.last_name, 'Нет преподавателя') AS teacher_name
            FROM Classes c
            LEFT JOIN Teachers t ON c.teacher_id = t.teacher_id;
        """)
        classes = cur.fetchall()  # Список кортежей (class_id, class_name, teacher_name)

    return classes

    
def add_subject(conn, subject_name):
    """Добавляет предмет"""
    with conn.cursor() as cur:
        cur.execute("INSERT INTO Subjects (subject_name) VALUES (%s) RETURNING subject_id;", (subject_name,))
        subject_id = cur.fetchone()[0]
        conn.commit()
    return subject_id

def add_teacher(conn, first_name, last_name, subject_id):
    """Добавляет учителя"""
    with conn.cursor() as cur:
        cur.execute("""
        INSERT INTO Teachers (first_name, last_name, subject_id) 
        VALUES (%s, %s, %s) RETURNING teacher_id;
        """, (first_name, last_name, subject_id))
        teacher_id = cur.fetchone()[0]
        conn.commit()
    return teacher_id

def get_teachers(conn):
    """Получает список всех учителей с их ID, именем, фамилией, ID и названием предмета"""
    with conn.cursor() as cur:
        try:
            cur.execute("""
                SELECT t.teacher_id, 
                       t.first_name || ' ' || t.last_name AS full_name, 
                       COALESCE(CAST(s.subject_id AS TEXT), 'Нет предмета') AS subject_id,
                       COALESCE(s.subject_name, 'Без предмета') AS subject_name
                FROM Teachers t
                LEFT JOIN Subjects s ON t.subject_id = s.subject_id;
            """)
            return cur.fetchall()
        except Exception as e:
            print("Ошибка при выполнении SQL-запроса:", e)
            return []


def clear_database(conn):
    """Удаляет все данные из базы, но сохраняет структуру таблиц"""
    with conn.cursor() as cur:
        cur.execute("""
            TRUNCATE TABLE Grades, Students, Classes, Teachers, Subjects 
            RESTART IDENTITY CASCADE;
        """)
        conn.commit()
    print("Все данные удалены.")

def get_subjects(conn):
    """Получает список всех предметов с их ID и названиями"""
    with conn.cursor() as cur:
        cur.execute("SELECT subject_id, subject_name FROM Subjects;")
        return cur.fetchall()  # Список кортежей (subject_id, subject_name)

def add_grade(conn, student_id, subject_id, grade, date_received):
    """Добавляет оценку студенту по предмету"""
    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO Grades (student_id, subject_id, grade, date_received)
            VALUES (%s, %s, %s, %s) RETURNING grade_id;
        """, (student_id, subject_id, grade, date_received))
        grade_id = cur.fetchone()[0]
        conn.commit()
    return grade_id


def get_all_grades(conn):
    """Получает список всех оценок"""
    with conn.cursor() as cur:
        cur.execute("""
            SELECT g.grade_id, 
                   s.first_name || ' ' || s.last_name AS student_name, 
                   sub.subject_name, 
                   g.grade, 
                   g.date_received
            FROM Grades g
            JOIN Students s ON g.student_id = s.student_id
            JOIN Subjects sub ON g.subject_id = sub.subject_id;
        """)
        return cur.fetchall()


def get_student_grades_by_period(conn, student_id, start_date, end_date):
    """Получает оценки конкретного ученика за указанный период"""
    with conn.cursor() as cur:
        cur.execute("""
            SELECT sub.subject_name, g.grade, g.date_received
            FROM Grades g
            JOIN Subjects sub ON g.subject_id = sub.subject_id
            WHERE g.student_id = %s AND g.date_received BETWEEN %s AND %s
            ORDER BY g.date_received;
        """, (student_id, start_date, end_date))
        return cur.fetchall()
    
def get_grade_distribution(class_id):
    """
    Функция выполняет запрос к PostgreSQL и возвращает распределение оценок по группам для указанного класса.
    :param class_id: ID класса
    :return: Словарь с распределением оценок {"Отлично": 5, ...}
    """
    query = """
        SELECT 
            CASE 
                WHEN grade >= 9 THEN '5'
                WHEN grade >= 7 THEN '4'
                WHEN grade >= 5 THEN '3'
                WHEN grade >= 3 THEN '2'
                WHEN grade >= 1 THEN '1'
                ELSE 'Очень плохо'
            END AS grade_group,
            COUNT(*) AS count
        FROM Grades g
        JOIN Students s ON g.student_id = s.student_id
        WHERE s.class_id = %s
        GROUP BY grade_group
        ORDER BY grade_group;
    """
    
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, (class_id,))
                result = cur.fetchall()
                return {row[0]: row[1] for row in result}
    except Exception as e:
        print(f"Ошибка при выполнении запроса: {e}")
        return {}
