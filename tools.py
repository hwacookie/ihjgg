import re
from cryptography.fernet import Fernet
from keys import Keys



def encrypt(message:str):
    fernet = Fernet(Keys.FERNET_KEY)
    return fernet.encrypt(message.encode())

def decrypt(message:str):
    fernet = Fernet(Keys.FERNET_KEY)
    return fernet.decrypt(message).decode()

regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,10}\b'

def checkEmailFormat(email):
    return re.fullmatch(regex, email)



if __name__ =='__main__':
    nachricht = 'test'
    nachricht = encrypt(nachricht)
    print(nachricht)
    print("-")
    print(decrypt(nachricht))