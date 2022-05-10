import semaforo
import time
from flask import Flask, render_template, request, redirect, url_for, make_response
import sqlite3
from sympy import *
app = Flask(__name__)

s = semaforo.semaforo()
STATO = "ATTIVO" #"SPENTO"

#ESEMPIO di pagina di test
@app.route('/test', methods=['GET', 'POST'])
def test():
    if request.method == 'POST':
        temp_verde= request.form['temp_verde']
        temp_giallo = request.form['temp_giallo']
        temp_rosso = request.form['temp_rosso']
        sp_sem = request.form['sp_sem']
    print(sp_sem)   
    if STATO == "ATTIVO":
        #Esempio di sequenza con semaforo attivo. I tempi devono essere
        #modificabili dalla pagina di configurazione!
        s.verde(int(temp_verde))
        s.giallo(int(temp_giallo))
        s.rosso(int(temp_rosso))
    else:
        #Esempio di sequenza con semaforo spento. I tempi devono essere
        #modificabili dalla pagina di configurazione!
        for _ in range(3):
            s.giallo(1)
            s.luci_spente(1)
    return 'TEST ESEGUITO!'

@app.route("/", methods=['GET', 'POST'])
def login():
    error = None
    
    if request.method == 'POST':
        username_c = request.cookies.get('username')
        username = request.form['username']
        password = request.form['password']
        completion = validate(username, password)
        if completion ==False:
            error = 'Invalid Credentials. Please try again.'
        else:  
            if username_c==None:
                resp = make_response(render_template('index.html'))
                resp.set_cookie('username', username)
                return resp  
            return redirect(url_for('index')) 
    return render_template('login.html', error=error)

def validate(username, password):
    completion = False
    con = sqlite3.connect('C:\A1_DATA\ITIS_2021_22\Tpsit\Python\es_veri_3\semaforo.db')
    cur = con.cursor()
    cur.execute("SELECT * FROM Utenti")
    rows = cur.fetchall()
    for row in rows:
        dbUser = row[0]
        dbPass = row[1]
        if dbUser==username:
            completion=check_password(dbPass, password)
    return completion

def check_password(hashed_password, user_password):
    return hashed_password == user_password

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1')