from loginutil import verify_existing
import genmethods as gen
import tkinter as tk

root:tk.Tk

def init() -> None:
    global root
    root = tk.Tk()
    root.title("Apothiki")
    root.configure(bg="light blue")

    width = 1175
    height = 625
    horiz_offset = (root.winfo_screenwidth() - width) / 2
    vert_offset = (root.winfo_screenheight() - height) / 2
    root.geometry(f"{width}x{height}+{int(horiz_offset)}+{int(vert_offset)}")
    root.resizable(False, False)

    logo_label = tk.Label(root, text="Apothiki Login", font=("Arial", 80), bg="light blue", justify="center")
    logo_label.grid(row=0, column=0, columnspan=2, pady=20)

    firstname_label = tk.Label(root, text="*First Name:", font=("Arial", 50), bg="light blue", justify="center")
    firstname_label.grid(row=1, column=0, padx=10, pady=5, sticky="e")

    firstname_entry = tk.Entry(root, font=("Arial", 50), justify="left")
    firstname_entry.grid(row=1, column=1, padx=10, pady=5)

    username_label = tk.Label(root, text="*Username:", font=("Arial", 50), bg="light blue", justify="center")
    username_label.grid(row=2, column=0, padx=10, pady=5, sticky="e")

    username_entry = tk.Entry(root, font=("Arial", 50), justify="left")
    username_entry.grid(row=2, column=1, padx=10, pady=5)

    password_label = tk.Label(root, text="*Password:", font=("Arial", 50), bg="light blue", justify="center")
    password_label.grid(row=3, column=0, padx=10, pady=5, sticky="e")

    password_entry = tk.Entry(root, show="*", font=("Arial", 50), justify="left")
    password_entry.grid(row=3, column=1, padx=10, pady=5)

    login_button = tk.Button(root, text="Login/Register", font=("Arial", 50), bg="green", fg="white", width=15, justify="center", command=lambda r=root, f=firstname_entry, u=username_entry, p=password_entry, fl=firstname_label, ul=username_label, pl=password_label, func=init_task_interface : verify_existing(r,f,u,p,fl,ul,pl,func))
    login_button.grid(row=4, column=0, columnspan=2, pady=20)

    def exit(event:tk.Event) -> None:
        root.destroy()

    root.bind("<Escape>", exit)
    root.mainloop()

def init_task_interface() -> None:
    global root
    root = tk.Tk()
    root.title("Apothiki")
    root.configure(bg="red")
    label = tk.Label(root, text="Apothiki", font=("Arial", 80), bg="light blue", justify="center")
    label.place(relx=0.5, rely=0.1, anchor=tk.CENTER)
    root.mainloop()