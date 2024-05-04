import tkinter as tk
import csv
import colors
import lists
import window_methods as wm
import ItemsManager as im
import json
from tkinter import messagebox
from tkinter import ttk

csv_path = 'D:\LABY\LABY 3 KURS\CURSACH\\csvFiles\\tasks.csv'

class Main_task(im.ItemsManager):
    def __init__(self, name, description, secondary_tasks=None, done_status=False):
        self.name = name
        self.description = description
        self.secondary_tasks = secondary_tasks if secondary_tasks is not None else []
        self.done_status = done_status

    @classmethod
    def from_row(cls, row):
        if len(row) == 4:
            name, description, done_status_str, secondary_tasks_json = row
            done_status = done_status_str.lower() == "true"
            secondary_tasks = [Secondary_task(**subtask_data) for subtask_data in json.loads(secondary_tasks_json)]
            return cls(name, description, secondary_tasks=secondary_tasks, done_status=done_status)

    @staticmethod
    def open_tasks_window(root):
        def toggle_done_status(task):
            task.done_status = not task.done_status
            Main_task.save_items_to_csv(csv_path, lists.task_list)
            tasks_window.destroy()
            Main_task.open_tasks_window(root)
            root.update()

        def remove_task(task):
            confirmation = messagebox.askyesno("Видалення завдання", "Ви впевнені, що хочете видалити це завдання?", parent=tasks_window)
            if confirmation:
                lists.task_list.remove(task)
                for main_task in lists.task_list:
                    main_task.secondary_tasks = [subtask for subtask in main_task.secondary_tasks if
                                                 not subtask.name.startswith(f"{task.name}_")]
                Main_task.save_items_to_csv(csv_path, lists.task_list)
                tasks_window.destroy()
                Main_task.open_tasks_window(root)
                root.update()

        def display_tasks(event=None):

            tasks_frame = tk.Frame(tasks_window, bg=colors.color_aqua)
            tasks_frame.place(x=432, y=200, relwidth=0.6, height=500)

            tasks_canvas = tk.Canvas(tasks_frame, bg=colors.color_aqua, highlightthickness=0)
            tasks_canvas.grid(row=0, column=0, sticky="nsew")

            tasks_scrollbar = tk.Scrollbar(tasks_frame, orient="vertical", command=tasks_canvas.yview)
            tasks_scrollbar.grid(row=0, column=1, sticky="ns")

            tasks_inner_frame = tk.Frame(tasks_canvas, bg=colors.color_aqua)
            tasks_canvas.create_window((0, 0), window=tasks_inner_frame, anchor="nw")
            tasks_inner_frame.bind("<Configure>",
                                   lambda event: tasks_canvas.configure(scrollregion=tasks_canvas.bbox("all")))

            tasks_frame.grid_rowconfigure(0, weight=1)
            tasks_frame.grid_columnconfigure(0, weight=1)

            for widget in tasks_inner_frame.winfo_children():
                widget.destroy()

            filter_item = task_filter_combobox.get()
            num_columns = 2

            for index, task in enumerate(lists.task_list):
                if filter_item == "Усі" or (filter_item == "Виконані" and task.done_status) or (
                        filter_item == "Не Виконані" and not task.done_status):
                    column = index % num_columns
                    row = index // num_columns

                    task_frame = tk.Frame(tasks_inner_frame, bg=colors.color_white, relief="solid", borderwidth=1)
                    task_frame.grid(row=row, column=column, padx=10, pady=10, sticky="nsew")

                    task_title_button = tk.Button(task_frame, text=task.name, font=("Tahoma", 14), width=30,
                                                  bg=colors.color_white, bd=0,
                                                  command=lambda t=task: Main_task.open_task(root, t))
                    task_title_button.pack(padx=10, pady=(10, 5), anchor="w")

                    task_description_button = tk.Button(task_frame, text=task.description, font=("Tahoma", 12),
                                                        width=35,
                                                        height=2,
                                                        bg=colors.color_white, fg=colors.color_gray, bd=0,
                                                        wraplength=250,
                                                        command=lambda t=task: Main_task.open_task(root, t), anchor="w",
                                                        justify="left")
                    task_description_button.pack(padx=10, pady=(0, 10), anchor="w")

                    done_text = "✔" if task.done_status else ""
                    task_done_btn = tk.Button(task_frame, width=3, height=1, font=("Tahoma", 14), text=done_text,
                                              bg=colors.color_white, bd=1, relief="solid",
                                              highlightthickness=1, highlightbackground="black",
                                              command=lambda t=task: toggle_done_status(t))
                    task_done_btn.pack(side="left", padx=(10, 0), pady=10)

                    task_edit_btn = tk.Button(task_frame, text='🖉', width=3, height=1,
                                              bg=colors.color_white, bd=0, font=("Tahoma", 18),
                                              command=lambda t=task: open_task_edit_window(root, t))
                    task_edit_btn.pack(side="left", padx=(10, 0), pady=10)

                    remove_task_btn = tk.Button(task_frame, text='🗑', width=3, height=1,
                                                bg=colors.color_white, bd=0, font=("Tahoma", 18),
                                                command=lambda t=task: remove_task(t))
                    remove_task_btn.pack(side="right", padx=(0, 10), pady=10)

            tasks_canvas.configure(yscrollcommand=tasks_scrollbar.set)


        def open_task_edit_window(root, task):
            def on_text_change(event):
                if len(task_edit_text.get()) > 20:
                    task_edit_text.delete(20, tk.END)

                if len(description_edit_text.get("1.0", "end-1c")) > 60:
                    description_edit_text.delete("1.0", "end")
                    description_edit_text.insert("1.0", description_edit_text.get("1.0", "end-1c")[:60])

            def save_changes():
                new_name = task_edit_text.get().strip()
                new_description = description_edit_text.get("1.0", "end-1c").strip()
                if not new_name or not new_description:
                    messagebox.showwarning("Попередження", "Заповніть усі поля")
                    return
                task.name = new_name
                task.description = new_description
                Main_task.save_items_to_csv(csv_path, lists.task_list)
                task_edit_window.destroy()
                Main_task.open_tasks_window(root)

            task_edit_window = tk.Toplevel(root)
            task_edit_window.title("Редагування завдання")
            task_edit_window.geometry("750x400")
            task_edit_window.resizable(False, False)
            task_edit_window['bg'] = colors.color_aqua

            task_edit_label = tk.Label(task_edit_window, text="Назва завдання:", font=("tahoma", 28, 'bold'),
                                       bg=colors.color_aqua, fg=colors.color_white)
            task_edit_label.place(x=64, y=50)

            task_edit_text = tk.Entry(task_edit_window, width=45, font=("Tahoma", 18))
            task_edit_text.insert(tk.END, task.name)
            task_edit_text.place(x=64, y=112)
            task_edit_text.bind("<KeyRelease>", on_text_change)

            description_edit_label = tk.Label(task_edit_window, text="Опис завдання:", font=("tahoma", 28, 'bold'),
                                              bg=colors.color_aqua, fg=colors.color_white)
            description_edit_label.place(x=64, y=162)

            description_edit_text = tk.Text(task_edit_window, width=45, height=2, font=("Tahoma", 18))
            description_edit_text.insert("1.0", task.description)
            description_edit_text.place(x=64, y=224)
            description_edit_text.bind("<KeyRelease>", on_text_change)

            save_changes_btn = tk.Button(task_edit_window, text="Зберегти зміни", font=("Tahoma", 14, 'bold'),
                                         bg=colors.color_white, padx=10, pady=5, command=save_changes)
            save_changes_btn.place(x=455, y=320)
        tasks_window = tk.Toplevel(root)
        tasks_window.state('zoomed')
        wm.set_default(tasks_window, "Огранізатор Завдань", root)
        Main_task.fill_items(csv_path, lists.task_list, Main_task)

        create_task_btn = tk.Button(tasks_window, text="Створити завдання", font=("Tahoma", 16, 'bold'),
                                    bg=colors.color_white, padx=10, pady=5,
                                    command=lambda: open_task_creation_window())
        create_task_btn.place(x=1086, y=44)
        filter_options = ["Усі", "Виконані", "Не Виконані"]
        task_filter_combobox = ttk.Combobox(tasks_window, values=filter_options, font=("Tahoma", 18), width=15)
        task_filter_combobox.set("Усі")
        task_filter_combobox.place(x=850, y=55)
        task_filter_combobox.bind("<<ComboboxSelected>>", display_tasks)

        if not lists.task_list:
            no_tasks_label = tk.Label(tasks_window, text="Завдань Немає", font=("Tahoma", 48, 'bold'),
                                      bg=colors.color_aqua, fg=colors.color_white)
            no_tasks_label.place(x=550, y=176)
        else:
            display_tasks()

        def open_task_creation_window():
            task_creation_window = tk.Toplevel(tasks_window)
            task_creation_window.title("Створення завдання")
            task_creation_window.geometry("750x400")
            task_creation_window.resizable(False, False)
            task_creation_window['bg'] = colors.color_aqua

            task_creation_label = tk.Label(task_creation_window, text="Назва Завдання:", font=("tahoma", 16),
                                           bg=colors.color_aqua, fg=colors.color_white)
            task_creation_label.place(x=64, y=100)

            task_creation_text = tk.Entry(task_creation_window, width=30, font=("Tahoma", 18))
            task_creation_text.place(x=240, y=95)

            def limit_task_name(event):
                value = task_creation_text.get()
                if len(value) > 20:
                    task_creation_text.delete(20, tk.END)

            task_creation_text.bind("<KeyRelease>", limit_task_name)

            task_description_label = tk.Label(task_creation_window, text="Опис Завдання:", font=("tahoma", 16),
                                              bg=colors.color_aqua, fg=colors.color_white)
            task_description_label.place(x=64, y=170)

            task_description_text = tk.Text(task_creation_window, width=30, height=2, font=("Tahoma", 18))
            task_description_text.place(x=240, y=165)

            def limit_task_description(event):
                value = task_description_text.get("1.0", "end-1c")
                if len(value) > 60:
                    task_description_text.delete("1.0", "end")
                    task_description_text.insert("1.0", value[:60])

            task_description_text.bind("<KeyRelease>", limit_task_description)

            def create_task():
                task_text = task_creation_text.get()
                task_description = task_description_text.get("1.0", "end-1c")
                if not task_text or not task_description:
                    messagebox.showwarning("Попередження", "Заповніть усі поля.")
                    return

                existing_task = next((task for task in lists.task_list if task.name == task_text), None)
                if existing_task:
                    messagebox.showwarning("Попередження", "Завдання з таким іменем вже існує")
                    return

                task = Main_task(task_text, task_description)
                lists.task_list.append(task)
                Main_task.save_items_to_csv(csv_path, lists.task_list)
                tasks_window.destroy()
                Main_task.open_tasks_window(root)

            create_task_btn = tk.Button(task_creation_window, text="Створити Завдання", font=("Tahoma", 14, 'bold'),
                                        bg=colors.color_white, padx=10, pady=5,
                                        command=create_task)
            create_task_btn.place(x=455, y=270)

    @staticmethod
    def open_task(root, task):
        task_window = tk.Toplevel(root)
        task_window.state('zoomed')
        wm.set_default(task_window, task.name, root)

        task_title_label = tk.Label(task_window, text=task.name.upper(), font=("Tahoma", 54, 'bold'),
                                    bg=colors.color_aqua, fg=colors.color_white)
        task_description_label = tk.Label(task_window, text=task.description, font=("Tahoma", 18),
                                          fg=colors.color_gray, bg=colors.color_white, wraplength=350,
                                          anchor="w", justify="left", padx=50, pady=10)
        task_title_label.place(x=450, y=100)
        task_description_label.place(x=450, y=200)
        if not task.secondary_tasks:
            no_tasks_label = tk.Label(task_window, text="Вкладені Завдання Відсутні", font=("Tahoma", 18, 'bold'),
                                             fg=colors.color_white, bg=colors.color_aqua)
            no_tasks_label.place(x=450, y=300)
        else:
            secondary_tasks_label = tk.Label(task_window, text="Вкладені завдання:", font=("Tahoma", 18, 'bold'),
                                             fg=colors.color_white, bg=colors.color_aqua)
            secondary_tasks_label.place(x=450, y=300)

            secondary_tasks_frame = tk.Frame(task_window, bg=colors.color_aqua)
            secondary_tasks_frame.place(x=450, y=340, relwidth=0.6, height=500)

            secondary_tasks_canvas = tk.Canvas(secondary_tasks_frame, bg=colors.color_aqua, highlightthickness=0)
            secondary_tasks_canvas.grid(row=0, column=0, sticky="nsew")

            secondary_tasks_scrollbar = tk.Scrollbar(secondary_tasks_frame, orient="vertical",
                                                     command=secondary_tasks_canvas.yview)
            secondary_tasks_scrollbar.grid(row=0, column=1, sticky="ns")

            secondary_tasks_inner_frame = tk.Frame(secondary_tasks_canvas, bg=colors.color_aqua)
            secondary_tasks_canvas.create_window((0, 0), window=secondary_tasks_inner_frame, anchor="nw")
            secondary_tasks_inner_frame.bind("<Configure>", lambda event: secondary_tasks_canvas.configure(
                scrollregion=secondary_tasks_canvas.bbox("all")))

            secondary_tasks_frame.grid_rowconfigure(0, weight=1)
            secondary_tasks_frame.grid_columnconfigure(0, weight=1)

            secondary_task_frames = []
            num_columns = 2
            for index, sub_task in enumerate(task.secondary_tasks):
                column = index % num_columns
                row = index // num_columns

                sub_task_frame = tk.Frame(secondary_tasks_inner_frame, bg=colors.color_white, relief="solid",
                                          borderwidth=1)
                sub_task_frame.grid(row=row, column=column, padx=10, pady=10, sticky="nsew")
                secondary_task_frames.append(sub_task_frame)

                sub_task_frame.grid_columnconfigure(0, minsize=50)
                sub_task_frame.grid_columnconfigure(1, minsize=200)
                sub_task_frame.grid_columnconfigure(2, minsize=50)
                sub_task_frame.grid_columnconfigure(3, minsize=50)

                sub_task_text_label = tk.Label(sub_task_frame, text=sub_task.name, font=("Tahoma", 18),
                                               fg=colors.color_gray, bg=colors.color_white, wraplength=200,
                                               anchor="w", justify="left")
                sub_task_text_label.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

                done_text = "✔" if sub_task.done_status else ""
                sub_task_done_btn = tk.Button(sub_task_frame, width=2, font=("Tahoma", 14, "bold"), text=done_text,
                                              bg=colors.color_white, bd=1, relief="solid",
                                              highlightthickness=1, highlightbackground="black",
                                              command=lambda t=sub_task: toggle_done_status(task_window, task, t))
                sub_task_done_btn.config(height=1, pady=0)
                sub_task_done_btn.grid(row=0, column=0, padx=(10, 0), pady=10, sticky="nsew")

                sub_task_text_label = tk.Label(sub_task_frame, text=sub_task.name, font=("Tahoma", 18),
                                               fg=colors.color_gray, bg=colors.color_white, wraplength=200,
                                               anchor="w", justify="left")
                sub_task_text_label.grid(row=0, column=1, padx=(10, 0), pady=10, sticky="nsew")

                sub_task_edit_btn = tk.Button(sub_task_frame, text='🖉', width=2, height=2,
                                              bg=colors.color_white, bd=0, font=("Tahoma", 18),
                                              command=lambda t=sub_task: open_sub_task_edit_window(task_window, task,
                                                                                                   t))
                sub_task_edit_btn.grid(row=0, column=2, padx=(0, 10), pady=10, sticky="nsew")

                remove_sub_task_btn = tk.Button(sub_task_frame, text='🗑', width=2, height=2,
                                                bg=colors.color_white, bd=0, font=("Tahoma", 18),
                                                command=lambda t=sub_task: remove_sub_task(task_window, task, t))
                remove_sub_task_btn.grid(row=0, column=3, padx=(0, 10), pady=10, sticky="nsew")

            for frame in secondary_task_frames:
                frame.grid_rowconfigure(0, weight=1)

            secondary_tasks_canvas.configure(yscrollcommand=secondary_tasks_scrollbar.set)

        done_text = "Виконано ✔" if task.done_status else "Не Виконано"
        task_done_label = tk.Label(task_window, text=done_text, font=("Tahoma", 18, 'bold'),
                                   fg=colors.color_gray, bg=colors.color_white, padx=60)
        task_done_label.place(x=1150, y=60)

        add_secondary_task_btn = tk.Button(task_window, text="Вкласти Завдання", font=("tahoma", 16), bg=colors.color_white,
                                           padx=30, command=lambda: open_secondary_task_window(task, task_window))
        add_secondary_task_btn.place(x=800, y=55)

        def open_sub_task_edit_window(task_window, task, sub_task):
            def on_text_change(event):
                if len(sub_task_edit_text.get()) > 60:
                    sub_task_edit_text.delete(60, tk.END)

            def save_changes():
                new_text = sub_task_edit_text.get().strip()
                if not new_text:
                    messagebox.showwarning("Попередження", "Заповніть усі поля")
                    return
                sub_task.name = new_text
                Main_task.save_items_to_csv(csv_path, lists.task_list)
                sub_task_edit_window.destroy()
                task_window.destroy()
                Main_task.open_task(root, task)

            sub_task_edit_window = tk.Toplevel(task_window)
            sub_task_edit_window.title("Редагування вкладеного завдання")
            sub_task_edit_window.geometry("750x400")
            sub_task_edit_window.resizable(False, False)
            sub_task_edit_window['bg'] = colors.color_aqua

            sub_task_edit_label = tk.Label(sub_task_edit_window, text="Текст вкладеного завдання:",
                                           font=("tahoma", 28, 'bold'), bg=colors.color_aqua, fg=colors.color_white)
            sub_task_edit_label.place(x=64, y=100)

            sub_task_edit_text = tk.Entry(sub_task_edit_window, width=45, font=("Tahoma", 18))
            sub_task_edit_text.insert(tk.END, sub_task.name)
            sub_task_edit_text.place(x=64, y=162)
            sub_task_edit_text.bind("<KeyRelease>", on_text_change)

            save_changes_btn = tk.Button(sub_task_edit_window, text="Зберегти Зміни", font=("Tahoma", 14, 'bold'),
                                         bg=colors.color_white, padx=10, pady=5, command=save_changes)
            save_changes_btn.place(x=455, y=270)
        def toggle_done_status(task_window, task, sub_task):
            sub_task.done_status = not sub_task.done_status
            Main_task.save_items_to_csv(csv_path, lists.task_list)
            task_window.destroy()
            Main_task.open_task(task_window, task)

        def remove_sub_task(task_window, task, sub_task):
            task.secondary_tasks.remove(sub_task)
            Main_task.save_items_to_csv(csv_path, lists.task_list)
            task_window.destroy()
            Main_task.open_task(task_window, task)

        def open_secondary_task_window(task, root):
            secondary_task_window = tk.Toplevel(root)
            secondary_task_window.title("Вкласти Завдання")
            secondary_task_window.geometry("750x400")
            secondary_task_window.resizable(False, False)
            secondary_task_window['bg'] = colors.color_aqua

            task_creation_label = tk.Label(secondary_task_window, text="Опис Завдання:", font=("tahoma", 16),
                                           bg=colors.color_aqua, fg=colors.color_white)
            task_creation_label.place(x=64, y=100)

            task_creation_text = tk.Entry(secondary_task_window, width=30, font=("Tahoma", 18))
            task_creation_text.place(x=240, y=95)

            def create_secondary_task():
                task_text = task_creation_text.get()
                if not task_text:
                    messagebox.showwarning("Попередження", "Заповніть поле опису вкладеного завдання")
                    return

                secondary_task = Secondary_task(task_text)
                task.secondary_tasks.append(secondary_task)
                Main_task.save_items_to_csv(csv_path, lists.task_list)
                secondary_task_window.destroy()
                root.destroy()
                Main_task.open_task(root, task)

            create_task_btn = tk.Button(secondary_task_window, text="Створити Завдання", font=("Tahoma", 14, 'bold'),
                                        bg=colors.color_white, padx=10, pady=5,
                                        command=create_secondary_task)
            create_task_btn.place(x=455, y=270)

            def toggle_done_status(root, task, sub_task):
                sub_task.done_status = not sub_task.done_status
                Main_task.save_items_to_csv(csv_path, lists.task_list)
                root.destroy()
                Main_task.open_task(root, task)

            def remove_sub_task(task_window, task, sub_task):
                confirmation = messagebox.askyesno("Видалення вкладеного завдання",
                                                   "Ви впевнені, що хочете видалити це вкладене завдання?",
                                                   parent=task_window)
                if confirmation:
                    task.secondary_tasks.remove(sub_task)
                    Main_task.save_items_to_csv(csv_path, lists.task_list)
                    task_window.destroy()
                    Main_task.open_task(task_window, task)

    @staticmethod
    def save_items_to_csv(csv_path, items):
        with open(csv_path, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            for item in items:
                if isinstance(item, Main_task):
                    done_status_str = "True" if item.done_status else "False"
                    row = [item.name, item.description, done_status_str, json.dumps(
                        [{"name": subtask.name, "done_status": subtask.done_status} for subtask in
                         item.secondary_tasks])]
                    writer.writerow(row)

    @staticmethod
    def number_of_items():
        return im.ItemsManager.number_of_items(csv_path)

class Secondary_task:
    def __init__(self, name, done_status=False):
        self.name = name
        self.done_status = done_status