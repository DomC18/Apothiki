from PIL import ImageTk, ImageFilter, Image, ImageGrab
from credential import Credential
import globalvariables
import tkinter as tk
import constants
import credutil

class Listbox(tk.Frame):
    def __init__(self, master=None, root=tk.Tk, width=0, height=0, bg="white", **kwargs) -> None:
        super().__init__(master, **kwargs)
        self.canvas = tk.Canvas(self, width=width, height=height, bg=bg)
        self.list_frame = tk.Frame(self.canvas)
        self.bg_color = self.rgb_to_hex((235, 235, 235))
        self.root = root

        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas.create_window((0, 0), window=self.list_frame, anchor="nw")

        self.list_index:int

        self.peek_icon = tk.PhotoImage(file=constants.PEEKFILE)
        self.info_large_icon = tk.PhotoImage(file=constants.INFOLARGEFILE)
        self.info_icon = tk.PhotoImage(file=constants.INFOFILE)
        self.edit_large_icon = tk.PhotoImage(file=constants.EDITLARGEFILE)
        self.edit_icon = tk.PhotoImage(file=constants.EDITMEDIUMFILE)
        self.delete_icon = tk.PhotoImage(file=constants.DELETEMEDIUMFILE)
        self.filter_large_icon = tk.PhotoImage(file=constants.FILTERLARGEFILE)

        self.button_images : dict = {}
        self.cred_combos : dict = {}

        self.name_option = tk.Button()
        self.desc_option = tk.Button()
        self.deadline_option = tk.Button()
        self.status_option = tk.Button()
        self.importance_option = tk.Button()
        self.exit_option = tk.Button()

        self.curr_cred_service:str
        self.x:int
        self.y:int
        self.w:int
        self.h:int
        self.blurred_screenshot:Image
        self.screenshot:Image
        self.screenshot_photo:ImageTk.PhotoImage
        self.screenshot_label:tk.Label
        self.edit_large:tk.Button
        self.edit_label:tk.Label
        self.back_button:tk.Button

        self.filter_service:tk.Button
        self.filter_tag:tk.Button

        self.old_name:tk.Label
        self.old_desc:tk.Label
        self.old_dead:tk.Label
        self.old_status:tk.Label
        self.old_importance:tk.Label
        self.name_entry:tk.Entry
        self.desc_entry:tk.Entry
        self.status_entry:tk.OptionMenu
        self.status_var = tk.StringVar()
        self.importance_entry:tk.OptionMenu
        self.importance_var = tk.StringVar()

    def rgb_to_hex(self, rgb:tuple) -> str:
        return '#{:02x}{:02x}{:02x}'.format(*rgb)

    def del_row_elements(self):
        services = self.cred_combos.keys()

        for service in services:
            self.cred_combos[service][1].destroy()
            self.cred_combos[service][2].destroy()
            self.cred_combos[service][3].destroy()
            self.cred_combos[service][4].destroy()
            self.cred_combos[service][5].destroy()
            self.cred_combos[service][6].destroy()
            self.cred_combos[service][7].destroy()

    def insert(self, idx:int, cred:credutil.Credential) -> None:
        y_multiplier = 0.015 + (idx*0.13)
        
        service_label = tk.Label(self.canvas, text=cred.service, font=('Helvetica', 20))
        service_label.place(relx=0, rely=y_multiplier, anchor="nw")
        username_label = tk.Label(self.canvas, text=cred.username[:13], font=('Helvetica', 49))
        username_label.place(relx=0.01, rely=y_multiplier, anchor="nw")
        password_label = tk.Label(self.canvas, text="*****", font=('Helvetica', 49))
        password_label.place(relx=0.02, rely=y_multiplier, anchor="nw")
        
        peek_button = tk.Button(self.canvas, bd=0, bg=self.bg_color)
        self.button_images.update({peek_button:self.peek_icon})
        peek_button.configure()
        peek_button.configure(image=self.button_images[peek_button])
        peek_button.place(relx=0.875, rely=y_multiplier, anchor="ne")

        info_button = tk.Button(self.canvas, bd=0, bg=self.bg_color)
        self.button_images.update({info_button:self.info_icon})
        info_button.configure()
        info_button.configure(image=self.button_images[info_button])
        info_button.place(relx=0.975, rely=y_multiplier, anchor="ne")

        edit_button = tk.Button(self.canvas, bd=0, bg=self.bg_color)
        self.button_images.update({edit_button:self.edit_icon})
        edit_button.configure(command=lambda s=cred.service : self.edit_task_interface(s))
        edit_button.configure(image=self.button_images[edit_button])
        edit_button.place(relx=0.875, rely=y_multiplier, anchor="ne")
        
        delete_button = tk.Button(self.canvas, bd=0, bg=self.bg_color)
        self.button_images.update({delete_button:self.delete_icon})
        delete_button.configure(command=lambda b=delete_button : self.delete(b))
        delete_button.configure(image=self.button_images[delete_button])
        delete_button.place(relx=0.975, rely=y_multiplier, anchor="ne")
        
        self.cred_combos.update({cred.service:[cred.service, service_label, username_label, password_label, peek_button, info_button, edit_button, delete_button]})
    
    def move_down(self) -> None:
        if self.list_index+8 > len(globalvariables.user_creds):
            return

        self.list_index += 1
        self.del_row_elements()
        self.place_forget()

        for idx, cred in enumerate(globalvariables.user_creds):
            if idx < self.list_index:
                continue
            if idx > self.list_index + 6:
                break
            self.insert(idx-self.list_index, cred)
        self.pack()

    def move_up(self) -> None:
        if self.list_index <= 0:
            return
        
        self.list_index -= 1
        self.del_row_elements()
        self.place_forget()

        for idx, cred in enumerate(globalvariables.user_creds):
            if idx < self.list_index:
                continue
            if idx > self.list_index + 6:
                break
            self.insert(idx-self.list_index, cred)
        self.pack()

    def add_task(self) -> None:
        if credutil.amount_cred("url") == 1:
            return
            
        globalvariables.user_creds.insert(0, Credential())
        self.list_index = 0
        self.del_row_elements()
        self.place_forget()

        for idx, cred in enumerate(globalvariables.user_creds):
            if idx < self.list_index:
                continue
            if idx > self.list_index + 6:
                break
            self.insert(idx-self.list_index, cred)
        self.pack()

        credutil.save_creds()

    def filter_interface(self) -> None:
        self.x = self.root.winfo_rootx()
        self.y = self.root.winfo_rooty()
        self.w = self.root.winfo_width()
        self.h = self.root.winfo_height()
        self.screenshot = ImageGrab.grab(bbox=(self.x, self.y, self.x+self.w, self.y+self.h))
        self.screenshot_photo = ImageTk.PhotoImage(self.screenshot)
        self.screenshot_label = tk.Label(self.root, image=self.screenshot_photo)
        self.screenshot_label.image = self.screenshot_photo
        self.screenshot_label.pack()
        self.blurred_screenshot = self.screenshot.filter(ImageFilter.GaussianBlur(9))
        self.screenshot_photo = ImageTk.PhotoImage(self.blurred_screenshot)
        self.screenshot_label.configure(image=self.screenshot_photo)
        self.screenshot_label.image = self.screenshot_photo
        self.screenshot_label.pack()

        self.back_button = tk.Button(self.root, bg="white", fg="black", text="←", font=("Helvetica", 75, "bold"), relief="flat")
        self.back_button.configure(command=self.back_from_filter)
        self.back_button.place(relx=-0.005, rely=-0.055, anchor="nw")

        self.filter_large = tk.Label(self.root, image=self.filter_large_icon, bd=0, bg=self.bg_color)
        self.filter_large.place(relx=0.125, rely=0.5, anchor="center")

        self.filter_service = tk.Button(self.root, text="Filter by Service", bg="white", fg="black", font=("Times New Roman", 50, "bold"))
        self.filter_tag = tk.Button(self.root, text="Filter by Tag", bg="white", fg="black", font=("Times New Roman", 50, "bold"))
        self.filter_service.configure(command=self.service_sort)
        self.filter_tag.configure(command=self.tag_sort)
        self.filter_service.place(relx=0.5, rely=1/3, anchor="center")
        self.filter_tag.place(relx=0.5, rely=2/3, anchor="center")

    def service_sort(self) -> None:
        credutil.service_sort()
        self.back_from_filter()
    
    def tag_sort(self) -> None:
        credutil.tag_sort()
        self.back_from_filter()
    
    def back_from_filter(self) -> None:
        self.back_button.destroy()
        self.screenshot_label.destroy()
        self.filter_large.destroy()
        self.filter_service.destroy()
        self.filter_tag.destroy()

        self.del_row_elements()
        self.place_forget()
        for idx, cred in enumerate(globalvariables.user_creds):
            if idx < self.list_index:
                continue
            if idx > self.list_index + 6:
                break
            self.insert(idx-self.list_index, cred)
        self.pack()

    def edit_task_interface(self, service:str) -> None:
        self.curr_cred_service = service

        self.x = self.root.winfo_rootx()
        self.y = self.root.winfo_rooty()
        self.w = self.root.winfo_width()
        self.h = self.root.winfo_height()
        self.screenshot = ImageGrab.grab(bbox=(self.x, self.y, self.x+self.w, self.y+self.h))
        self.screenshot_photo = ImageTk.PhotoImage(self.screenshot)
        self.screenshot_label = tk.Label(self.root, image=self.screenshot_photo)
        self.screenshot_label.image = self.screenshot_photo
        self.screenshot_label.pack()
        self.blurred_screenshot = self.screenshot.filter(ImageFilter.GaussianBlur(9))
        self.screenshot_photo = ImageTk.PhotoImage(self.blurred_screenshot)
        self.screenshot_label.configure(image=self.screenshot_photo)
        self.screenshot_label.image = self.screenshot_photo
        self.screenshot_label.pack()

        self.back_button = tk.Button(self.root, bg="white", fg="black", text="←", font=("Helvetica", 75, "bold"), relief="flat")
        self.back_button.configure(command=self.back_from_edit)
        self.back_button.place(relx=-0.005, rely=-0.055, anchor="nw")

        self.old_service = tk.Label(self.root, text=service[:17], bg="black", fg="white", font=("Times New Roman", 60, "bold"))
        self.old_service.place(relx=0.25, rely=1/6, anchor="w")
        self.old_desc = tk.Label(self.root, text=credutil.find_cred(service).description, bg="black", fg="white", font=("Times New Roman", 60, "bold"))
        self.old_desc.place(relx=0.25, rely=2/6, anchor="w")
        self.old_dead = tk.Label(self.root, text=((credutil.find_cred(service).deadline + "*") if (credutil.find_cred(service).deadline == "00/00/0000") else (credutil.find_cred(service).deadline)), bg="black", fg="white", font=("Times New Roman", 60, "bold"))
        self.old_dead.place(relx=0.25, rely=3/6, anchor="w")
        self.old_status = tk.Label(self.root, text=credutil.find_cred(service).status, bg="black", fg="white", font=("Times New Roman", 60, "bold"))
        self.old_status.place(relx=0.25, rely=4/6, anchor="w")
        self.old_importance = tk.Label(self.root, text=credutil.find_cred(service).importance, bg="black", fg="white", font=("Times New Roman", 60, "bold"))
        self.old_importance.place(relx=0.25, rely=5/6, anchor="w")
        self.name_entry = tk.Entry(self.root, bg="black", fg="white", font=("Times New Roman", 60, "bold"), width=10)
        self.name_entry.place(relx=0.95, rely=1/6, anchor="e")
        self.desc_entry = tk.Entry(self.root, bg="black", fg="white", font=("Times New Roman", 60, "bold"), width=10)
        self.desc_entry.place(relx=0.95, rely=2/6, anchor="e")
        self.status_entry = tk.OptionMenu(self.root, self.status_var, "Not Started", "Delayed", "Underway", "Almost Completed", "Finished")
        self.status_entry.place(relx=0.95, rely=4/6, anchor="e")
        self.importance_entry = tk.OptionMenu(self.root, self.importance_var, "Minimal", "Trivial", "Average", "Significant", "Critical")
        self.importance_entry.place(relx=0.95, rely=5/6, anchor="e")

        self.edit_large = tk.Button(self.root, image=self.edit_large_icon, bd=0, bg=self.bg_color)
        self.edit_large.configure(command=lambda n=self.curr_cred_service, ne=self.name_entry, dese=self.desc_entry, se=self.status_var, ie=self.importance_var: self.edit_task(n, ne, dese, se, ie))
        self.edit_large.place(relx=0.125, rely=0.4, anchor="center")
        self.edit_label = tk.Label(self.root, text="Edit Task", justify="center", font=("Times New Roman", 52, "bold"), bg="white", fg="black")
        self.edit_label.place(relx=0.125, rely=0.575, anchor="center")
    
    def edit_task(self, service:str, service_entry:tk.Entry, username_entry:tk.Entry, password_entry:tk.Entry, email_entry:tk.Entry, tag_var:tk.StringVar, id_entry:tk.Entry) -> None:
        if not credutil.edit_cred(service, service_entry, username_entry, password_entry, email_entry, tag_var, id_entry):
            return
        self.back_from_edit()

        self.del_row_elements()
        self.place_forget()
        for idx, cred in enumerate(globalvariables.user_creds):
            if idx < self.list_index:
                continue
            if idx > self.list_index + 6:
                break
            self.insert(idx-self.list_index, cred)
        self.pack()

    def back_from_edit(self) -> None:
        self.back_button.destroy()
        self.screenshot_label.destroy()
        self.edit_large.destroy()
        self.edit_label.destroy()
        self.old_name.destroy()
        self.old_desc.destroy()
        self.old_dead.destroy()
        self.old_status.destroy()
        self.old_importance.destroy()
        self.name_entry.destroy()
        self.desc_entry.destroy()
        self.status_entry.destroy()
        self.importance_entry.destroy()

        self.status_var.set("")
        self.importance_var.set("")

    def delete(self, delete_button:tk.Button) -> None:
        cred_combos = self.cred_combos.values()
        
        for combo in cred_combos:
            if combo[7] == delete_button:
                service = combo[0]
        
        self.del_row_elements()
        self.cred_combos.pop(self.cred_combos[service][0])
        globalvariables.user_creds.pop(globalvariables.user_creds.index(credutil.find_cred(service)))
        self.place_forget()

        for idx, cred in enumerate(globalvariables.user_creds):
            if idx < self.list_index:
                continue
            if idx > self.list_index + 6:
                break
            self.insert(idx-self.list_index, cred)
        self.pack()