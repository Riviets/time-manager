import tkinter as tk
import colors
import lists
import window_methods as wm
import ItemsManager as im
from tkinter import messagebox

csv_path = 'D:\LABY\LABY 3 KURS\CURSACH\\csvFiles\\notifications_items.csv'

class Notification(im.ItemsManager):
    def __init__(self, text):
        self.text = text

    @staticmethod
    def from_row(row):
        text = row[0]
        return Notification(text)

    def to_row(self):
        return [self.text]

    @staticmethod
    def number_of_items():
        return im.ItemsManager.number_of_items(csv_path)

    @staticmethod
    def open_notifications_window(root):
        def remove_notification(idx):
            confirmed = messagebox.askyesno("Підтвердження", "Ви впевнені, що хочете видалити цю справу?",
                                            parent=notifications_window)
            if confirmed:
                lists.notifications_items.pop(idx)
                Notification.refresh_csv_file(csv_path, lists.notifications_items)
                Notification.fill_items(csv_path, lists.notifications_items, Notification)
                notifications_window.destroy()
                Notification.open_notifications_window(root)
                root.update()

        def display_notifications():
            tasks_title = tk.Label(notifications_window, bg=colors.color_aqua, fg=colors.color_white,
                                   font=("Tahoma", 48, 'bold'), text="Ваші нотатки:")
            tasks_title.place(x=400, y=100)
            notifications_frame = tk.Frame(notifications_window, bg=colors.color_aqua)
            notifications_frame.place(x=432, y=200, relwidth=0.6, height=500)

            notifications_canvas = tk.Canvas(notifications_frame, bg=colors.color_aqua, highlightthickness=0)
            notifications_canvas.pack(side="left", fill="both", expand=True)

            notifications_scrollbar = tk.Scrollbar(notifications_frame, orient="vertical",
                                                   command=notifications_canvas.yview)
            notifications_scrollbar.pack(side="right", fill="y")

            notifications_inner_frame = tk.Frame(notifications_canvas, bg=colors.color_aqua)
            notifications_canvas.create_window((0, 0), window=notifications_inner_frame, anchor="nw")
            notifications_inner_frame.bind("<Configure>", lambda event: notifications_canvas.configure(
                scrollregion=notifications_canvas.bbox("all")))

            num_columns = 2
            notification_frames = []

            for index, notification in enumerate(lists.notifications_items):
                column = index % num_columns
                row = index // num_columns

                notification_frame = tk.Frame(notifications_inner_frame, bg=colors.color_white, relief="solid",
                                              borderwidth=1)
                notification_frame.grid(row=row, column=column, padx=10, pady=10, sticky="nsew")
                notification_frames.append(notification_frame)

                notification_frame.grid_columnconfigure(0, minsize=200)
                notification_frame.grid_columnconfigure(1, minsize=50)

                notification_text_label = tk.Label(notification_frame, text=notification.text, font=("Tahoma", 18),
                                                   fg=colors.color_gray, bg=colors.color_white, wraplength=200,
                                                   anchor="w", justify="left")
                notification_text_label.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

                edit_notification_btn = tk.Button(notification_frame, text='🖉', width=3, height=1,
                                                  bg=colors.color_white, bd=0, font=("Tahoma", 18),
                                                  command=lambda idx=index: open_notification_edit_window(idx))
                edit_notification_btn.grid(row=0, column=1, padx=(0, 10), pady=10, sticky="nsew")

                remove_notification_btn = tk.Button(notification_frame, text='🗑', width=3, height=1,
                                                    bg=colors.color_white, bd=0, font=("Tahoma", 18),
                                                    command=lambda idx=index: remove_notification(idx))
                remove_notification_btn.grid(row=0, column=2, padx=(0, 10), pady=10, sticky="nsew")

            for frame in notification_frames:
                frame.grid_rowconfigure(0, weight=1)

            notifications_canvas.configure(yscrollcommand=notifications_scrollbar.set)

        def open_notification_edit_window(idx):
            def on_text_change(event):
                if len(notification_edit_text.get("1.0", "end-1c")) > 60:
                    notification_edit_text.delete("end-2c", "end-1c")

            def save_changes():
                new_text = notification_edit_text.get("1.0", tk.END).strip()
                if not new_text:
                    messagebox.showwarning("Попередження", "Заповніть усі поля!")
                    return
                lists.notifications_items[idx].text = new_text
                Notification.refresh_csv_file(csv_path, lists.notifications_items)
                notification_edit_window.destroy()
                notifications_window.destroy()
                Notification.open_notifications_window(root)

            notification_edit_window = tk.Toplevel(notifications_window)
            notification_edit_window.title("Редагування нотатки")
            notification_edit_window.geometry("750x400")
            notification_edit_window.resizable(False, False)
            notification_edit_window['bg'] = colors.color_aqua

            notification_edit_label = tk.Label(notification_edit_window, text="Текст нотатки:",
                                               font=("tahoma", 28, 'bold'), bg=colors.color_aqua, fg=colors.color_white)
            notification_edit_label.place(x=64, y=100)

            notification_edit_text = tk.Text(notification_edit_window, width=45, height=2, pady=5, padx=10,
                                             font=("Tahoma", 18))
            notification_edit_text.insert(tk.END, lists.notifications_items[idx].text)
            notification_edit_text.place(x=64, y=162)
            notification_edit_text.bind("<KeyRelease>", on_text_change)

            save_changes_btn = tk.Button(notification_edit_window, text="Зберегти Зміни", font=("Tahoma", 14, 'bold'),
                                         bg=colors.color_white, padx=10, pady=5, command=save_changes)
            save_changes_btn.place(x=455, y=270)

        notifications_window = tk.Toplevel(root)
        notifications_window.state('zoomed')
        wm.set_default(notifications_window, "Нотатки", root)
        Notification.fill_items(csv_path, lists.notifications_items, Notification)

        create_notification_btn = tk.Button(notifications_window, text="Створити Нотатку", font=("Tahoma", 16, 'bold'),
                                            bg=colors.color_white, padx=10, pady=5,
                                            command=lambda: open_notification_creation_window())
        create_notification_btn.place(x=1086, y=44)

        if not lists.notifications_items:
            no_notifications_label = tk.Label(notifications_window, text="Нотаток Немає",
                                              font=("Tahoma", 48, 'bold'),
                                              bg=colors.color_aqua, fg=colors.color_white)
            no_notifications_label.place(x=550, y=176)
        else:
            display_notifications()

        def open_notification_creation_window():
            def on_text_change(event):
                if len(notification_creation_text.get("1.0", "end-1c")) > 60:
                    notification_creation_text.delete("end-2c", "end-1c")

            def create_notification():
                notification_text = notification_creation_text.get("1.0", "end-1c")
                if not notification_text:
                    messagebox.showwarning("Попередження", "Введіть текст нотатки.")
                    return
                notification = Notification(notification_text)
                lists.notifications_items.append(notification)
                Notification.refresh_csv_file(csv_path, lists.notifications_items)
                notifications_window.destroy()
                Notification.open_notifications_window(root)

            notification_creation_window = tk.Toplevel(notifications_window)
            notification_creation_window.title("Створення Нотатки")
            notification_creation_window.geometry("750x400")
            notification_creation_window.resizable(False, False)
            notification_creation_window['bg'] = colors.color_aqua

            notification_creation_label = tk.Label(notification_creation_window, text="Текст Нотатки:",
                                                   font=("tahoma", 28, 'bold'), bg=colors.color_aqua, fg=colors.color_white)
            notification_creation_label.place(x=64, y=100)

            notification_creation_text = tk.Text(notification_creation_window, width=45, height=2, pady=5, padx=10,
                                                 font=("Tahoma", 18))
            notification_creation_text.place(x=64, y=162)
            notification_creation_text.bind("<Return>", lambda event: "break")
            notification_creation_text.bind("<BackSpace>", on_text_change)
            notification_creation_text.bind("<Delete>", on_text_change)

            notification_creation_text.bind("<Key>", on_text_change)

            create_notification_btn = tk.Button(notification_creation_window, text="Створити Нотатку",
                                                font=("Tahoma", 14, 'bold'),
                                                bg=colors.color_white, padx=10, pady=5,
                                                command=create_notification)
            create_notification_btn.place(x=455, y=270)
