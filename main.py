import tkinter as tk
import gui
from screeninfo import get_monitors
import info_panel
import data_base_interactions

monitor = get_monitors()[0]  # Используем первый монитор (если несколько, можно изменить индекс)
screen_width = monitor.width
screen_height = monitor.height

# Рассчитываем размеры окна (70% от разрешения экрана)
window_width = int(screen_width * 0.7)
window_height = int(screen_height * 0.7)
font_size = int(window_height * 0.02)

root = tk.Tk()  # Создаём основное окно
root.title("SchoolDB-GUI")  # Заголовок окна
root.option_add(f"*Font", "JetBrainsMonoNerd{font_size}")
root.geometry(f"{window_width}x{window_height}")  # Размер окна
root.configure(bg="#ffffff")


conn = data_base_interactions.get_connection()
data_base_interactions.create_tables(conn)

subject_id = data_base_interactions.add_subject(data_base_interactions.get_connection(), "Математика")
print(f"Добавлен предмет с ID {subject_id}")

# 2. Добавляем учителя
teacher_id = data_base_interactions.add_teacher(data_base_interactions.get_connection(), "Иван", "Петров", subject_id)
print(f"Добавлен учитель с ID {teacher_id}")
class_id = data_base_interactions.add_class(data_base_interactions.get_connection(), "1A", None)
student_id = data_base_interactions.add_student(data_base_interactions.get_connection(), "Alice", "Johnson", "2008-05-14", "Female", 1)


gui.side_menu(root)
info_panel.print_students(root)

root.mainloop()
