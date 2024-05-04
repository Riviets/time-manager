from tkinter import messagebox
import tkinter as tk
from PIL import Image, ImageTk
import colors
import window_methods as wm


class Pomodoro:

    def __init__(self, working_time, resting_time):
        self.working_time = working_time
        self.resting_time = resting_time
        self.timer_running = False
        self.remaining_time = 0

    @staticmethod
    def open_pomodoro_window(root):
        pomodoro_window = tk.Toplevel(root)
        pomodoro_window.state('zoomed')

        wm.set_default(pomodoro_window, "Помодоро", root)
        canvas = tk.Canvas(pomodoro_window, width=550, height=455, borderwidth=0, highlightthickness=0)
        canvas['bg'] = colors.color_aqua
        canvas.place(x=595, y=95)
        rectangle = canvas.create_rectangle(0, 155, 550, 455, fill=colors.color_lightyellow, outline='')
        circle = canvas.create_oval(150, 35, 400, 285, fill=colors.color_lightyellow, outline='')
        pomodoro_label = tk.Label(pomodoro_window, text="POMODORO", font=('Tahoma', 42, 'bold'),
                                  fg=colors.color_burgundy, bg=colors.color_lightyellow)
        pomodoro_label.place(x=700, y=274)
        working_label = tk.Label(pomodoro_window, text='Період роботи', font=('Tahoma', 12, 'bold'),
                                 bg=colors.color_lightyellow)
        working_label.place(x=658, y=362)
        resting_label = tk.Label(pomodoro_window, text='Період Відпочинку', font=('Tahoma', 12, 'bold'),
                                 bg=colors.color_lightyellow)
        resting_label.place(x=930, y=362)

        def on_validate(event):
            content = event.widget.get("1.0", "end-1c")
            if not content.isdigit() or len(content) > 2:
                event.widget.delete("end-2c", "end-1c")

        working_minutes_text = tk.Text(pomodoro_window, height=1, width=3, pady=5, padx=5, font=('Tahoma', 16))
        working_seconds_text = tk.Text(pomodoro_window, height=1, width=3, pady=5, padx=5, font=('Tahoma', 16))
        resting_minutes_text = tk.Text(pomodoro_window, height=1, width=3, pady=5, padx=5, font=('Tahoma', 16))
        resting_seconds_text = tk.Text(pomodoro_window, height=1, width=3, pady=5, padx=5, font=('Tahoma', 16))
        working_minutes_text.bind("<KeyRelease>", on_validate)
        working_seconds_text.bind("<KeyRelease>", on_validate)
        resting_minutes_text.bind("<KeyRelease>", on_validate)
        resting_seconds_text.bind("<KeyRelease>", on_validate)
        working_minutes_text.bind('<BackSpace>', lambda _: True)
        working_seconds_text.bind('<BackSpace>', lambda _: True)
        resting_minutes_text.bind('<BackSpace>', lambda _: True)
        resting_seconds_text.bind('<BackSpace>', lambda _: True)
        working_minutes_text.bind('<Delete>', lambda _: True)
        working_seconds_text.bind('<Delete>', lambda _: True)
        resting_minutes_text.bind('<Delete>', lambda _: True)
        resting_seconds_text.bind('<Delete>', lambda _: True)

        working_minutes_text.place(x=670, y=408)
        working_seconds_text.place(x=728, y=408)
        resting_minutes_text.place(x=942, y=408)
        resting_seconds_text.place(x=1000, y=408)
        confirm_btn = tk.Button(pomodoro_window, text='START', bg=colors.color_burgundy, fg=colors.color_white, width=25, font=('Tahoma', 16, 'bold'), pady=0,
                                command=lambda: Pomodoro.pomodoro_btn_action(working_minutes_text, working_seconds_text, resting_minutes_text, resting_seconds_text,pomodoro_window))
        confirm_btn.place(x=650, y=480)
        confirm_btn = tk.Button(pomodoro_window, text='STOP', bg=colors.color_gray, fg=colors.color_white,
                                width=5, font=('Tahoma', 16, 'bold'), pady=0, command=lambda: Pomodoro.stop_timer(working_minutes_text, working_seconds_text, resting_minutes_text, resting_seconds_text,
                            pomodoro_window))
        confirm_btn.place(x=1025, y=480)
        tomato_img_path = 'D:\LABY\LABY 3 KURS\CURSACH\images\\tomato.png'
        img = Image.open(tomato_img_path)
        img = img.resize((200, 200))
        Pomodoro.tk_img_tomato = ImageTk.PhotoImage(img)
        tomato_label = canvas.create_image(174, -10, anchor=tk.NW, image=Pomodoro.tk_img_tomato)


    @staticmethod
    def stop_timer(working_minutes_text, working_seconds_text, resting_minutes_text, resting_seconds_text,
                            pomodoro_window):
        global const_working_minutes, const_working_seconds, const_resting_minutes, const_resting_seconds
        working_minutes_text.delete("1.0", tk.END)
        working_seconds_text.delete("1.0", tk.END)
        resting_minutes_text.delete("1.0", tk.END)
        resting_seconds_text.delete("1.0", tk.END)
        working_minutes_text.insert(tk.END, f"{const_working_minutes}")
        working_seconds_text.insert(tk.END, f"{const_working_seconds}")
        resting_minutes_text.insert(tk.END, f"{const_resting_minutes}")
        resting_seconds_text.insert(tk.END, f"{const_resting_seconds}")
        Pomodoro.timer_running = False

    @staticmethod
    def pomodoro_btn_action(working_minutes_text, working_seconds_text, resting_minutes_text, resting_seconds_text,
                            pomodoro_window):
        global const_working_minutes, const_working_seconds, const_resting_minutes, const_resting_seconds
        working_minutes = int(working_minutes_text.get("1.0", "end-1c"))
        working_seconds = int(working_seconds_text.get("1.0", "end-1c"))
        resting_minutes = int(resting_minutes_text.get("1.0", "end-1c"))
        resting_seconds = int(resting_seconds_text.get("1.0", "end-1c"))
        const_working_minutes = working_minutes
        const_resting_minutes = resting_minutes
        const_working_seconds = working_seconds
        const_resting_seconds = resting_seconds

        if not (0 <= working_minutes < 60 and 0 <= working_seconds < 60 and
                0 <= resting_minutes < 60 and 0 <= resting_seconds < 60):
            messagebox.showinfo("Помилка", "Будь ласка, введіть коректний час.", parent=pomodoro_window)
            return

        Pomodoro.timer_running = True

        def countdown_work():
            nonlocal working_minutes, working_seconds, resting_minutes, resting_seconds

            if Pomodoro.timer_running:
                if working_minutes == 0 and working_seconds == 0:
                    messagebox.showinfo("Інформація", "Час відпочивати!", parent=pomodoro_window)
                    working_minutes = const_working_minutes
                    working_seconds = const_working_seconds
                    countdown_rest()
                    return

                if working_seconds == 0:
                    working_minutes -= 1
                    working_seconds = 59
                else:
                    working_seconds -= 1

                working_minutes_text.delete("1.0", "end")
                working_seconds_text.delete("1.0", "end")
                working_minutes_text.insert("1.0", str(working_minutes))
                working_seconds_text.insert("1.0", str(working_seconds))

                pomodoro_window.after(1000, countdown_work)

        def countdown_rest():
            nonlocal resting_minutes, resting_seconds, working_minutes, working_seconds

            if Pomodoro.timer_running:
                if resting_minutes == 0 and resting_seconds == 0:
                    messagebox.showinfo("Інформація", "Час Працювати", parent=pomodoro_window)
                    resting_minutes = const_resting_minutes
                    resting_seconds = const_resting_seconds
                    countdown_work()
                    return

                if resting_seconds == 0:
                    resting_minutes -= 1
                    resting_seconds = 59
                else:
                    resting_seconds -= 1

                resting_minutes_text.delete("1.0", "end")
                resting_seconds_text.delete("1.0", "end")
                resting_minutes_text.insert("1.0", str(resting_minutes))
                resting_seconds_text.insert("1.0", str(resting_seconds))

                pomodoro_window.after(1000, countdown_rest)

        countdown_work()
