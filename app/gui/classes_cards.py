import tkinter as tk
import db
import gui

class ClassCard(tk.Canvas):
    def __init__(self, parent, class_name, students_count, teacher_name, **kwargs):
        super().__init__(parent, width=250, height=100, bg=parent["bg"], highlightthickness=0)

        self.radius = 20  # Радиус закруглений
        self.badge_radius = 20  # Радиус закругления бейджа

        # Рисуем карточку
        self.create_rounded_rect(3, 3, 247, 97, self.radius, outline="black", width=3, fill="")

        # Рисуем бейдж для имени класса (в верхнем левом углу)
        self.create_rounded_rect(10, 10, 60, 55, self.badge_radius, outline="black", width=2, fill="white")

        # Текст внутри бейджа (Название класса)
        self.class_name = class_name  # Сохраняем название класса
        self.class_label = self.create_text(33, 30, 
                                            text=class_name, font=("Arial", 10, "bold"), fill="black")

        # Основные надписи на карточке
        self.students_label = self.create_text(125, 33, text=f"Ученики: {students_count}", font=("Arial", 10), fill="black")
        self.teacher_label = self.create_text(125, 75, text=f"Классрук: {teacher_name}", font=("Arial", 10), fill="black")

        # Привязка события клика
        self.tag_bind(self.students_label, "<Button-1>", self.on_click)
        self.tag_bind(self.teacher_label, "<Button-1>", self.on_click)
        self.bind("<Button-1>", self.on_click)

    def create_rounded_rect(self, x1, y1, x2, y2, radius, **kwargs):
        """Рисует только контур скруглённого прямоугольника"""
        points = [
            x1 + radius, y1,
            x2 - radius, y1,
            x2, y1,
            x2, y1 + radius,
            x2, y2 - radius,
            x2, y2,
            x2 - radius, y2,
            x1 + radius, y2,
            x1, y2,
            x1, y2 - radius,
            x1, y1 + radius,
            x1, y1
        ]
        return self.create_polygon(points, smooth=True, **kwargs)

    def on_click(self, event):
        print(f"Вы выбрали класс: {self.class_name}")

        conn = db.data_base_interactions.get_connection()
        
        with conn.cursor() as cur:
            # Используем self.class_name, а не self.class_label
            cur.execute("SELECT class_id FROM Classes WHERE class_name = %s;", (self.class_name,))

            class_id = cur.fetchone()  # Получаем только одну строку
            
            if class_id:
                # Извлекаем сам class_id из результата
                class_id = class_id[0]
                
                # Передаем в функцию для создания карточек учеников
                gui.students_cards.create_student_cards(self.master.master, class_id)
            else:
                print("Класс не найден.")

           
def create_class_cards(root):
    conn = db.data_base_interactions.get_connection()
    classes = db.data_base_interactions.get_classes(conn)
    frame = tk.Frame(root, bg="white", padx=10, pady=10)
    frame.place(x=500, y=50)

    for i, (class_id, class_name, teacher_id) in enumerate(classes):
        card = ClassCard(frame, class_name, "12",  teacher_id)
        card.grid(row=i // 3, column=i % 3, padx=10, pady=10)
