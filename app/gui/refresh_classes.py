import tkinter as tk
from screeninfo import get_monitors

import gui


def refresh_classes(root):
    monitor = get_monitors()[0]
    screen_width = monitor.width
    screen_height = monitor.height
    window_width = int(screen_width * 0.7)
    window_height = int(screen_height * 0.7)

    for widget in root.winfo_children():
        widget.destroy()
    gui.classes_cards.create_class_cards(root)

    gui.add_class_button.create_button(root, window_width, window_height)
    gui.add_teacher_button.create_button(root, window_width, window_height)
    gui.add_subject_button.create_button(root, window_width, window_height)

