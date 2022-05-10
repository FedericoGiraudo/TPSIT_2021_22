from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import socket as sck
tipologia={'FTP':[20,21], 'SSH':[22], 'Telnet':[23], 'SMTP':[25], 'DNS':[53],
       'DHCP':[67,68], 'TFTP':[69], 'HTTP':[80], 'HTTPS':[443]}
app = Flask(__name__)

def scan(ip,porta_max,porta_min):
    risultati=[]

    s = sck.socket(sck.AF_INET, sck.SOCK_STREAM)
    for i in range(int(porta_min),int(porta_max)+1):
        if s.connect_ex((ip,i)) == 0:
            risultati.append(i)
            s.close
          
    con = sqlite3.connect('C:\A1_DATA\ITIS_2021_22\Tpsit\Python\esercitazione_veri\porte.db')
    cur = con.cursor()
    for port in risultati:
        cur.execute(f"INSERT INTO porte_ap(ip,porte) VALUES ('{ip}','{port}')")
        con.commit()
    con.close
    
            
 
@app.route("/", methods=['GET', 'POST'])
def index():
    error = None
    if request.method == 'POST':
        ip = request.form['ip']
        porta_min = request.form['min']
        porta_max = request.form['max']
        pl = request.form['pl']
        print(pl,"ciaoooooo")
        scan(ip,porta_max,porta_min)
        return render_template('index.html', error="scansione terminata")
    return render_template('index.html')
        

if __name__ == '__main__':   
    app.run(debug=True, host="0.0.0.0")