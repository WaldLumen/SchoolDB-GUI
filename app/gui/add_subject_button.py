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
    button_style = {"bg": "black", "fg": "white", "font": font_main, "bd": 0, "width": 12, "height": 2}

    # === Поля ввода с placeholder ===
    subject_name_entry = tk.Entry(new_window, width=20, font=font_main, bd=2, relief="solid", bg="white")
    subject_name_entry.place(x=10, y=10)
    add_placeholder(subject_name_entry, "Введите название предмета")

    def add_class_s(conn):
        db.data_base_interactions.add_subject(conn, subject_name_entry.get())
        gui.refresh_classes.refresh_classes(root)

        
    # === Кнопка "Сохранить" ===
    save_button = tk.Button(new_window, text="💾 Сохранить", **button_style, command=lambda: add_class_s(conn))
    save_button.place(x=40, y=150)

def create_button(root, window_width, window_height):
    open_button = tk.Button(root, text="Добавить предмет", command=lambda: gui.add_subject_button.open_new_window(root, db.data_base_interactions.get_connection()), font=("Arial", 15),  bg="black", fg="white", bd=0, width=int(window_width * 0.006), height=int(window_height * 0.002))

    open_button.place(x=window_width / 2 - 500, y= window_height - 100)

