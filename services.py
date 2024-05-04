import colors
import tkinter as tk
from PIL import Image, ImageTk
import todolist as td
import window_methods as wm
import lists


def create_button(text, image_path, click_handler, window, *args):
    button_frame = tk.Frame(window, bg=colors.color_aqua)
    button_frame.pack(pady=10)

    img = Image.open(image_path)
    img = img.resize((40, 40))
    tk_img = ImageTk.PhotoImage(img)

    button = tk.Button(button_frame, text=text, bg=colors.color_white, fg=colors.color_gray, image=tk_img, compound="right",
                       command=lambda: click_handler(*args), font=("Tahoma", 16, "bold"), width=220, height=69, anchor="center")
    button.image = tk_img
    button.pack(side=tk.LEFT, padx=10, fill=tk.BOTH, expand=True)

    return button_frame


def close_all_windows(root):
    for window in root.winfo_children():
        if isinstance(window, tk.Toplevel):
            window.destroy()

def set_default_method(window, title, tasks_handler, notes_handler, pomodoro_handler, reminders_handler, todolist_handler, root):
    window.title(title)
    window.geometry("1540x850")
    window['bg'] = colors.color_aqua
    vertical_line = tk.Frame(window, bg=colors.color_gray, width=2, height=850)
    vertical_line.place(x=297)
    tasks_btn_frame = create_button("Організатор\nЗавдань", "D:/LABY/LABY 3 KURS/CURSACH/images/tasks.png",
                                    lambda: tasks_handler(root), window)
    tasks_btn_frame.place(x=39, y=67)
    notes_btn_frame = create_button("Нотатки", "D:/LABY/LABY 3 KURS/CURSACH/images/notes.png", lambda: notes_handler(root),
                                    window)
    notes_btn_frame.place(x=39, y=161)
    pomodoro_btn_frame = create_button("Помодоро", "D:/LABY/LABY 3 KURS/CURSACH/images/pomodoro.png",
                                       lambda: pomodoro_handler(root), window)
    pomodoro_btn_frame.place(x=39, y=255)
    reminders_btn_frame = create_button("Нагадування", "D:/LABY/LABY 3 KURS/CURSACH/images/reminders.png",
                                        lambda: reminders_handler(root), window)
    reminders_btn_frame.place(x=39, y=349)
    todolist_btn_frame = create_button("Список\nСправ", "D:/LABY/LABY 3 KURS/CURSACH/images/todo.png",
                                       lambda: todolist_handler(root), window)

    todolist_btn_frame.place(x=39, y=443)
    robot_img_url = "images/robot.png"
    img = Image.open(robot_img_url)
    img = img.resize((122, 157))
    tk_img_robot = ImageTk.PhotoImage(img)
    robot_label = tk.Label(window, image=tk_img_robot, bg=colors.color_aqua)
    robot_label.image = tk_img_robot
    robot_label.place(x=88, y=542)