from credential import Credential
from tkinter import messagebox
import globalvariables
import tkinter as tk
import constants
import json
import os

def amount_cred(service:str) -> int:
    cred_num = 0
    for cred in globalvariables.user_creds:
        if cred.service == service:
            cred_num += 1
    return cred_num

def find_cred(service:str) -> Credential:
    for cred in globalvariables.user_creds:
        if cred.service == service:
            return cred
    return None

def edit_cred(service:str, service_entry:tk.Entry, username_entry:tk.Entry, password_entry:tk.Entry, email_entry:tk.Entry, tag_var:tk.StringVar, info_entry:tk.Entry) -> bool:
    cred_index = globalvariables.user_creds.index(find_cred(service))

    if globalvariables.user_creds[cred_index].tag == "" and tag_var.get() == "":
        messagebox.showerror("Tag Error", "Please select a tag from the dropdown")
        return False

    if tag_var.get() != "":
        globalvariables.user_creds[cred_index].tag = tag_var.get()
    if service_entry.get() != "":
        globalvariables.user_creds[cred_index].service = service_entry.get()
    if username_entry.get() != "":
        globalvariables.user_creds[cred_index].username = username_entry.get()
    if password_entry.get() != "":
        globalvariables.user_creds[cred_index].password = password_entry.get()
    if email_entry.get() != "":
        globalvariables.user_creds[cred_index].email = email_entry.get()
    if info_entry.get() != "":
        globalvariables.user_creds[cred_index].info = info_entry.get()
    
    return True

def service_sort() -> None:
    globalvariables.user_creds.sort(key=lambda cred : cred.service)

def tag_sort() -> None:
    globalvariables.user_creds.sort(key=lambda cred : cred.tag)

def load_creds() -> None:
    data:dict = {}
    file_dir = rf"{constants.USERDATADIR+globalvariables.name}.json"

    try:
        with open(file_dir, "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        return
    
    for idx in range(len(data["creds"])):
        globalvariables.user_creds.append(
            Credential(
                data["creds"][idx]["service"], 
                data["creds"][idx]["username"], 
                data["creds"][idx]["password"],
                data["creds"][idx]["email"],
                data["creds"][idx]["tag"],
                data["creds"][idx]["info"]
            ))

def save_creds() -> None:
    data:dict = {}
    file_dir = rf"{constants.USERDATADIR+globalvariables.name}.json"

    data = {
        globalvariables.name: {
            "username": globalvariables.username,
            "password": globalvariables.password
        }
    }

    cred_data = {"creds": []}
    for cred in globalvariables.user_creds:
        cred_data["creds"].append(cred.cred_as_dict())
    data.update(cred_data)

    try:
        os.remove(file_dir)
    except FileNotFoundError:
        return
    
    with open(file_dir, "w") as file:
        json.dump(data, file, indent=4)

def sign_out(root:tk.Tk, init_func) -> None:
    save_creds()
    root.destroy()
    init_func()