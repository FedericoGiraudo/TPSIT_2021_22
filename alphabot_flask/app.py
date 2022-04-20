from crypt import methods
from flask import Flask, render_template, request, redirect, url_for, make_response
import time
import RPi.GPIO as GPIO
import sqlite3
import string
import random

app = Flask(__name__)

class AlphaBot(object):          #creo una classe Alphabot   
    def __init__(self, in1=13, in2=12, ena=6, in3=21, in4=20, enb=26):
        self.IN1 = in1
        self.IN2 = in2
        self.IN3 = in3
        self.IN4 = in4
        self.ENA = ena
        self.ENB = enb
        self.PA  = 25
        self.PB  = 25

        
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.IN1, GPIO.OUT)
        GPIO.setup(self.IN2, GPIO.OUT)
        GPIO.setup(self.IN3, GPIO.OUT)
        GPIO.setup(self.IN4, GPIO.OUT)
        GPIO.setup(self.ENA, GPIO.OUT)
        GPIO.setup(self.ENB, GPIO.OUT)
        self.PWMA = GPIO.PWM(self.ENA,500)
        self.PWMB = GPIO.PWM(self.ENB,500)
        self.PWMA.start(self.PA)
        self.PWMB.start(self.PB)
        self.stop()
        
    def stop(self):
            self.PWMA.ChangeDutyCycle(0)
            self.PWMB.ChangeDutyCycle(0)
            GPIO.output(self.IN1, GPIO.LOW)
            GPIO.output(self.IN2, GPIO.LOW)     #funzione per permettere al robot di fermarsi 
            GPIO.output(self.IN3, GPIO.LOW)
            GPIO.output(self.IN4, GPIO.LOW)
            
    def left(self, t):
        self.PWMA.ChangeDutyCycle(self.PA)
        self.PWMB.ChangeDutyCycle(self.PB)
        GPIO.output(self.IN1, GPIO.HIGH)
        GPIO.output(self.IN2, GPIO.LOW)          #funzione per permettere al robot di girare a sinistra per un certo tempo t
        GPIO.output(self.IN3, GPIO.HIGH)
        GPIO.output(self.IN4, GPIO.LOW)
        time.sleep(t)
        al.stop()
        

    def right(self,t):
        self.PWMA.ChangeDutyCycle(self.PA)
        self.PWMB.ChangeDutyCycle(self.PB)
        GPIO.output(self.IN1, GPIO.LOW)
        GPIO.output(self.IN2, GPIO.HIGH)        #funzione per permettere al robot di girare a destra per un certo tempo t
        GPIO.output(self.IN3, GPIO.LOW)
        GPIO.output(self.IN4, GPIO.HIGH)
        time.sleep(t)
        al.stop()

    def forward(self,t, speed =30):
        self.PWMA.ChangeDutyCycle(speed)
        self.PWMB.ChangeDutyCycle(speed)
        GPIO.output(self.IN1, GPIO.LOW)         #funzione per permettere al robot di andare avanti per un certo tempo t
        GPIO.output(self.IN2, GPIO.HIGH)
        GPIO.output(self.IN3, GPIO.HIGH)
        GPIO.output(self.IN4, GPIO.LOW)
        time.sleep(t)
        al.stop()
            
        

    def backward(self,t, speed =30):
        self.PWMA.ChangeDutyCycle(speed)
        self.PWMB.ChangeDutyCycle(speed)
        GPIO.output(self.IN1, GPIO.HIGH)
        GPIO.output(self.IN2, GPIO.LOW)         #funzione per permettere al robot di andare indietro per un certo tempo t 
        GPIO.output(self.IN3, GPIO.LOW)
        GPIO.output(self.IN4, GPIO.HIGH)
        time.sleep(t)
        al.stop()
        
    def set_pwm_a(self, value):
        self.PA = value
        self.PWMA.ChangeDutyCycle(self.PA)

    def set_pwm_b(self, value):
        self.PB = value
        self.PWMB.ChangeDutyCycle(self.PB)    
        
    def set_motor(self, left, right):
        if (right >= 0) and (right <= 100):
            GPIO.output(self.IN1, GPIO.HIGH)
            GPIO.output(self.IN2, GPIO.LOW)
            self.PWMA.ChangeDutyCycle(right)
        elif (right < 0) and (right >= -100):
            GPIO.output(self.IN1, GPIO.LOW)
            GPIO.output(self.IN2, GPIO.HIGH)
            self.PWMA.ChangeDutyCycle(0 - right)
        if (left >= 0) and (left <= 100):
            GPIO.output(self.IN3, GPIO.HIGH)
            GPIO.output(self.IN4, GPIO.LOW)
            self.PWMB.ChangeDutyCycle(left)
        elif (left < 0) and (left >= -100):
            GPIO.output(self.IN3, GPIO.LOW)
            GPIO.output(self.IN4, GPIO.HIGH)
            self.PWMB.ChangeDutyCycle(0 - left)

al=AlphaBot()

length=20
token = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))

@app.route("/", methods=['GET', 'POST'])
def login():
    error = None
    
    if request.method == 'POST':
        username_c = request.cookies.get('username')
        username = request.form['username']
        password = request.form['password']
        print(username,  password)
        completion = validate(username, password)
        if completion ==False:
            error = 'Invalid Credentials. Please try again.'
        else:  
            print("entratooooooo")
            if username_c==None:
                resp = make_response(render_template('index.html'))
                resp.set_cookie('username', username)
                return resp  
            return redirect(url_for('index')) 
    return render_template('login.html', error=error)

def validate(username, password):
    completion = False
    con = sqlite3.connect('./comandi.db')
    cur = con.cursor()
    cur.execute("SELECT * FROM Users")
    rows = cur.fetchall()
    for row in rows:
        dbUser = row[0]
        dbPass = row[1]
        if dbUser==username:
            completion=check_password(dbPass, password)
    return completion

def check_password(hashed_password, user_password):
    return hashed_password == user_password

@app.route(f"/{token}", methods=['GET', 'POST'])
def index():
    username_c = request.cookies.get('username') 
    modifica = time.ctime()
    print(modifica)
    con = sqlite3.connect('./comandi.db')
    cur = con.cursor()

    if request.method == 'POST':
        if request.form.get('avanti') == 'avanti':
            al.forward(5)
            comando='avanti'
            print("vai avanti")
        elif request.form.get('stop') == 'stop':
            al.stop()
            comando='stop'
            print("fermati")
        elif  request.form.get('indietro') == 'indietro':
            al.backward(5)
            comando='indietro'
            print("vai indietro")          
        elif  request.form.get('destra') == 'destra':
            al.right(5)
            comando='destra'
            print("vai a destra")        
        elif  request.form.get('sinistra') == 'sinistra':
            al.left(5)
            comando='sinistra'
            print("vai a sinistra")
        elif request.form.get('invio') == 'invio':
            nome=request.form.get('nome')
            print(nome)     
        else:
            print("Unknown")
    elif request.method == 'GET':
        return render_template('index.html')
    print(f"INSERT INTO Modifiche(Username,modifica,comando) VALUES ('{username_c}','{modifica}', '{comando}')")
    cur.execute(f"INSERT INTO Modifiche(Username,modifica,comando) VALUES ('{username_c}','{modifica}', '{comando}')")
    con.commit()
    return render_template('index.html')

    


if __name__ == '__main__':   
    app.run(debug=True, host="0.0.0.0")