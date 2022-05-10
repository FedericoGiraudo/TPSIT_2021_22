import socket as sck
import threading as thr
import sqlite3 as sq
import os.path

database = {}
clients = []

class ClientManager(thr.Thread):
    def __init__(self, connection, address, nome):
        thr.Thread.__init__(self)
        self.nome = nome
        self.connection = connection
        self.address = address
        self.running = True
    #OVERRIDE
    def run(self):
        while self.running:
            receive = self.connection.recv(4096).decode()
           
            

def main():
    

    s = sck.socket(sck.AF_INET, sck.SOCK_STREAM)
    s.bind(("localhost", 5000))
    s.listen()
    
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, "fiumi.db")
    
    

    con = sq.connect(db_path)
    cur = con.cursor()
    query = f"SELECT * FROM livelli;"
    cur.execute(query)
    rows = cur.fetchall()
    for row in rows: 
        print(row[3])
        
    con.close()
    
    while True:
        conn, address = s.accept()
        receive =conn.recv(4096).decode()
        h = receive.split(",")
        msg=f"avvenuta ricezione +{row[1]} + {row[2]} + {h[1]} "
        if int(h[0]) > (row[3]*30)/100 or int(h[0])<(row[3]*70)/100:
            print("pericolo imminente")
            conn.send(msg)
        if int(h[0])>(row[3]*70)/100:
            print("pericolo in corso")
            conn.send(msg)
            
            
            
            

        

    
            

        
if __name__ == "__main__":
    main()