from credential import Credential
import globalvariables
import tkinter as tk
import constants
import json
import os

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
                data["creds"][idx]["service_name"], 
                data["creds"][idx]["service_url"], 
                data["creds"][idx]["username"], 
                data["creds"][idx]["password"],
                data["creds"][idx]["email"],
                data["creds"][idx]["ids"]
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
        cred_data["creds"].append(cred.return_as_dict())
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