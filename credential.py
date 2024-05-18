import random as rr
import constants

class Credential:
    def __init__(self, service_name:str=None, service_url:str=None, username:str=None, password:str=None, email:str=None, **ids:str) -> None:
        self.service_name = service_name
        self.service_url = service_url
        self.username = username
        self.password =  password
        self.email = email
        self.ids = ids
    
    def edit_service_name(self, new_service_name:str) -> None:
        self.service_name = new_service_name

    def edit_service_url(self, new_url:str) -> None:
        self.service_url = new_url

    def edit_username(self, new_username:str) -> None:
        self.username = new_username
    
    def edit_password(self, new_password:str) -> None:
        self.password = new_password

    def edit_email(self, new_email:str) -> None:
        self.email = new_email

    def edit_ids(self, id_key:str, id_value:str) -> None:
        self.ids[id_key] = id_value

    def generate_random_cred(self, include_letters:bool=False, include_digits:bool=False, include_punc:bool=False, length:int=20) -> str:
        if not include_letters and not include_digits and not include_punc:
            raise ValueError("Must include at least one type of character")
        
        cred = ""
        if include_letters and include_digits and include_punc:
            for _ in range(length):
                cred += rr.choice(constants.CRED_CHARS)
            return cred
    
        if include_letters and include_digits:
            for _ in range(length):
                cred += rr.choice(constants.LET_CHARS + constants.DIGIT_CHARS)
            return cred
        
        if include_letters:
            for _ in range(length):
                cred += rr.choice(constants.LET_CHARS)
            return cred
        
        if include_digits:
            for _ in range(length):
                cred += rr.choice(constants.DIGIT_CHARS)
            return cred

    def __repr__(self) -> str:
        return f"\nService Name: {self.service_name}\nService URL: {self.service_url}\nUsername: {self.username}\nPassword: {self.password}\nEmail: {self.email}\nIDs: {self.ids}\n"

    def __str__(self) -> str:
        return f"\nService Name: {self.service_name}\nService URL: {self.service_url}\nUsername: {self.username}\nPassword: {self.password}\nEmail: {self.email}\nIDs: {self.ids}\n"
    
    def __eq__(self, other) -> bool:
        return self.service_name == other.service_name and self.service_url == other.service_url and self.username == other.username and self.password == other.password and self.email == other.email and self.ids == other.ids
    
    def __ne__(self, other) -> bool:
        return self.service_name != other.service_name or self.service_url != other.service_url or self.username != other.username or self.password != other.password or self.email != other.email or self.ids != other.ids
    
    def cred_as_dict(self) -> dict:
        return {
            "service_name": self.service_name,
            "service_url": self.service_url,
            "username": self.username,
            "password":  self.password,
            "email": self.email,
            "ids": self.ids,
        }