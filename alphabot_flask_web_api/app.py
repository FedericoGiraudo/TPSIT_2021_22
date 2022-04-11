from flask import Flask, render_template, request, redirect, url_for, make_response,jsonify
import time
import RPi.GPIO as GPIO

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
        left=int(left)
        right=int(right)
        right=-right
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
 
@app.route('/api/v1/motors/left', methods=['GET'])
def api_left():
    try:
        left = request.args['pwm']
        t = request.args['time']
        al.set_motor(0,left)
        time.sleep(float(t))
        al.stop()
        return '1'
    except:
        return '0'
        
   
@app.route('/api/v1/motors/right', methods=['GET'])
def api_right():
    try:
        right = request.args['pwm']
        t = request.args['time']
        al.set_motor(right,0)
        time.sleep(float(t))
        al.stop()
        return '1'
    except:
        return '0'

@app.route('/api/v1/motors/both', methods=['GET'])
def api_both():
    try:
        right = request.args['pwmR']
        left = request.args['pwmL']
        t = request.args['time']
        al.set_motor(right,left)
        time.sleep(float(t))
        al.stop()
        return '1'
    except:
        return '0'

@app.route('/api/v1/sensors/obstacles', methods=['GET'])
def api_id():
    DR = 16
    DL = 19

    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(DR,GPIO.IN,GPIO.PUD_UP)
    GPIO.setup(DL,GPIO.IN,GPIO.PUD_UP)

    try:
        DR_status = GPIO.input(DR)
        DL_status = GPIO.input(DL)
        diz={'destra':DR_status,
             'sinistra':DL_status}
        return jsonify(diz)

    except KeyboardInterrupt:
        GPIO.cleanup();

#if __name__ == '__main__':   
#    app.run(debug=True, host="0.0.0.0")
app.run(debug=True, host="0.0.0.0")