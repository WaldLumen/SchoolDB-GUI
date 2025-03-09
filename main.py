import tkinter as tk
import gui
from screeninfo import get_monitors

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

gui.side_menu(root)

root.mainloop()
