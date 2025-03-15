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

    print("База данных успешно создана!")

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
        cur.execute("SELECT student_id, first_name, last_name FROM Students")
        return cur.fetchall()

def add_class(conn, class_name, teacher_id):
    """Добавляет класс в базу данных"""
    with conn.cursor() as cur:
        cur.execute("INSERT INTO Classes (class_name, teacher_id) VALUES (%s, %s) RETURNING class_id;", (class_name, teacher_id))
        class_id = cur.fetchone()[0]
        conn.commit()
    return class_id
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
