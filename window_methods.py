from tkinter import messagebox
import services as sv
import Pomodoro as pm
import todolist as td
import notification as nt
import reminders as rm
import tasks

def open_tasks_window(root):
    sv.close_all_windows(root)
    tasks.Main_task.open_tasks_window(root)


def open_notes_window(root):
    sv.close_all_windows(root)
    nt.Notification.open_notifications_window(root)


def pomodoro_handler(root):
    sv.close_all_windows(root)
    pm.Pomodoro.open_pomodoro_window(root)


def open_reminders_window(root):
    sv.close_all_windows(root)
    rm.Reminder.open_reminders_window(root)

def todolist_handler(root):
    sv.close_all_windows(root)
    td.Todolist.open_todolist_window(root)

def set_default(window, title, root):
        sv.set_default_method(window, title, open_tasks_window, open_notes_window, pomodoro_handler,
                              open_reminders_window, todolist_handler, root)