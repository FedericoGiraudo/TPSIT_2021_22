import socket as sck

s = sck.socket(sck.AF_INET, sck.SOCK_STREAM) # creo un socket TCP tipo IPV4
s.connect(('192.168.0.122', 5000)) #indirizzo ip della macchina server (0.0.0.0 = il mio ip), porta
while True:
    stringa = input("scrivi un messaggio: ")  #chiedo in input il messaggio da mandare
    s.sendall(stringa.encode()) #codifico il messaggio in UTF-8 lìe lo invio al server
    
sock.close()   