import tkinter as tk
import gui
import db


class DropDownMenu(tk.Frame):
    def __init__(self, parent, root, window_width, window_height, **kwargs):
        super().__init__(parent, bg="white", bd=1, relief="solid", **kwargs)

        self.root = root
        self.window_width = window_width
        self.window_height = window_height
        self.visible = False

        for text, cmd in [
            ("Добавить Клас", self.open_classes),
            ("Добавить Учителя", self.open_students),
            ("Добавить Предмет", self.open_subject),
        ]:
            btn = tk.Label(
                self,
                text=text,
                bg="white",
                fg="black",
                anchor="w",
                padx=12,
                pady=6,
                cursor="hand2"
            )
            btn.pack(fill="x")
            btn.bind("<Button-1>", lambda e, c=cmd: c())
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg="#f0f0f0"))
            btn.bind("<Leave>", lambda e, b=btn: b.config(bg="white"))

    def toggle(self, x, y):
        if self.visible:
            self.place_forget()
        else:
            self.place(x=x, y=y)
        self.visible = not self.visible

    def hide(self):
        if self.visible:
            self.place_forget()
            self.visible = False

    def open_classes(self):
        gui.add_class_button.open_new_window(self.root, db.data_base_interactions.get_connection())
        self.hide()

    def open_students(self):
        gui.add_subject_button.open_new_window(
            self.root,
            db.data_base_interactions.get_connection()
        )
        self.hide()

    def open_subject(self):
        gui.add_teacher_button.open_new_window(self.root, db.data_base_interactions.get_connection())
        self.hide()


def create_menu(root, window_width, window_height):
    menu = DropDownMenu(root, root, window_width, window_height)

    menu_button = tk.Label(
        root,
        text="☰ Меню",
        bg="white",
        fg="black",
        padx=10,
        pady=5,
        cursor="hand2",
        relief="solid",
        bd=1
    )
    menu_button.place(x=20, y=0)

    def toggle_menu(event):
        x = menu_button.winfo_x()
        y = menu_button.winfo_y() + menu_button.winfo_height()
        menu.toggle(x, y)

    menu_button.bind("<Button-1>", toggle_menu)

    def click_outside(event):
        if menu.visible and not menu.winfo_containing(event.x_root, event.y_root):
            menu.hide()

    root.bind("<Button-1>", click_outside, add="+")

    return menu
