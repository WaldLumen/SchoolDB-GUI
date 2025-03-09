import tkinter as tk

def side_menu(root):
    """Создаёт боковое меню с тремя кнопками"""
    frame = tk.Frame(root, borderwidth=2, relief="ridge")
    frame.place(x=100, y=150)

    button_t = tk.Button(frame, text="Верх кнопка")
    button_t.pack(pady=20, padx=20)

    button_c = tk.Button(frame, text="Центр кнопка")
    button_c.pack(pady=20, padx=20)  

    button_b = tk.Button(frame, text="Нижняя кнопка")  # Исправлено
    button_b.pack(pady=20, padx=20)
