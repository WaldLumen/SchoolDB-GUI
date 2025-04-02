import tkinter as tk
import tkinter.ttk as ttk
import db
import gui
import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class ClassCard(tk.Canvas):
    def __init__(self, parent, student_id, class_name, first_name, last_name, gender, birth_date, **kwargs):
        super().__init__(parent, width=300, height=150, bg=parent["bg"], highlightthickness=0)

        self.student_id = student_id
        self.first_name = first_name
        self.last_name = last_name

        self.create_rounded_rect(2, 2, 290, 148, 15, outline="black", width=2, fill="white")

        self.create_text(140, 30, text=f"Имя: {first_name}", font=("Arial", 10), fill="black")
        self.create_text(140, 50, text=f"Фамилия: {last_name}", font=("Arial", 10), fill="black")
        self.create_text(140, 70, text=f"Пол: {gender}", font=("Arial", 10), fill="black")
        self.create_text(140, 90, text=f"Дата рождения: {birth_date}", font=("Arial", 10), fill="black")

        # Создаём кнопку и привязываем к ней команду
        self.grades_button = tk.Button(self, text=" ", command=self.open_grades, font=("Arial", 9), bg="black", fg="white")
        
        # Добавляем кнопку в сам Canvas
        self.create_window(140, 120, window=self.grades_button, anchor="center")
        
  
        self.bind("<Button-1>", self.on_click)

    def create_rounded_rect(self, x1, y1, x2, y2, radius, **kwargs):
        points = [
            x1 + radius, y1, x2 - radius, y1, x2, y1, x2, y1 + radius,
            x2, y2 - radius, x2, y2, x2 - radius, y2, x1 + radius, y2,
            x1, y2, x1, y2 - radius, x1, y1 + radius, x1, y1
        ]
        return self.create_polygon(points, smooth=True, **kwargs)

    def on_click(self, event):
        print(f"Вы выбрали ученика: {self.first_name} {self.last_name}")

    def open_grades(self):
        today = datetime.date.today()
        grades_window = tk.Toplevel()
        grades_window.title(f"Журнал оценок - {self.first_name} {self.last_name}")
        grades_window.geometry("700x500")
        grades_window.configure(bg="#f4f4f4")
        
        conn = db.data_base_interactions.get_connection()
        
        # Заголовок "Оценки"
        tk.Label(grades_window, text=(f"Журнал оценок - {self.first_name} {self.last_name}"), font=("Arial", 15, "bold"), bg="#f4f4f4", fg="black").pack(side=tk.TOP, pady=15)
        
        # Фрейм для выбора дат
        date_frame = tk.Frame(grades_window, bg="#f4f4f4")
        date_frame.pack(pady=15)
        
        start_date_var = today - datetime.timedelta(days=30)
        end_date_var = today

        # Метка для среднего балла
        avg_label = tk.Label(grades_window, text="Средний балл: -", font=("Arial", 12, "bold"), bg="#f4f4f4", fg="black")
        avg_label.pack(pady=15)
        
        # Фрейм для отображения оценок
        grades_frame = tk.Frame(grades_window, bg="#f4f4f4")
        grades_frame.pack(pady=10, fill=tk.BOTH, expand=True)
    
        def load_grades(start_date, end_date):
            print(f"Загрузка оценок с {start_date} по {end_date}")  # Проверка вызова функции
        
            # Очищаем frame перед обновлением
            for widget in grades_frame.winfo_children():
                widget.destroy()
            
            # Получаем оценки из БД
            grades = db.data_base_interactions.get_student_grades_by_period(conn, self.student_id, start_date, end_date)
            print(f"Полученные оценки: {grades}")  # Проверка данных
        
            if not grades:
                tk.Label(grades_frame, text="Нет оценок за этот период", 
                         font=("Arial", 13), bg="#f4f4f4", fg="black").pack(pady=5, anchor="w")
                avg_label.config(text="Средний балл: -")
                return  # Выходим из функции

            total_score = 0
            count = 0
            
            # Выводим оценки
            for subject, grade, date_received in grades:
                print(f"Выводим: {date_received}: {subject} - {grade}")  # Проверка в консоли
                tk.Label(grades_frame, text=f"{date_received}: {subject} - {grade}", 
                         font=("Arial", 13), bg="#f4f4f4", fg="black").pack(anchor="center", pady=2)
                total_score += grade
                count += 1

            # Рассчитываем средний балл
            avg_grade = round(total_score / count, 2) if count > 0 else "-"
            avg_label.config(text=f"Средний балл: {avg_grade}")

        date_entry(grades_window, 20, 70, lambda date: load_grades(date, end_date_var))
        date_entry(grades_window, 400, 70, lambda date: load_grades(start_date_var, date))

        
        # Загрузка начальных оценок
        load_grades(start_date_var, end_date_var)
        
        def add_grade():
            add_window = tk.Toplevel(grades_window)
            add_window.title("Добавить оценку")
            add_window.geometry("700x500")
            add_window.configure(bg="#f4f4f4")
        
            tk.Label(add_window, text="Предмет:", font=("Arial", 13), bg="#f4f4f4", fg="black").pack()
            subject_var = tk.StringVar()
            subjects = db.data_base_interactions.get_subjects(conn)

            subject_menu = tk.OptionMenu(add_window, subject_var, *[sub[1] for sub in subjects])
            subject_menu.config(font=("Arial", 13), width=20, bg="#f4f4f4", fg="black")
            subject_menu.pack()

            menu = subject_menu.nametowidget(subject_menu.menuname)
            menu.config(font=("Arial", 13))
            
            tk.Label(add_window, text="Оценка:", font=("Arial", 13), bg="#f4f4f4", fg="black").pack()
            grade_entry = tk.Entry(add_window)
            grade_entry.config(font=("Arial", 13), width=20, bg="#f4f4f4", fg="black")
            grade_entry.pack()
            
            tk.Label(add_window, text="Дата оценки:", font=("Arial", 13), bg="#f4f4f4", fg="black").pack()
            date_frame = tk.Frame(add_window)
            date_frame.configure(bg="#f4f4f4")
            date_frame.pack()

            day_var = tk.StringVar(value=str(today.day))
            month_var = tk.StringVar(value=str(today.month))
            year_var = tk.StringVar(value=str(today.year))
            
            # Увеличенный шрифт
            big_font = ("Arial", 14)
            
            # Spinbox для дня
            day_spinbox = tk.Spinbox(date_frame, from_=1, to=31, textvariable=day_var, width=5, font=big_font, bg="#f4f4f4", fg="black")
            month_spinbox = tk.Spinbox(date_frame, from_=1, to=12, textvariable=month_var, width=5, font=big_font, bg="#f4f4f4", fg="black")
            year_spinbox = tk.Spinbox(date_frame, from_=2000, to=today.year, textvariable=year_var, width=7, font=big_font, bg="#f4f4f4", fg="black")
            
            # Размещение с отступами
            day_spinbox.pack(side=tk.LEFT, padx=5, pady=5, ipady=5)
            tk.Label(date_frame, text="/", font=big_font, bg="#f4f4f4", fg="black").pack(side=tk.LEFT)
            month_spinbox.pack(side=tk.LEFT, padx=5, pady=5, ipady=5)
            tk.Label(date_frame, text="/", font=big_font, bg="#f4f4f4", fg="black").pack(side=tk.LEFT)
            year_spinbox.pack(side=tk.LEFT, padx=5, pady=5, ipady=5)


            
            def save_grade():
                subject_name = subject_var.get()
                grade = float(grade_entry.get())
                subject_id = next(sub[0] for sub in subjects if sub[1] == subject_name)
                selected_date = datetime.date(int(year_var.get()), int(month_var.get()), int(day_var.get()))
                db.data_base_interactions.add_grade(conn, self.student_id, subject_id, grade, selected_date)
                add_window.destroy()
                load_grades(today - datetime.timedelta(days=30), today)
            
            tk.Button(add_window, text="Сохранить", command=save_grade, font=("Arial", 13), bg="#f4f4f4", fg="black").pack()
        
        tk.Button(grades_window, text="Добавить оценку", command=add_grade, font=("Arial", 13), bg="#f4f4f4", fg="black").pack(pady=10)
        
