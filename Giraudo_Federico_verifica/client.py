import socket as sck
import threading
import datetime as dt

class Receiver(threading.Thread):
    def __init__(self,sock):
        threading.Thread.__init__(self)
        self.sock = sock
        self.running = True
    def run(self):
        while self.running:
            msg =  self.sock.recv(4096).decode()
       

def main():
    s = sck.socket(sck.AF_INET, sck.SOCK_STREAM)
    s.connect(("localhost", 5000))
    rec = Receiver(s)
    rec.start()
    while True:
        stringa = input("Insert string: ")    
        s.sendall(stringa.encode())
    
    rec.join()
    
if __name__ == "__main__":
    main()