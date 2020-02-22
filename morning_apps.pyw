"""
Based of the tutorial by Dev Ed
YouTube URL: https://youtu.be/jE-SpRI3K5g
"""
import tkinter as tk
from tkinter import filedialog
import os
import tkinter.messagebox
apps = []


def read_file():
    if os.path.isfile('save.txt'):
        with open('save.txt', 'r') as f:
            temp_apps = f.read()
            temp_apps = temp_apps.split(',')
            apps = [x for x in temp_apps if x.strip()]

    for app in apps:
        label = tk.Label(frame, text=app, bg="gray")
        label.pack()


def add_app():
    global apps
    read_file()
    for widget in frame.winfo_children():
        widget.destroy()

    file_name = filedialog.askopenfilename(initialdir="/", title="Select File",
                                           filetypes=(("executables", "*.exe"), ("all files", "*.*")))
    if not file_name:
        read_file()
    else:
        apps.append(file_name)
    for app in apps:
        label = tk.Label(frame, text=app, bg="gray")
        label.pack()


def run_apps():
    if len(apps) != 0:
        for app in apps:
            os.startfile(app)
    else:
        tkinter.messagebox.showerror("No Apps Selected", "No Apps have been selected to run.")


root = tk.Tk()
root.resizable(0, 0)
root.title("Morning Apps Starter")
root.wm_iconbitmap("favicon.ico")


canvas = tk.Canvas(root, height=700, width=700, bg="#263D42")
canvas.pack()

menu_bar = tk.Menu(canvas)
file_menu = tk.Menu(menu_bar, tearoff=0)
file_menu.add_command(label="Open File", command=add_app)
file_menu.add_command(label="Run Apps", command=run_apps)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=root.quit)
menu_bar.add_cascade(label="File", menu=file_menu)

frame = tk.Frame(root, bg="white")
frame.place(relwidth=0.8, relheight=0.8, relx=0.1, rely=0.1)

open_file = tk.Button(root, text="Open File", padx=15, pady=5, fg="white", bg="#263D42", command=add_app)
open_file.pack(side="left", padx=100, pady=10)

run_apps = tk.Button(root, text="Run Apps", padx=15, pady=5, fg="white", bg="#263D42", command=run_apps)
run_apps.pack(side="right", padx=100, pady=10)


for app in apps:
    label = tk.Label(frame, text=app, bg="gray")
    label.pack()


read_file()
root.config(menu=menu_bar)
root.mainloop()

if len(apps) == 0:
    pass
else:
    with open('save.txt', 'w') as f:
        for app in apps:
            f.write(app + ',')