def create_student_cards(root, class_id):
    conn = db.data_base_interactions.get_connection()
    students = db.data_base_interactions.get_students_in_definite_class(conn, class_id)

    for widget in root.winfo_children():
        widget.destroy()

    open_button = tk.Button(root, text="back", command=lambda: gui.refresh_classes.refresh_classes(root), font=("Arial", 15), bg="black", fg="white", bd=0, width=2, height=2)
    open_button.place(x=3, y=3)
    gui.add_student_button.create_button(root, 2000, 1200, class_id)
    
    frame = tk.Frame(root, bg="white", padx=10, pady=10)
    frame.place(x=500, y=50)
    
    for i, (student_id, first_name, last_name, birth_date, gender) in enumerate(students):
        card = ClassCard(frame, student_id, class_id, first_name, last_name, gender, birth_date)
        card.grid(row=i // 3, column=i % 3, padx=10, pady=10)
    diagram(root, class_id)


def date_entry(root, x, y, callback):
    today = datetime.date.today()

    frame = tk.Frame(root)
    frame.config(bg="#f4f4f4")
    frame.place(x=x, y=y)
    

    # Используем IntVar вместо StringVar
    day_var = tk.IntVar(value=today.day)
    month_var = tk.IntVar(value=today.month)
    year_var = tk.IntVar(value=today.year)

    big_font = ("Arial", 10)

    debounced_call = None
    
    def on_date_change(*args):
        nonlocal debounced_call
        
        try:
            selected_date = datetime.date(year_var.get(), month_var.get(), day_var.get())
            print(f"Дата изменена: {selected_date}")  # Проверка
            if debounced_call:
                root.after_cancel(debounced_call)

            # Вызываем callback через 500мс после последнего изменения
            debounced_call = root.after(500, lambda: callback(selected_date))

  
        except ValueError:
            print("Некорректная дата!")

    # Привязываем обновление к изменениям переменных
    day_var.trace_add("write", on_date_change)
    month_var.trace_add("write", on_date_change)
    year_var.trace_add("write", on_date_change)

    # Spinbox'ы
    day_spinbox = tk.Spinbox(frame, from_=1, to=31, textvariable=day_var, width=5, font=big_font, bg="#f4f4f4", fg="black")
    month_spinbox = tk.Spinbox(frame, from_=1, to=12, textvariable=month_var, width=5, font=big_font, bg="#f4f4f4", fg="black")
    year_spinbox = tk.Spinbox(frame, from_=2000, to=today.year, textvariable=year_var, width=7, font=big_font, bg="#f4f4f4", fg="black")

    day_spinbox.pack(side=tk.LEFT, padx=5)
    tk.Label(frame, text="/", font=big_font, bg="#f4f4f4", fg="black").pack(side=tk.LEFT)
    month_spinbox.pack(side=tk.LEFT, padx=5)
    tk.Label(frame, text="/", font=big_font, bg="#f4f4f4", fg="black").pack(side=tk.LEFT)
    year_spinbox.pack(side=tk.LEFT, padx=5)

    return frame

def diagram(root, class_id):
    marks = db.data_base_interactions.get_grade_distribution(class_id)


    labels = list(marks.keys())
    sizes = list(marks.values())


    # Создаем новый фрейм
    chart_frame = ttk.Frame(root)
    chart_frame.place(x=10, y=850)

    # Создаем фигуру и оси
    fig, ax = plt.subplots(figsize=(1.8, 1.8))  # Здесь размер 8x6 дюймов
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=['green', 'blue', 'orange', 'red', "yellow"])
    ax.axis('equal')  # Делаем круг правильным
    ax.set_title("Оценки:")

    # Встраиваем график в Tkinter
    canvas = FigureCanvasTkAgg(fig, master=chart_frame)
    canvas.draw()
    canvas.get_tk_widget().pack()

