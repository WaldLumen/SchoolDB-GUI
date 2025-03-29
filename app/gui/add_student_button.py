import tkinter as tk
from tkinter import filedialog
import gui
import db

def open_new_window(root, conn):
    """Создаёт новое окно с placeholder в полях ввода"""
    new_window = tk.Toplevel(root)
    new_window.title("Добавление пользователя")
    new_window.geometry("520x410")
    new_window.configure(bg="#f4f4f4")

    def add_placeholder(entry, text):
        """Добавляет placeholder в поле ввода"""
        entry.insert(0, text)
        entry.config(fg="gray")

        def on_focus_in(event):
            if entry.get() == text:
                entry.delete(0, "end")
                entry.config(fg="black")

        def on_focus_out(event):
            if entry.get() == "":
                entry.insert(0, text)
                entry.config(fg="gray")

        entry.bind("<FocusIn>", on_focus_in)
        entry.bind("<FocusOut>", on_focus_out)

    # === Стили ===
    font_main = ("Arial", 12)
    button_style = {"bg": "#4CAF50", "fg": "white", "font": font_main, "bd": 0, "width": 18, "height": 2}

    # === Поля ввода с placeholder ===
    name_entry = tk.Entry(new_window, width=30, font=font_main, bd=2, relief="solid", background="white", foreground="black")
    name_entry.place(x=20, y=80)
    add_placeholder(name_entry, "Введите имя:")

    last_name_entry = tk.Entry(new_window, width=30, font=font_main, bd=2, relief="solid", background="white", foreground="black")
    last_name_entry.place(x=20, y=160)
    add_placeholder(last_name_entry, "Введите фамилию:")

    class_entry = tk.Entry(new_window, width=10, font=font_main, bd=2, relief="solid", background="white", foreground="black")
    class_entry.place(x=300, y=80)
    add_placeholder(class_entry, "Класс")

    gender_entry = tk.Entry(new_window, width=10, font=font_main, bd=2, relief="solid", background="white", foreground="black")
    gender_entry.place(x=300, y=120)
    add_placeholder(gender_entry, "Гендер: ")

    birth_entry = tk.Entry(new_window, width=15, font=font_main, bd=2, relief="solid", background="white", fg="red")
    birth_entry.place(x=300, y=150)
    add_placeholder(birth_entry, "ДД.ММ.ГГГГ")

    def add_student():
        db.data_base_interactions.add_student(conn, name_entry.get(), last_name_entry.get(), birth_entry.get(), gender_entry.get(), class_entry.get())
        gui.students_cards.create_student_cards(root, "7")
    
    # === Кнопка "Сохранить" ===
    save_button = tk.Button(new_window, text="💾 Сохранить", **button_style, command=add_student)
    save_button.place(x=20, y=315)

    
def create_button(root, window_width, window_height):
    open_button = tk.Button(root, text="Добавить ученика", command=lambda: open_new_window(root, db.data_base_interactions.get_connection()), font=("Arial", 15),  bg="black", fg="white", bd=0, width=int(window_width * 0.006), height=int(window_height * 0.002))
    open_button.place(x=window_width / 1.6, y=window_height - 100)
