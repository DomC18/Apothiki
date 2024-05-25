from tkinter import messagebox
import random as rr
import constants

class Credential:
    tag_keycodes = {
        "No Category": ["NC", (169, 169, 169), "black", 0],        # Gray
        "Social Media": ["SM", (59, 89, 152), "white", 1],         # Facebook Blue
        "Banking": ["BK", (0, 102, 204), "white", 2],              # Bank Blue
        "Shopping": ["SH", (255, 153, 0), "darkblue", 3],          # Orange
        "Streaming": ["ST", (229, 9, 20), "white", 4],             # Netflix Red
        "Productivity": ["PV", (0, 128, 0), "lightgreen", 5],      # Green
        "Gaming": ["GA", (76, 187, 23), "black", 6],               # Xbox Green
        "Travel": ["TL", (255, 140, 0), "darkred", 7],             # Dark Orange
        "Telecomm": ["TC", (0, 174, 239), "navy", 8],              # Light Blue
        "Utilities": ["U", (112, 128, 144), "lightyellow", 9],     # Slate Gray
        "Subscriptions": ["SU", (138, 43, 226), "lavender", 10],   # Blue Violet
        "Professional": ["PR", (70, 130, 180), "white", 11]        # Steel Blue
    }

    def __init__(self, service:str="service", username:str="username", password:str="password", email:str="email", tag:str="No Category", other_info:str="info") -> None:
        self.service = service
        self.username = username
        self.password = password
        self.email = email
        self.tag = tag
        self.other_info = other_info
    
    def edit_service(self, new_service:str) -> None:
        self.service = new_service

    def edit_username(self, new_username:str) -> None:
        self.username = new_username
    
    def edit_password(self, new_password:str) -> None:
        self.password = new_password

    def edit_email(self, new_email:str) -> None:
        self.email = new_email

    def edit_tag(self, new_tag:str) -> None:
        self.tag = new_tag

    def edit_other_info(self, new_info:str) -> None:
        self.other_info = new_info

    def get_tag_short(self) -> str:
        return self.tag_keycodes[self.tag][0]
    
    def get_tag_color(self) -> tuple:
        return self.tag_keycodes[self.tag][1]
    
    def get_tag_font_color(self) -> str:
        return self.tag_keycodes[self.tag][2]
    
    def get_tag_priority(self) -> int:
        return self.tag_keycodes[self.tag][3]

    def generate_random_cred(self, entry, length, include_letters:bool=False, include_digits:bool=False, include_punc:bool=False) -> None:
        if not include_letters and not include_digits and not include_punc:
            raise ValueError("Must include at least one type of character")
        
        if entry.get() != "":
            messagebox.showerror("Error", "Clear entry before generating")
            return
        
        cred = ""
        if include_letters and include_digits and include_punc:
            for _ in range(length):
                cred += rr.choice(constants.CRED_CHARS)
            entry.delete(0, "end")
            entry.insert(0, cred)
            return
    
        if include_letters and include_digits:
            for _ in range(length):
                cred += rr.choice(constants.LET_CHARS + constants.DIGIT_CHARS)
            entry.delete(0, "end")
            entry.insert(0, cred)
            return
        
        if include_letters:
            for _ in range(length):
                cred += rr.choice(constants.LET_CHARS)
            entry.delete(0, "end")
            entry.insert(0, cred)
            return
        
        if include_digits:
            for _ in range(length):
                cred += rr.choice(constants.DIGIT_CHARS)
            entry.delete(0, "end")
            entry.insert(0, cred)
            return

    def __repr__(self) -> str:
        return f"\nService: {self.service}\nUsername: {self.username}\nPassword: {self.password}\nEmail: {self.email}\nInfo: {self.other_info}\n"

    def __str__(self) -> str:
        return f"\nService: {self.service}\nUsername: {self.username}\nPassword: {self.password}\nEmail: {self.email}\nInfo: {self.other_info}\n"
    
    def __eq__(self, other) -> bool:
        return self.service == other.service and self.username == other.username and self.password == other.password and self.email == other.email and self.other_info == other.other_info
    
    def __ne__(self, other) -> bool:
        return self.service != other.service or self.username != other.username or self.password != other.password or self.email != other.email or self.other_info != other.other_info
    
    def cred_as_dict(self) -> dict:
        return {
            "service": rf"{self.service}",
            "username": rf"{self.username}",
            "password": rf"{self.password}",
            "email": rf"{self.email}",
            "tag": rf"{self.tag}",
            "info": rf"{self.other_info}"
        }