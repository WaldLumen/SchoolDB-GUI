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
root.iconbitmap("../school.ico")


with db.data_base_interactions.get_connection() as conn:
    db.data_base_interactions.create_tables(conn)

    # DEBUG THINGS
    gui.utils.print_teachers(conn)
    gui.utils.print_subjects(conn)
    gui.utils.print_classes(conn)


gui.classes_cards.create_class_cards(root)

gui.drop_down_menu.create_menu(root, window_width, window_height)

root.mainloop()
