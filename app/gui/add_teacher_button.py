import tkinter as tk

import db
import gui

def open_new_window(root, conn):
    """Создаёт новое окно с placeholder в полях ввода"""
    new_window = tk.Toplevel(root)
    new_window.title("add_class")
    new_window.geometry("300x280")
    new_window.configure(bg="#f4f4f4")
    new_window.img = None  

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
    button_style = {"bg": "black", "fg": "white", "font": font_main, "bd": 0, "width": 20, "height": 2}

    # === Поля ввода с placeholder ===
    name_entry = tk.Entry(new_window, width=20, font=font_main, bd=2, relief="solid", bg="white")
    name_entry.place(x=10, y=10)
    add_placeholder(name_entry, "Введите имя преподователя")

    last_name_entry = tk.Entry(new_window, width=20, font=font_main, bd=2, relief="solid", bg="white")
    last_name_entry.place(x=10, y=50)
    add_placeholder(last_name_entry, "Введите фамилию преподователя")

    subject_id_entry = tk.Entry(new_window, width=20, font=font_main, bd=2, relief="solid", bg="white")
    subject_id_entry.place(x=10, y=100)
    add_placeholder(subject_id_entry, "Предмет(id)")

    def add_class_s(conn):
        db.data_base_interactions.add_teacher(conn, name_entry.get(), last_name_entry.get(), subject_id_entry.get())
        gui.refresh_classes.refresh_classes(root)

        
    # === Кнопка "Сохранить" ===
    save_button = tk.Button(new_window, text="💾 Сохранить", **button_style, command=lambda: add_class_s(conn))
    save_button.place(x=40, y=150)

