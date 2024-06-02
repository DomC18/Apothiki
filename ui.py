from loginutil import verify_existing
from listbox import Listbox
import tkinter as tk
import globalvariables as globalvar
import constants
import credutil

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
    
    width = 1440
    height = 810
    horiz_offset = (root.winfo_screenwidth() - width) / 2
    vert_offset = (root.winfo_screenheight() - height) / 2
    root.geometry(f"{width}x{height}+{int(horiz_offset)}+{int(vert_offset)}")
    root.resizable(False, False)

    util_frame = tk.Frame(root, bg="red")
    util_frame.place(relx=0, rely=0, anchor="nw")
    search_frame = tk.Frame(root, bg="red")
    search_frame.place(relx=0.5, rely=0, anchor="n")
    profile_frame = tk.Frame(root, bg="red")
    profile_frame.place(relx=1, rely=0, anchor="ne")
    cred_frame = tk.Frame(root)
    cred_frame.place(relx=0.5, rely=1, anchor="s")

    cred_list = Listbox(cred_frame, root, 826, 676, "grey", util_frame)
    cred_list.list_index = 0
    for idx, task in enumerate(globalvar.user_creds):
        if idx < cred_list.list_index:
            continue
        if idx > cred_list.list_index + 6:
            break
        cred_list.insert(idx-cred_list.list_index, task)
    cred_list.pack()

    search_entry = tk.Entry(search_frame, bd=0, bg="#ffabab", fg="black", font=("Times New Roman", 35, "bold"), width=20)
    search_entry.grid(row=0, column=0, padx=10, pady=10)
    search_icon = tk.PhotoImage(file=constants.SEARCHFILE)
    search_button = tk.Button(search_frame, image=search_icon, bd=0, bg="red", command=lambda e=search_entry, f=cred_list.filter_insert, b=cred_list.back_from_search : credutil.search_creds(e,f,b))
    search_button.grid(row=0, column=1)

    save_icon = tk.PhotoImage(file=constants.SAVEFILE)
    save_button = tk.Button(util_frame, image=save_icon, bd=0, bg="red", command=credutil.save_creds)
    save_button.grid(row=0, column=0)
    save_label = tk.Label(util_frame, text="Save", justify="center", font=("Times New Roman", 40), bg="red", fg="black")
    save_label.grid(row=0,column=1)
    filter_icon = tk.PhotoImage(file=constants.FILTERFILE)
    filter_button = tk.Button(util_frame, image=filter_icon, bd=0, bg="red")
    filter_button.configure(command=cred_list.filter_interface)
    filter_button.grid(row=1, column=0)
    filter_label = tk.Label(util_frame, text="Filter", justify="center", font=("Times New Roman", 40), bg="red", fg="black")
    filter_label.grid(row=1, column=1)

    profile_label = tk.Label(profile_frame, text="Log Out", justify="center", font=("Times New Roman", 46), bg="red", fg="black")
    profile_label.grid(row=0, column=0)
    profile_icon = tk.PhotoImage(file=constants.PROFILEFILE)
    profile_button = tk.Button(profile_frame, image=profile_icon, bd=0, bg="red", command=lambda r=root, i=init : credutil.sign_out(r, i))
    profile_button.grid(row=0, column=1)

    up_button = tk.Button(root, bd=0, text="↑", bg="red", fg="black", font=("Times New Roman", 46, "bold"))
    up_button.configure(command=cred_list.move_up)
    up_button.place(relx=0.7875, rely=0.1675, anchor="nw")
    down_button = tk.Button(root, bd=0, text="↓", bg="red", fg="black", font=("Times New Roman", 46, "bold"))
    down_button.configure(command=cred_list.move_down)
    down_button.place(relx=0.7875, rely=0.9875, anchor="sw")

    add_icon = tk.PhotoImage(file=constants.ADDFILE)
    add_button = tk.Button(root, image=add_icon, bg="red", bd=0)
    add_button.configure(command=cred_list.add_task)
    add_button.place(relx=0.9, rely=0.5, anchor="center")
    add_label = tk.Label(root, text="Add Service", justify="center", font=("Times New Roman", 35), bg="red", fg="black")
    add_label.place(relx=0.9, rely=0.6, anchor="center")

    def exit(event:tk.Event) -> None:
        root.destroy()

    root.bind("<Escape>", exit)
    root.mainloop()