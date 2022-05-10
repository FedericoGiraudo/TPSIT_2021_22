import socket as sck
import threading

class Receiver(threading.Thread):
    def __init__(self,sock):
        threading.Thread.__init__(self)
        self.sock = sock
        self.running = True
    def run(self):
        while self.running:
            msg =  self.sock.recv(4096).decode()
            if msg == "exit":
                self.running = False
            else:
                self.sock.sendall(f"{eval(msg)}".encode()) 

def main():
    s = sck.socket(sck.AF_INET, sck.SOCK_STREAM)
    s.connect(("localhost", 5000))
    rec = Receiver(s)
    rec.start()
    
if __name__ == "__main__":
    main()