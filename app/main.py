import tkinter as tk
from screeninfo import get_monitors

import db
import gui

monitor = get_monitors()[0]
screen_width = monitor.width
screen_height = monitor.height
window_width = int(screen_width * 0.7)
window_height = int(screen_height * 0.7)

root = tk.Tk()
root.title("SchoolDB-GUI")
root.geometry(f"{window_width}x{window_height}")
root.configure(bg="#ffffff")


db.data_base_interactions.create_tables(db.data_base_interactions.get_connection())
#db.data_base_interactions.clear_database(db.data_base_interactions.get_connection())



gui.utils.print_teachers(db.data_base_interactions.get_connection())
gui.utils.print_subjects(db.data_base_interactions.get_connection())
gui.utils.print_classes(db.data_base_interactions.get_connection())


gui.classes_cards.create_class_cards(root)

gui.add_class_button.create_button(root, window_width, window_height)
gui.add_teacher_button.create_button(root, window_width, window_height)
gui.add_subject_button.create_button(root, window_width, window_height)
root.mainloop()
