import tkinter as tk
from tkinter import messagebox, simpledialog
import json
import os

FILE_NAME = "tasks.json"

# ------------------ Task Load/Save ------------------
def load_tasks():
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "r") as f:
            return json.load(f)
    return []

def save_tasks(tasks):
    with open(FILE_NAME, "w") as f:
        json.dump(tasks, f, indent=4)

# ------------------ GUI Functions ------------------
def refresh_listbox():
    listbox.delete(0, tk.END)
    for idx, task in enumerate(tasks):
        status = "✅" if task["done"] else "❌"
        listbox.insert(tk.END, f"{idx+1}. {task['title']} [{status}]")
        if task["done"]:
            listbox.itemconfig(idx, bg="#d4edda", fg="#155724")  # Light green
        else:
            listbox.itemconfig(idx, bg="#f8d7da", fg="#721c24")  # Light red

def add_task():
    title = simpledialog.askstring("Add Task", "Enter task title:")
    if title:
        tasks.append({"title": title, "done": False})
        save_tasks(tasks)
        refresh_listbox()

def mark_done():
    try:
        idx = listbox.curselection()[0]
        tasks[idx]["done"] = True
        save_tasks(tasks)
        refresh_listbox()
    except IndexError:
        messagebox.showwarning("Warning", "Select a task first!")

def delete_task():
    try:
        idx = listbox.curselection()[0]
        tasks.pop(idx)
        save_tasks(tasks)
        refresh_listbox()
    except IndexError:
        messagebox.showwarning("Warning", "Select a task first!")

# ------------------ Main GUI ------------------
tasks = load_tasks()
root = tk.Tk()
root.title("✨ To-Do List App ✨")
root.geometry("600x450")
root.minsize(400, 300)
root.config(bg="#f0f4f8")

# Make the grid expand
root.grid_columnconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=1)

# Title Label
title_label = tk.Label(root, text="📝 My Tasks", font=("Helvetica", 20, "bold"), bg="#f0f4f8", fg="#333")
title_label.grid(row=0, column=0, pady=10, sticky="n")

# Listbox Frame
frame = tk.Frame(root, bg="#f0f4f8")
frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

frame.grid_rowconfigure(0, weight=1)
frame.grid_columnconfigure(0, weight=1)

listbox = tk.Listbox(frame, font=("Helvetica", 12, "bold"), bd=0, highlightthickness=0, activestyle='none')
listbox.grid(row=0, column=0, sticky="nsew")

scrollbar = tk.Scrollbar(frame, orient=tk.VERTICAL, command=listbox.yview)
scrollbar.grid(row=0, column=1, sticky="ns")
listbox.config(yscrollcommand=scrollbar.set)

# Buttons Frame
button_frame = tk.Frame(root, bg="#f0f4f8")
button_frame.grid(row=2, column=0, pady=15, sticky="ew")
button_frame.grid_columnconfigure((0,1,2), weight=1)

btn_style = {"width": 15, "font": ("Helvetica", 12, "bold"), "bd": 0, "bg": "#007bff", "fg": "white", "activebackground": "#0056b3"}

add_btn = tk.Button(button_frame, text="Add Task", command=add_task, **btn_style)
add_btn.grid(row=0, column=0, padx=5, sticky="ew")

done_btn = tk.Button(button_frame, text="Mark Done", command=mark_done, **btn_style)
done_btn.grid(row=0, column=1, padx=5, sticky="ew")

del_btn = tk.Button(button_frame, text="Delete Task", command=delete_task, **btn_style)
del_btn.grid(row=0, column=2, padx=5, sticky="ew")

refresh_listbox()
root.mainloop()
