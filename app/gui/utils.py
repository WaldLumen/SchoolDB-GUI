import db

def print_teachers(conn):
    """Выводит всех учителей в консоль вместе с ID учителя и ID предмета"""
    teachers =db.data_base_interactions.get_teachers(conn)

    if not teachers:
        print("Учителей в базе нет или произошла ошибка.")
        return

    print("Список учителей:")
    for teacher_id, full_name, subject_id, subject_name in teachers:
        print(f"- ID: {teacher_id}, {full_name} (Предмет ID: {subject_id}, {subject_name})")


def print_subjects(conn):
    """Выводит все предметы в консоль"""
    subjects = db.data_base_interactions.get_subjects(conn)

    if not subjects:
        print("Предметов в базе нет.")
        return

    print("Список предметов:")
    for subject_id, subject_name in subjects:
        print(f"- ID: {subject_id}, Название: {subject_name}")
        

def print_classes(conn):
    classes = db.data_base_interactions.get_classes(conn)
    if not classes:
        print("Предметов в базе нет.")
        return

    print("Класы")

    for class_id, class_name, teacher_id in classes:
        print(f"- ID: {class_id}, Название: {class_name}")
        
def hide_all_widgets(root):
    global hidden_widgets
    hidden_widgets = root.winfo_children()  # Сохраняем виджеты
    for widget in hidden_widgets:
        widget.pack_forget()
        widget.grid_forget()
        widget.place_forget()
