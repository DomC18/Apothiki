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
        self.bg = bg
        self.list_index:int
        self.root = root

        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas.create_window((0, 0), window=self.list_frame, anchor="nw")

        self.peek_icon = tk.PhotoImage(file=constants.PEEKFILE)
        self.info_large_icon = tk.PhotoImage(file=constants.INFOLARGEFILE)
        self.info_icon = tk.PhotoImage(file=constants.INFOFILE)
        self.edit_large_icon = tk.PhotoImage(file=constants.EDITLARGEFILE)
        self.edit_icon = tk.PhotoImage(file=constants.EDITMEDIUMFILE)
        self.delete_icon = tk.PhotoImage(file=constants.DELETEMEDIUMFILE)
        self.filter_large_icon = tk.PhotoImage(file=constants.FILTERLARGEFILE)

        self.cred_state : dict = {}
        self.cred_labels : dict = {}
        self.button_images : dict = {}
        self.cred_combos : dict = {}

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


        self.old_service:tk.Label
        self.old_username:tk.Label
        self.old_password:tk.Label
        self.old_email:tk.Label
        self.old_tag:tk.Label
        self.old_info:tk.Label
    
        self.service_entry:tk.Entry
        self.username_entry:tk.Entry
        self.password_entry:tk.Entry
        self.email_entry:tk.Entry
        self.tag_entry:tk.OptionMenu
        self.tag_var = tk.StringVar()
        self.tag_var.set("")
        self.info_entry:tk.Entry

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
        y_multiplier = 0.0275 + (idx*0.13)
        service_multiplier = 0.041 + (idx*0.13)
        button_y_multiplier = 0.015 + (idx*0.13)
        self.cred_state.update({cred.service: [y_multiplier, 0, service_multiplier]})
        
        service_label = tk.Label(self.canvas, text=cred.service[:13], font=('Helvetica', 15), bg=self.bg_color, fg="black")
        service_label.place(relx=0, rely=service_multiplier, anchor="nw")
        username_label = tk.Label(self.canvas, text=cred.username[:13], font=('Helvetica', 30), bg=self.bg_color, fg="black")
        username_label.place(relx=0.45, rely=y_multiplier, anchor="ne")
        password_label = tk.Label(self.canvas, text="*****", font=('Helvetica', 30), bg=self.bg_color, fg="black")
        password_label.place(relx=0.975-(4.55*0.0925), rely=y_multiplier, anchor="ne")
        self.cred_labels.update({cred.service: [service_label, username_label, password_label]})
        
        peek_button = tk.Button(self.canvas, bd=0, bg=self.bg)
        self.button_images.update({peek_button:self.peek_icon})
        peek_button.configure(command=lambda s=cred.service : self.toggle_peek(s))
        peek_button.configure(image=self.button_images[peek_button])
        peek_button.place(relx=0.975-(3*0.0925), rely=button_y_multiplier, anchor="ne")

        info_button = tk.Button(self.canvas, bd=0, bg=self.bg)
        self.button_images.update({info_button:self.info_icon})
        info_button.configure(command=lambda s=cred.service : self.info_interface(s))
        info_button.configure(image=self.button_images[info_button])
        info_button.place(relx=0.975-(2*0.0925), rely=button_y_multiplier, anchor="ne")

        edit_button = tk.Button(self.canvas, bd=0, bg=self.bg)
        self.button_images.update({edit_button:self.edit_icon})
        edit_button.configure(command=lambda s=cred.service : self.edit_task_interface(s))
        edit_button.configure(image=self.button_images[edit_button])
        edit_button.place(relx=0.975-0.0925, rely=button_y_multiplier, anchor="ne")
        
        delete_button = tk.Button(self.canvas, bd=0, bg=self.bg)
        self.button_images.update({delete_button:self.delete_icon})
        delete_button.configure(command=lambda b=delete_button : self.delete(b))
        delete_button.configure(image=self.button_images[delete_button])
        delete_button.place(relx=0.975, rely=button_y_multiplier, anchor="ne")
        
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
        if credutil.amount_cred("service") == 1:
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

        found_service = credutil.find_cred(service)
        self.old_service = tk.Label(self.root, text=service[:17], bg="black", fg="white", font=("Times New Roman", 60, "bold"))
        self.old_service.place(relx=0.25, rely=1/7, anchor="w")
        self.old_username = tk.Label(self.root, text=found_service.username, bg="black", fg="white", font=("Times New Roman", 60, "bold"))
        self.old_username.place(relx=0.25, rely=2/7, anchor="w")
        self.old_password = tk.Label(self.root, text=found_service.password, bg="black", fg="white", font=("Times New Roman", 60, "bold"))
        self.old_password.place(relx=0.25, rely=3/7, anchor="w")
        self.old_email = tk.Label(self.root, text=found_service.email, bg="black", fg="white", font=("Times New Roman", 60, "bold"))
        self.old_email.place(relx=0.25, rely=4/7, anchor="w")
        self.old_tag = tk.Label(self.root, text=found_service.tag, bg="black", fg="white", font=("Times New Roman", 60, "bold"))
        self.old_tag.place(relx=0.25, rely=5/7, anchor="w")
        self.old_info = tk.Label(self.root, text=found_service.other_info, bg="black", fg="white", font=("Times New Roman", 60, "bold"))
        self.old_info.place(relx=0.25, rely=6/7, anchor="w")

        self.service_entry = tk.Entry(self.root, bg="black", fg="white", font=("Times New Roman", 60, "bold"), width=10)
        self.service_entry.place(relx=0.95, rely=1/7, anchor="e")
        self.username_entry = tk.Entry(self.root, bg="black", fg="white", font=("Times New Roman", 60, "bold"), width=10)
        self.username_entry.place(relx=0.95, rely=2/7, anchor="e")
        self.password_entry = tk.Entry(self.root, bg="black", fg="white", font=("Times New Roman", 60, "bold"), width=10)
        self.password_entry.place(relx=0.95, rely=3/7, anchor="e")
        self.email_entry = tk.Entry(self.root, bg="black", fg="white", font=("Times New Roman", 60, "bold"), width=10)
        self.email_entry.place(relx=0.95, rely=4/7, anchor="e")
        self.tag_entry = tk.OptionMenu(self.root, self.tag_var,"No Category","Social Media","Banking","Shopping","Streaming","Productivity","Gaming","Travel","Telecomm","Utilities","Subscriptions","Professional")
        self.tag_entry.place(relx=0.95, rely=5/7, anchor="e")
        self.info_entry = tk.Entry(self.root, bg="black", fg="white", font=("Times New Roman", 60, "bold"), width=10)
        self.info_entry.place(relx=0.95, rely=6/7, anchor="e")

        self.edit_large = tk.Button(self.root, image=self.edit_large_icon, bd=0, bg=self.bg_color)
        self.edit_large.configure(command=lambda s=service, se=self.service_entry, ue=self.username_entry, pe=self.password_entry, ee=self.email_entry, tv=self.tag_var, ie=self.info_entry: self.edit_task(s, se, ue, pe, ee, tv, ie))
        self.edit_large.place(relx=0.125, rely=0.5, anchor="s")
        self.edit_label = tk.Label(self.root, text="Edit Service", justify="center", font=("Times New Roman", 35, "bold"), bg="white", fg="black")
        self.edit_label.place(relx=0.125, rely=0.5, anchor="n")
    
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
        self.tag_var.set("")
        self.back_button.destroy()
        self.screenshot_label.destroy()
        self.edit_large.destroy()
        self.edit_label.destroy()
        self.old_service.destroy()
        self.old_username.destroy()
        self.old_password.destroy()
        self.old_email.destroy()
        self.old_tag.destroy()
        self.old_info.destroy()
        self.service_entry.destroy()
        self.username_entry.destroy()
        self.password_entry.destroy()
        self.email_entry.destroy()
        self.tag_entry.destroy()
        self.info_entry.destroy()

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
    
    def toggle_peek(self, service:str) -> None:
        found_state = self.cred_state[service]

        if found_state[1] % 2 == 0:
            found_labels = self.cred_labels[service]
            found_labels[0].place_forget()
            found_labels[1].place_forget()
            found_labels[2].place_forget()

            found_labels[2].configure(text=credutil.find_cred(service).password)
            found_labels[2].place(anchor="ne", relx=0.975-(4.55*0.0925), rely=found_state[0])
            found_labels[1].configure(text=credutil.find_cred(service).username[:3] + "...")
            found_labels[1].place(anchor="nw", relx=0, rely=found_state[0])
        else:
            found_labels = self.cred_labels[service]
            found_labels[1].place_forget()
            found_labels[2].place_forget()

            found_labels[0].place(anchor="nw", relx=0, rely=found_state[2])
            found_labels[1].configure(text=credutil.find_cred(service).username[:13])
            found_labels[1].place(anchor="ne", relx=0.45, rely=found_state[0])
            found_labels[2].configure(text="*****")
            found_labels[2].place(anchor="ne", relx=0.975-(4.55*0.0925), rely=found_state[0])
        
        found_state[1] += 1

    def info_interface(self, service:str) -> None:
        found_service = credutil.find_cred(service)

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
        self.back_button.configure(command=self.back_from_info)
        self.back_button.place(relx=-0.005, rely=-0.055, anchor="nw")

        self.info_large = tk.Label(self.root, image=self.info_large_icon, bd=0, bg=self.bg_color)
        self.info_large.place(relx=0.125, rely=0.5, anchor="s")
        self.info_icon_label = tk.Label(self.root, text="Info", bg="black", fg="white", font=("Times New Roman", 35, "bold"))
        self.info_icon_label.place(relx=0.125, rely=0.5, anchor="n")
        self.service_label = tk.Label(self.root, text=f"Service: {service}", bg="black", fg="white", font=("Times New Roman", 60, "bold"))
        self.service_label.place(relx=0.5, rely=1/7, anchor="center")
        self.username_label = tk.Label(self.root, text=f"Username: {found_service.username}", bg="black", fg="white", font=("Times New Roman", 60, "bold"))
        self.username_label.place(relx=0.5, rely=2/7, anchor="center")
        self.password_label = tk.Label(self.root, text=f"Password: {found_service.password}", bg="black", fg="white", font=("Times New Roman", 60, "bold"))
        self.password_label.place(relx=0.5, rely=3/7, anchor="center")
        self.email_label = tk.Label(self.root, text=f"Email: {found_service.email}", bg="black", fg="white", font=("Times New Roman", 60, "bold"))
        self.email_label.place(relx=0.5, rely=4/7, anchor="center")
        self.tag_label = tk.Label(self.root, text=f"Tag: {found_service.tag}", bg="black", fg="white", font=("Times New Roman", 60, "bold"))
        self.tag_label.place(relx=0.5, rely=5/7, anchor="center")
        self.info_label = tk.Label(self.root, text=f"Info: {found_service.other_info}", bg="black", fg="white", font=("Times New Roman", 60, "bold"))
        self.info_label.place(relx=0.5, rely=6/7, anchor="center")

    def back_from_info(self):
        self.screenshot_label.destroy()
        self.back_button.destroy()
        self.info_large.destroy()
        self.info_icon_label.destroy()
        self.service_label.destroy()
        self.username_label.destroy()
        self.password_label.destroy()
        self.email_label.destroy()
        self.tag_label.destroy()
        self.info_label.destroy()

        self.del_row_elements()
        self.place_forget()
        for idx, cred in enumerate(globalvariables.user_creds):
            if idx < self.list_index:
                continue
            if idx > self.list_index + 6:
                break
            self.insert(idx-self.list_index, cred)
        self.pack()