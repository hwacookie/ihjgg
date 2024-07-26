import re
 
regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
 
def checkEmailFormat(email):
    return re.fullmatch(regex, email)
