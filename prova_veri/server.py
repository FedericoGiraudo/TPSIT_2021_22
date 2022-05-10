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

            for op in database[self.nome]:
                self.connection.sendall(op.encode())
                receive = self.connection.recv(4096).decode()

                # print (f"{operazione} = {risultato} from {client_ip} - {client_port}")
                print(f"{op} = {receive} from {self.address[0]} - {self.address[1]}")

            self.connection.sendall("exit".encode())
            self.running = False
            self.connection.close()
            

def main():
    global database

    s = sck.socket(sck.AF_INET, sck.SOCK_STREAM)
    s.bind(("localhost", 5000))
    s.listen()
    
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, "operations.db")


    con = sq.connect(db_path)
    cur = con.cursor()
    query = f"SELECT * FROM operations;"
    cur.execute(query)
    rows = cur.fetchall()
    for row in rows: 
        if row[1] in database:
            database[row[1]].append(row[2])
        else:
            database[row[1]] = [row[2]]

    con.close()

    while True:
        connection, address = s.accept()
        client = ClientManager(connection, address, len(clients)+1)
        clients.append(client)
        client.start()
        
if __name__ == "__main__":
    main()