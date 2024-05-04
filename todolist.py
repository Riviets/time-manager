import tkinter as tk
from tkinter import messagebox
import colors
import lists
import window_methods as wm
import ItemsManager as im
from tkinter import ttk

csv_path = 'D:\LABY\LABY 3 KURS\CURSACH\\csvFiles\\todolist-items.csv'

class Todolist(im.ItemsManager):
    def __init__(self, text, done):
        self.text = text
        self.done = done

    @staticmethod
    def from_row(row):
        if len(row) == 2:
            text = row[0]
            done = True if row[1].strip().lower() == 'true' else False
            return Todolist(text, done)
        else:
            raise ValueError("Unexpected number of columns in CSV row")

    def to_row(self):
        return [self.text, str(self.done)]

    @staticmethod
    def number_of_items():
        return im.ItemsManager.number_of_items(csv_path)

    @staticmethod
    def open_todolist_window(root):

        todolist_window = tk.Toplevel(root)
        todolist_window.state('zoomed')
        wm.set_default(todolist_window, "To-do list", root)

        def toggle_done_status(idx):
            lists.todolist_items[idx].done = not lists.todolist_items[idx].done
            Todolist.refresh_csv_file(csv_path, lists.todolist_items)
            display_todolist_items()

        def remove_item(idx):
            confirmed = messagebox.askyesno("Підтвердження", "Ви впевнені, що хочете видалити цю справу?",
                                            parent=todolist_window)
            if confirmed:
                lists.todolist_items.pop(idx)
                Todolist.refresh_csv_file(csv_path, lists.todolist_items)
                display_todolist_items()

        def display_todolist_items(event=None):
            for widget in todolist_inner_frame.winfo_children():
                widget.destroy()

            todolist_item_frames = []
            filter_item = todolist_filter_combobox.get()
            num_columns = 2

            for index, item in enumerate(lists.todolist_items):
                if filter_item == "Усі" or (filter_item == "Виконані" and item.done) or (
                        filter_item == "Не Виконані" and not item.done):
                    column = len(todolist_item_frames) % num_columns
                    row = len(todolist_item_frames) // num_columns

                    todolist_item_frame = tk.Frame(todolist_inner_frame, bg=colors.color_white, relief="solid",
                                                   borderwidth=1)
                    todolist_item_frame.grid(row=row, column=column, padx=10, pady=10, sticky="ew")
                    todolist_item_frames.append(todolist_item_frame)

                    todolist_item_frame.grid_columnconfigure(0, weight=1)
                    todolist_item_frame.grid_columnconfigure(1, minsize=50)

                    text = "✔" if item.done else ""
                    todolist_done_btn = tk.Button(todolist_item_frame, width=3, height=1, font=("Tahoma", 14),
                                                  text=text,
                                                  bg=colors.color_white, bd=1, relief="solid",
                                                  highlightthickness=1, highlightbackground="black",
                                                  command=lambda idx=index: toggle_done_status(idx))
                    todolist_done_btn.grid(row=0, column=0, padx=(20, 0), pady=17, sticky="w")

                    todolist_text_label = tk.Label(todolist_item_frame, text=item.text, font=("Tahoma", 18),
                                                   fg=colors.color_gray, bg=colors.color_white, wraplength=200,
                                                   anchor="w", justify="left", padx=20)
                    todolist_text_label.grid(row=0, column=1, padx=(10, 0), pady=17, sticky="ew")

                    todolist_edit_btn = tk.Button(todolist_item_frame, text='🖉', width=3, height=1,
                                                  bg=colors.color_white, bd=0, font=("Tahoma", 18),
                                                  command=lambda idx=index: open_todolist_edit_window(idx))
                    todolist_edit_btn.grid(row=0, column=2, padx=(0, 10), pady=17, sticky="e")

                    remove_item_btn = tk.Button(todolist_item_frame, text='🗑', width=3, height=1,
                                                bg=colors.color_white, bd=0, font=("Tahoma", 18),
                                                command=lambda idx=index: remove_item(idx))
                    remove_item_btn.grid(row=0, column=3, padx=(0, 10), pady=17, sticky="e")

            todolist_inner_frame.update_idletasks()

        def open_todolist_edit_window(idx):
            todolist_edit_window = tk.Toplevel(todolist_window)
            todolist_edit_window.title("Редагування Справи")
            todolist_edit_window.geometry("750x400")
            todolist_edit_window.resizable(False, False)
            todolist_edit_window['bg'] = colors.color_aqua
            todolist_edit_label = tk.Label(todolist_edit_window, text="Текст Справи:",
                                               font=("tahoma", 28, 'bold'), bg=colors.color_aqua)
            todolist_edit_label.place(x=64, y=100)

            def on_entry_change(event):
                text = todolist_edit_text.get("1.0", "end-1c")
                if len(text) > 60:
                    todolist_edit_text.delete("end-2c")

            todolist_edit_text = tk.Text(todolist_edit_window, width=45, height=2, pady=5, padx=10,
                                         font=("Tahoma", 18))
            todolist_edit_text.insert(tk.END, lists.todolist_items[idx].text)
            todolist_edit_text.place(x=64, y=162)
            todolist_edit_text.bind("<KeyRelease>", on_entry_change)

            def save_changes():
                new_text = todolist_edit_text.get("1.0", tk.END).strip()
                if not new_text:
                    messagebox.showwarning("Попередження", "Заповніть поле для тексту")
                    return
                lists.todolist_items[idx].text = new_text
                Todolist.refresh_csv_file(csv_path, lists.todolist_items)
                todolist_edit_window.destroy()
                display_todolist_items()

            save_changes_btn = tk.Button(todolist_edit_window, text="Зберегти Зміни", font=("Tahoma", 14, 'bold'),
                                         bg=colors.color_white, padx=10, pady=5, command=save_changes)
            save_changes_btn.place(x=455, y=270)

        todolist_inner_frame = tk.Frame(todolist_window, bg=colors.color_aqua)
        todolist_inner_frame.place(x=432, y=200, relwidth=0.6, height=500)

        Todolist.fill_items(csv_path, lists.todolist_items, Todolist)

        create_todolist_item_btn = tk.Button(todolist_window, text="Додати Справу", font=("Tahoma", 16, 'bold'),
                                             bg=colors.color_white, padx=10, pady=5,
                                             command=lambda: open_todolist_creation_window())
        create_todolist_item_btn.place(x=1086, y=44)

        filter_options = ["Усі", "Виконані", "Не Виконані"]
        todolist_filter_combobox = ttk.Combobox(todolist_window, values=filter_options, font=("Tahoma", 18), width=15)
        todolist_filter_combobox.set("Усі")
        todolist_filter_combobox.place(x=850, y=55)

        todolist_filter_combobox.bind("<<ComboboxSelected>>", display_todolist_items)

        if len(lists.todolist_items) == 0:
            no_items_label = tk.Label(todolist_window, text="Елементів Немає", font=("Tahoma", 48, 'bold'),
                                      bg=colors.color_aqua, fg=colors.color_white)
            no_items_label.place(x=550, y=176)
        else:
            display_todolist_items()

        def open_todolist_creation_window():
            todolist_creation_window = tk.Toplevel(todolist_window)
            todolist_creation_window.title("Створення Справи")
            todolist_creation_window.geometry("750x400")
            todolist_creation_window.resizable(False, False)
            todolist_creation_window['bg'] = colors.color_aqua

            todolist_creation_label = tk.Label(todolist_creation_window, text="Текст Справи:",
                                               font=("tahoma", 28, 'bold'), bg=colors.color_aqua, fg=colors.color_white)
            todolist_creation_label.place(x=64, y=100)

            def on_entry_change(event):
                text = todolist_creation_text.get("1.0", "end-1c")
                if len(text) > 60:
                    todolist_creation_text.delete("end-2c")

            def on_enter(event):
                return "break"

            todolist_creation_text = tk.Text(todolist_creation_window, width=45, height=2, pady=5, padx=10,
                                             font=("Tahoma", 18))
            todolist_creation_text.place(x=64, y=162)
            todolist_creation_text.bind("<KeyRelease>", on_entry_change)
            todolist_creation_text.bind("<Return>", on_enter)

            def create_todolist_item():
                todolist_item_text = todolist_creation_text.get("1.0", "end-1c")
                if not todolist_item_text:
                    messagebox.showwarning("Попередження", "Введіть Текст Справи.")
                    return
                todolist_obj = Todolist(todolist_item_text[:60], False)
                lists.todolist_items.append(todolist_obj)
                Todolist.refresh_csv_file(csv_path, lists.todolist_items)
                todolist_creation_window.destroy()
                todolist_window.destroy()
                Todolist.open_todolist_window(root)

            create_todolist_item_btn = tk.Button(todolist_creation_window, text="Створити Справу",
                                                 font=("Tahoma", 14, 'bold'),
                                                 bg=colors.color_white, padx=10, pady=5,
                                                 command=create_todolist_item)
            create_todolist_item_btn.place(x=455, y=270)
