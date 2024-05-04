import tkinter as tk
import colors
import window_methods as wm
import ItemsManager as im
import threading
import calendar
import datetime
import json
from plyer import notification
import lists
from tkinter import ttk
from tkinter import messagebox

csv_path = 'D:\LABY\LABY 3 KURS\CURSACH\\csvFiles\\reminders_items.csv'

class Date:
    def __init__(self, month, day, hour, minute):
        self.month = month
        self.day = day
        self.hour = hour
        self.minute = minute

class Reminder(im.ItemsManager):
    def __init__(self, text, date):
        self.text = text
        self.date = date
        self.displayed = False

    @staticmethod
    def from_row(row):
        text = row[0]
        date_data = json.loads(row[1])
        date = Date(**date_data)
        return Reminder(text, date)

    def to_row(self):
        date_data = {'month': self.date.month, 'day': self.date.day, 'hour': self.date.hour, 'minute': self.date.minute}
        return [self.text, json.dumps(date_data)]

    @staticmethod
    def number_of_items():
        return im.ItemsManager.number_of_items(csv_path)

    @staticmethod
    def open_reminders_window(root):
        def remove_reminder(idx):
            confirmed = messagebox.askyesno("Підтвердження", "Ви впевнені, що хочете видалити це нагадування?",
                                            parent=reminders_window)
            if confirmed:
                lists.reminders_items.pop(idx)
                Reminder.refresh_csv_file(csv_path, lists.reminders_items)
                reminders_window.destroy()
                Reminder.open_reminders_window(root)

        def display_reminders():
            reminders_title = tk.Label(reminders_window, bg=colors.color_aqua, fg=colors.color_white,
                                       font=("Tahoma", 48, 'bold'), text="Ваші нагадування:")
            reminders_title.place(x=400, y=100)
            reminders_frame = tk.Frame(reminders_window, bg=colors.color_aqua)
            reminders_frame.place(x=432, y=200, relwidth=0.6, height=500)

            reminders_canvas = tk.Canvas(reminders_frame, bg=colors.color_aqua, highlightthickness=0)
            reminders_canvas.pack(side="left", fill="both", expand=True)

            reminders_scrollbar = tk.Scrollbar(reminders_frame, orient="vertical",
                                               command=reminders_canvas.yview)
            reminders_scrollbar.pack(side="right", fill="y")

            reminders_inner_frame = tk.Frame(reminders_canvas, bg=colors.color_aqua)
            reminders_canvas.create_window((0, 0), window=reminders_inner_frame, anchor="nw")
            reminders_inner_frame.bind("<Configure>", lambda event: reminders_canvas.configure(
                scrollregion=reminders_canvas.bbox("all")))

            num_columns = 2
            reminder_frames = []

            for index, reminder in enumerate(lists.reminders_items):
                column = index % num_columns
                row = index // num_columns

                reminder_frame = tk.Frame(reminders_inner_frame, bg=colors.color_white, relief="solid",
                                          borderwidth=1)
                reminder_frame.grid(row=row, column=column, padx=10, pady=10, sticky="nsew")
                reminder_frames.append(reminder_frame)

                reminder_frame.grid_columnconfigure(0, minsize=200)
                reminder_frame.grid_columnconfigure(1, minsize=50)

                reminder_text_label = tk.Label(reminder_frame, text=reminder.text, font=("Tahoma", 18),
                                               fg=colors.color_gray, bg=colors.color_white, wraplength=200,
                                               anchor="w", justify="left")
                reminder_text_label.grid(row=0, column=0, padx=10, pady=5, sticky="nsew")

                reminder_date_label = tk.Label(reminder_frame,
                                               text=f"{reminder.date.day:02}-{reminder.date.month:02}\t{reminder.date.hour:02}:{reminder.date.minute:02}",
                                               font=("Tahoma", 16), fg=colors.color_gray, bg=colors.color_white)
                reminder_date_label.grid(row=1, column=0, padx=10, pady=5, sticky="nsew")

                remove_reminder_btn = tk.Button(reminder_frame, text='🗑', width=3, height=1,
                                                bg=colors.color_white, bd=0, font=("Tahoma", 18),
                                                command=lambda idx=index: remove_reminder(idx))
                remove_reminder_btn.grid(row=0, column=1, padx=(0, 10), pady=10, sticky="nsew")

            for frame in reminder_frames:
                frame.grid_rowconfigure(0, weight=1)

            reminders_canvas.configure(yscrollcommand=reminders_scrollbar.set)

        def open_reminder_creation_window():
            def update_days(event=None):
                selected_month = month_combobox.get()
                month_number = months.index(selected_month) + 1
                days_in_month = calendar.monthrange(year, month_number)[1]
                current_day = datetime.datetime.now().day
                day_combobox['values'] = list(range(1, days_in_month + 1))
                day_combobox.set(current_day if current_day <= days_in_month else days_in_month)

            def create_reminder():
                text = reminder_text_entry.get("1.0", "end-1c").strip()
                if not text:
                    messagebox.showwarning("Попередження", "Текст не може бути пустим", parent=reminders_window)
                    return

                selected_month = month_combobox.get()
                month_number = months.index(selected_month) + 1
                day = int(day_combobox.get())
                hour = int(hours_combobox.get())
                minute = int(minutes_combobox.get())

                current_datetime = datetime.datetime.now()
                selected_datetime = datetime.datetime(current_datetime.year, month_number, day, hour, minute)

                if selected_datetime < current_datetime:
                    messagebox.showwarning("Попередження", "Вибраний час у минулому", parent=reminders_window)
                    return

                date = Date(month=month_number, day=day, hour=hour, minute=minute)
                reminder = Reminder(text, date)
                lists.reminders_items.append(reminder)
                Reminder.refresh_csv_file(csv_path, lists.reminders_items)
                reminders_window.destroy()
                Reminder.open_reminders_window(root)

            reminder_creation_window = tk.Toplevel(reminders_window)
            reminder_creation_window.title("Створити Нагадування")
            reminder_creation_window.geometry("750x500")
            reminder_creation_window.resizable(False, False)
            reminder_creation_window['bg'] = colors.color_aqua

            reminder_text_label = tk.Label(reminder_creation_window, text="Текст Нагадування:",
                                           font=("tahoma", 28, 'bold'),
                                           bg=colors.color_aqua, fg=colors.color_white)
            reminder_text_label.place(x=64, y=60)
            reminder_text_entry = tk.Text(reminder_creation_window, font=('tahoma', 18), width=50, height=2)
            reminder_text_entry.place(x=40, y=120)
            reminder_date_text = tk.Label(reminder_creation_window, text="Виберіть Дату:", font=("Tahoma", 22),
                                          bg=colors.color_aqua, fg = colors.color_white)
            reminder_date_text.place(x=40, y=200)
            month_text = tk.Label(reminder_creation_window, text="Місяць", font=("tahoma", 18), bg=colors.color_aqua,
                                  fg=colors.color_white)
            month_text.place(x=40, y=260)
            day_text = tk.Label(reminder_creation_window, text="День", font=("tahoma", 18), bg=colors.color_aqua,
                                fg=colors.color_white)
            day_text.place(x=40, y=300)
            hour_text = tk.Label(reminder_creation_window, text="Години", font=("tahoma", 18), bg=colors.color_aqua,
                                 fg=colors.color_white)
            hour_text.place(x=40, y=340)
            minute_text = tk.Label(reminder_creation_window, text="Хвилини", font=("tahoma", 18), bg=colors.color_aqua,
                                   fg=colors.color_white)
            minute_text.place(x=40, y=380)
            create_btn = tk.Button(reminder_creation_window, text="Створити", font=("tahoma", 18, 'bold'), padx=40,
                                   bg=colors.color_white, command=create_reminder)
            create_btn.place(x=460, y=400)
            months = [
                "Січень", "Лютий", "Березень", "Квітень", "Травень", "Червень",
                "Липень", "Серпень", "Вересень", "Жовтень", "Листопад", "Грудень"
            ]
            month_combobox = ttk.Combobox(reminder_creation_window, values=months, font=("tahoma", 18), width=12)
            month_combobox.place(x=220, y=260)
            current_month = datetime.datetime.now().month
            month_combobox.set(months[current_month - 1])
            month_combobox.bind("<<ComboboxSelected>>", update_days)
            year = datetime.datetime.now().year
            current_day = datetime.datetime.now().day
            day_combobox = ttk.Combobox(reminder_creation_window, font=("tahoma", 18), width=12)
            day_combobox.set(current_day)
            day_combobox.place(x=220, y=300)
            update_days()
            hours_combobox = ttk.Combobox(reminder_creation_window, values=list(range(1, 25)), font=("tahoma", 18),
                                          width=12)
            hours_combobox.place(x=220, y=340)
            hours_combobox.set(datetime.datetime.now().hour)
            minutes_combobox = ttk.Combobox(reminder_creation_window, values=list(range(1, 61)), font=("tahoma", 18),
                                            width=12)
            minutes_combobox.place(x=220, y=380)
            minutes_combobox.set(datetime.datetime.now().minute)
        reminders_window = tk.Toplevel(root)
        reminders_window.state('zoomed')
        wm.set_default(reminders_window, "Нагадування", root)
        Reminder.fill_items(csv_path, lists.reminders_items, Reminder)
        open_creation_window_btn = tk.Button(reminders_window, text="Створити Нагадування", font=("Tahoma", 16, 'bold'),
                                             bg=colors.color_white, padx=10, pady=5,
                                             command=open_reminder_creation_window)
        open_creation_window_btn.place(x=1086, y=44)
        if not lists.reminders_items:
            no_reminders_label = tk.Label(reminders_window, text="Нагадувань Немає",
                                          font=("Tahoma", 48, 'bold'),
                                          bg=colors.color_aqua, fg=colors.color_white)
            no_reminders_label.place(x=550, y=176)
        else:
            display_reminders()


def show_reminder_notification(reminder):
    def show_notification():
        current_time = datetime.datetime.now()
        reminder_time = datetime.datetime(current_time.year, reminder.date.month, reminder.date.day, reminder.date.hour, reminder.date.minute)

        if not reminder.displayed and current_time >= reminder_time:
            notification.notify(
                title="Нагадування",
                message=reminder.text,
                timeout=10
            )
            reminder.displayed = True

    notification_thread = threading.Thread(target=show_notification)
    notification_thread.start()