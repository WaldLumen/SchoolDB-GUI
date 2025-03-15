import data_base_interactions
import tkinter as tk

def print_students(root):
    """Создаёт фрейм справа и выводит студентов"""
    
    # Фрейм справа с отступами
    right_frame = tk.Frame(root, bg="blue", width=200, height=400)
    right_frame.pack(side="right", fill="y", padx=10, pady=10)

    # Получаем список студентов
    conn = data_base_interactions.get_connection()
    students = data_base_interactions.get_students(conn)
    conn.close()  # Закрываем соединение после запроса

    # Добавляем студентов в правый фрейм
    for student in students:
        label = tk.Label(right_frame, text=f"{student[1]} {student[2]}")
        label.pack(anchor="w", padx=5, pady=2)

