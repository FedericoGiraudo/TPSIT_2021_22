#server
import socket as sck

s = sck.socket(sck.AF_INET, sck.SOCK_DGRAM)

s.bind(('0.0.0.0', 5000)) #(indirizzo ip della macchina server (0.0.0.0 = il mio ip), porta
utenti={}
while True:   
    data, addr = s.recvfrom(4096) #dati ricevuti(data), addr è una tupla con indirizzo ip del client e porta del client
    if data.decode.split(':')[0]=="Nickname":
        utenti[data.decode.split(':')[1]]=addr
        print(utenti)