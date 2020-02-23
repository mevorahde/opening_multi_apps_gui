"""
Idea based of the tutorial by Dev Ed
YouTube URL: https://youtu.be/jE-SpRI3K5g
Enhancements made by @mevorahde
V1.0 Created on Sat Feb 22 2020
"""
import tkinter as tk
from tkinter import filedialog
import os
import tkinter.messagebox
apps = []


def start_file():
    global apps
    if os.path.isfile('save.txt'):
        with open('save.txt', 'r') as f:
            temp_apps = f.read()
            temp_apps = temp_apps.split(',')
            apps = [x for x in temp_apps if x.strip()]

    for app in apps:
        list_box.insert(tk.END, app)
        list_box.pack()

        # list_box.insert(tk.END, apps[app])


def read_file():
    global apps
    if os.path.isfile('save.txt'):
        with open('save.txt', 'r') as f:
            temp_apps = f.read()
            temp_apps = temp_apps.split(',')
            apps = [x for x in temp_apps if x.strip()]


def write_file():
    if len(apps) == 0:
        pass
    else:
        with open('save.txt', 'w') as f:
            for app in apps:
                f.write(app + ',')


def modify_file():
    with open('save.txt', 'w') as f:
        for app in apps:
            f.write(app + ',')


def add_app():
    global apps
    for widget in list_box.winfo_children():
        widget.destroy()

    file_name = filedialog.askopenfilename(initialdir="/", title="Select File",
                                           filetypes=(("executables", "*.exe"), ("all files", "*.*")))
    if not file_name:
        read_file()
    else:
        apps.append(file_name)
        list_box.insert(tk.END, file_name)
        list_box.pack()
    write_file()
    read_file()


def deselect_app():
    list_box.select_clear(tk.END)


def run_apps():
    current_selection = list_box.curselection()
    if current_selection:
        result = tkinter.messagebox.askquestion("Run Confirmation", "Are you sure you only want to run this program?")
        if result == "yes":
            item = list_box.get(current_selection)
            os.startfile(item)
        deselect_app()
    else:
        if len(apps) != 0:
            for app in apps:
                os.startfile(app)
        else:
            tkinter.messagebox.showerror("No Apps Selected", "No Apps have been selected to run.")


def delete_app():
    global apps
    result = tkinter.messagebox.askquestion("Delete Confirmation", "Are you sure you want to delete this program?")
    if result == 'yes':
        current_selection = list_box.curselection()
        if not current_selection:
            tkinter.messagebox.showerror("No App Selected", "No App has been selected to delete.")
        else:
            item = list_box.get(current_selection)
            if item in apps:
                apps.remove(item)
            list_box.delete(current_selection)
            modify_file()
    else:
        deselect_app()


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
file_menu.add_command(label="Delete App", command=delete_app)
file_menu.add_command(label="Deselect App", command=deselect_app)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=root.quit)
menu_bar.add_cascade(label="File", menu=file_menu)

frame = tk.Frame(root, bg="white")
frame.place(relwidth=0.8, relheight=0.8, relx=0.1, rely=0.1)

list_box = tk.Listbox(frame, width=640, height=640, activestyle="none")
list_box.pack()

open_file = tk.Button(root, text="Open File", padx=15, pady=5, fg="white", bg="#263D42", command=add_app)
open_file.pack(side="left", padx=50, pady=10)

delete_app = tk.Button(root, text="Delete App", padx=15, pady=5, fg="white", bg="#263D42", command=delete_app)
delete_app.pack(side="right", padx=75, pady=10)

run_apps = tk.Button(root, text="Run Apps", padx=15, pady=5, fg="white", bg="#263D42", command=run_apps)
run_apps.pack(side="right", padx=50, pady=10)

start_file()
root.config(menu=menu_bar)
root.mainloop()

write_file()
