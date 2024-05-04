import tkinter as tk
from PIL import Image, ImageTk
import colors
import lists
import notification as nt
import reminders as rm
import todolist as td
import tasks as t
import window_methods as wm
import schedule

def update_root(root, canvas):
    tasks_present = t.Main_task.number_of_items() > 0
    todolist_present = td.Todolist.number_of_items() > 0
    reminders_present = rm.Reminder.number_of_items() > 0
    notification_present = nt.Notification.number_of_items() > 0

    items_present = tasks_present or todolist_present or notification_present or reminders_present

    if not items_present:
        items_present_title.place_forget()
        items_present_text.place_forget()
        no_data_text.place(x=550, y=150)
        canvas.itemconfig(img_id, state="normal")
    else:
        no_data_text.place_forget()
        canvas.itemconfig(img_id, state="hidden")
        items_present_title.place(x=400, y=100)
        items_present_text.config(text="Завдання:\t\t" + str(t.Main_task.number_of_items()) +
                                     "\n\nНотатки:\t\t\t" + str(nt.Notification.number_of_items()) +
                                     "\n\nНагадування:\t\t" + str(rm.Reminder.number_of_items()) +
                                     "\n\nСписок Справ:\t\t" + str(td.Todolist.number_of_items()))
        items_present_text.place(x=400, y=200)
        for reminder in lists.reminders_items:
            rm.show_reminder_notification(reminder)
    root.after(2000, update_root, root, canvas)
    schedule.run_pending()

def main():
    global img_id
    root = tk.Tk()
    root.state('zoomed')
    wm.set_default(root, "Організація часу та завдань", root)
    root.resizable(False, False)
    canvas = tk.Canvas(root, bg=colors.color_aqua, highlightbackground=colors.color_aqua)
    canvas.place(x=402, y=67, width=1338 - 402, height=682 - 67)

    global no_data_text
    no_data_text = tk.Label(root, anchor="nw", text="Елементів Немає", font=("Tahoma", 48, 'bold'))
    no_data_text.config(bg=colors.color_aqua, fg=colors.color_white)

    sad_robot_img_url = "images/sad_robot.png"
    img = Image.open(sad_robot_img_url)
    img = ImageTk.PhotoImage(img)
    img_id = canvas.create_image(286, 206, anchor="nw", image=img)

    global items_present_title, items_present_text
    items_present_title = tk.Label(root, text="Ваші Елементи:", font=("Tahoma", 48, 'bold'), fg=colors.color_white,
                                   bg=colors.color_aqua)
    items_present_text = tk.Label(root, text="", justify=tk.LEFT, font=("Tahoma", 18),
                                  pady=20, padx=40)

    update_root(root, canvas)

    root.mainloop()

main()