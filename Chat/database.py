import sqlite3
import socket as sck

s = sck.socket(sck.AF_INET,sck.SOCK_DGRAM)
ACK = "logged"
s.bind(('0.0.0.0', 3000)) #solo su Server

con = sqlite3.connect(f"C:\A1_DATA\ITIS_2021_22\Tpsit\Python\date.db")
cur = con.cursor()
for riga in cur.fetchall():       # cursore fetchall() genera una sequenza di righe di risultato della query.
                                          # in sequenza, le righe una alla volta vengono assegnate'oggetto `riga`
        print(riga)   

while True:
    msg, add = s.recvfrom(4096)
    tmp = msg.decode().split(":")
    if (tmp[0].lower=="nickname"):
        dict[tmp[1]]=add
        s.sendto(ACK.encode(),(add))
    else:
        tmp2 = msg.decode().split(",")
        rec = tmp[1].split(":")
        s.sendto(tmp2[2].encode(),(dict[rec[1]]))
        print(f"mando{tmp2[2]}a{rec[1]}")
    print(dict)

print(cur.fetchall())    
con.close()
s.close()