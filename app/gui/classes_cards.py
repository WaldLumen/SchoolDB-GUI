import tkinter as tk
import db
import gui


class ClassCard(tk.Canvas):
    WIDTH = 520
    HEIGHT = 130
    RADIUS = 20
    BADGE_RADIUS = 20

    def __init__(self, parent, class_name, students_count, teacher_name):
        super().__init__(
            parent,
            width=self.WIDTH,
            height=self.HEIGHT,
            bg="white",
            highlightthickness=0
        )

        self.class_name = class_name

        self.create_rounded_rect(5, 5, self.WIDTH - 5, self.HEIGHT - 5, self.RADIUS, outline="black", fill="white")
        self.create_rounded_rect(15, 15, 85, 70, self.BADGE_RADIUS, outline="black", fill="white")

        self.create_text(50, 42, text=class_name, font=("Arial", 10, "bold"))
        self.create_text(180, 45, text=f"Ученики: {students_count}", font=("Arial", 12))
        self.create_text(240, 90, text=f"Классрук: {teacher_name}", font=("Arial", 12))

        self.bind("<Button-1>", self.on_click)

    def create_rounded_rect(self, x1, y1, x2, y2, r, **kwargs):
        points = [
            x1 + r, y1,
            x2 - r, y1,
            x2, y1,
            x2, y1 + r,
            x2, y2 - r,
            x2, y2,
            x2 - r, y2,
            x1 + r, y2,
            x1, y2,
            x1, y2 - r,
            x1, y1 + r,
            x1, y1
        ]
        return self.create_polygon(points, smooth=True, **kwargs)

    def on_click(self, event):
        print(f"Вы выбрали класс: {self.class_name}")

        conn = db.data_base_interactions.get_connection()
        with conn.cursor() as cur:
            cur.execute(
                "SELECT class_id FROM Classes WHERE class_name = %s",
                (self.class_name,)
            )
            res = cur.fetchone()
            if res:
                gui.students_cards.create_student_cards(self.master.master, res[0])





def create_class_cards(root):
    conn = db.data_base_interactions.get_connection()
    classes = db.data_base_interactions.get_classes(conn)

    frame = tk.Frame(root, bg="white", padx=10, pady=10)
    frame.place(x=200, y=50)




    for i, (class_id, class_name, teacher_name) in enumerate(classes):
        card = ClassCard(
            frame,
            class_name,
            students_count=len(db.data_base_interactions.get_students_in_definite_class(conn, class_id)),
            teacher_name=teacher_name
        )
        card.grid(row=i // 3, column=i % 3, padx=10, pady=10)

