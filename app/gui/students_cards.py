import tkinter as tk

import db
import gui

from PIL import Image, ImageTk

class ClassCard(tk.Canvas):
    def __init__(self, parent, class_name, first_name, last_name, gender, birth_date, **kwargs):
        super().__init__(parent, width=250, height=120, bg=parent["bg"], highlightthickness=0)

        self.radius = 15  # Радиус закруглений
        self.badge_radius = 10  # Радиус бейджа

        # Рисуем карточку
        self.create_rounded_rect(2, 2, 248, 118, self.radius, outline="black", width=2, fill="white")

        # Бейдж с классом
        self.create_rounded_rect(10, 10, 60, 40, self.badge_radius, outline="black", width=2, fill="lightgray")
        self.class_label = self.create_text(35, 25, text=class_name, font=("Arial", 10, "bold"), fill="black")

        self.first_name = first_name  # Сохраняем имя ученика
        self.last_name = last_name  # Сохраняем фамилию

        
        # Основные надписи
        self.create_text(125, 35, text=f"Имя: {first_name}", font=("Arial", 10), fill="black")
        self.create_text(125, 55, text=f"Фамилия: {last_name}", font=("Arial", 10), fill="black")
        self.create_text(125, 75, text=f"Пол: {gender}", font=("Arial", 10), fill="black")
        self.create_text(125, 95, text=f"Дата рождения: {birth_date}", font=("Arial", 10), fill="black")
        
        # Привязка клика к всей карточке
        self.bind("<Button-1>", self.on_click)

    def create_rounded_rect(self, x1, y1, x2, y2, radius, **kwargs):
        """Рисует скругленный прямоугольник"""
        points = [
            x1 + radius, y1,  x2 - radius, y1,  x2, y1,  x2, y1 + radius,
            x2, y2 - radius,  x2, y2,  x2 - radius, y2,  x1 + radius, y2,
            x1, y2,  x1, y2 - radius,  x1, y1 + radius,  x1, y1
        ]
        return self.create_polygon(points, smooth=True, **kwargs)

    def on_click(self, event):
        print(f"Вы выбрали ученика: {self.first_name} {self.last_name}")


def create_student_cards(root, class_id):
    conn = db.data_base_interactions.get_connection()
    students = db.data_base_interactions.get_students_in_definite_class(conn, class_id)

    for widget in root.winfo_children():  # Очистка старых карточек
        widget.destroy()

    open_button = tk.Button(root, text="back", command=lambda: gui.refresh_classes.refresh_classes(root), font=("Arial", 15),  bg="black", fg="white", bd=0, width=20, height=20)
     
    open_button.place(x=3, y=3)

    gui.add_student_button.create_button(root, 1800, 1200)
    
    frame = tk.Frame(root, bg="white", padx=10, pady=10)
    frame.place(x=500, y=50)  # Смещаем влево для лучшего расположения

    for i, (class_name, first_name, last_name, gender, birth_date) in enumerate(students):
        card = ClassCard(frame, class_name, first_name, last_name, gender, birth_date)
        card.pack(pady=5, padx=5)
