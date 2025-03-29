import tkinter as tk
from screeninfo import get_monitors

def create_rounded_rectangle(canvas, x1, y1, x2, y2, radius, fill, outline, width, tags):
    """Рисует прямоугольник с округлыми углами на Canvas"""
    elements = []  # Список ID элементов кнопки

    # Углы (округлённые)
    elements.append(canvas.create_oval(x1, y1, x1 + 2*radius, y1 + 2*radius, 
                                       fill=fill, outline=outline, width=width, tags=tags))
    elements.append(canvas.create_oval(x2 - 2*radius, y1, x2, y1 + 2*radius, 
                                       fill=fill, outline=outline, width=width, tags=tags))
    elements.append(canvas.create_oval(x1, y2 - 2*radius, x1 + 2*radius, y2, 
                                       fill=fill, outline=outline, width=width, tags=tags))
    elements.append(canvas.create_oval(x2 - 2*radius, y2 - 2*radius, x2, y2, 
                                       fill=fill, outline=outline, width=width, tags=tags))

    # Центральные части кнопки
    elements.append(canvas.create_rectangle(x1 + radius, y1, x2 - radius, y2, 
                                            fill=fill, outline=outline, width=width, tags=tags))
    elements.append(canvas.create_rectangle(x1, y1 + radius, x2, y2 - radius, 
                                            fill=fill, outline=outline, width=width, tags=tags))

    return elements  # Возвращаем ID элементов кнопки

def rounded_button(canvas, text, x, y, width, height, radius, command, button_tag):
    monitor = get_monitors()[0]
    screen_height = monitor.height
    window_height = int(screen_height * 0.7)
    font_size = int(window_height * 0.008)

    """Создаёт кнопку с округлыми углами на Canvas"""
    button_elements = create_rounded_rectangle(
        canvas, x, y, x + width, y + height, radius, 
        fill="#ebe939", outline="#ebe939", width=1, tags=button_tag
    )

    # Текст кнопки (отдельно, чтобы цвет не менялся)
    text_id = canvas.create_text(x + width / 2, y + height / 2, text=text, 
                                 fill="black", font=("JetBrainsMonoNerd", font_size), tags=button_tag)

    # Привязываем события
    canvas.tag_bind(button_tag, "<Button-1>", command)
    canvas.tag_bind(button_tag, "<Enter>", lambda event: on_hover(canvas, button_elements, "#ffff00"))
    canvas.tag_bind(button_tag, "<Leave>", lambda event: on_leave(canvas, button_elements, "#ebe939"))

def on_hover(canvas, elements, hover_color):
    """Меняет цвет кнопки (и её границы) при наведении"""
    for element in elements:
        canvas.itemconfig(element, fill=hover_color, outline=hover_color)  # Обновляем и фон, и границы

def on_leave(canvas, elements, original_color):
    """Возвращает оригинальный цвет кнопки (и её границы)"""
    for element in elements:
        canvas.itemconfig(element, fill=original_color, outline=original_color)  # Восстанавливаем цвета


