##client
import socket as sck

s = sck.socket(sck.AF_INET,sck.SOCK_DGRAM)

nickname="federico"
stringa =f"Nickname:{nickname}"
s.sendto(stringa.encode(),('192.168.88.92',5000))

while True:
    mes = input("messaggio: ")
    s.sendto(mes.encode(),('192.168.88.92',5000))
    

