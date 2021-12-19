import socket as sck
import sqlite3
dict = {}
s = sck.socket(sck.AF_INET,sck.SOCK_DGRAM)
ACK = "logged"
s.bind(('0.0.0.0', 3000)) #solo su Server

while True:
    msg, add = s.recvfrom(4096)
    tmp = msg.decode().split(":")
    if (tmp[0].lower()=="nickname"):
        con = sqlite3.connect('example1.db')
        cur = con.cursor()
        cur.execute(f"INSERT INTO users VALUES ('{tmp[0]}','{add[0]}',{add[1]})")
        con.commit()
        con.close()
        dict[tmp[1]]=add
        s.sendto(ACK.encode(),(add))
    else:

        tmp2=msg.decode().split(",")
        rec = tmp2[1].split(":")
        sen = tmp2[0].split(":")
        con = sqlite3.connect('example1.db')
        cur = con.cursor()
        for row in cur.execute(f"SELECT * FROM users"):
            if row[0] == rec[1]:
                addr = row[1]
                port = row[2]
                des = (addr,port)
        s.sendto(tmp2[2].encode(),(des))
        print(f"{sen[1]} manda '{tmp2[2]}' a {des[0]}/{des[1]}")
        con.commit()
        con.close()

    print(dict)

#f"sender:{nickname},receiver:{nickname_ricevente},{msg}"

s.close()