import socket as sck
import time                                 #importo le librerie socket, time e RPi.GPIO
import RPi.GPIO as GPIO


class AlphaBot(object):                     #creo una classe Alphabot
    
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

    def left(self):
        self.PWMA.ChangeDutyCycle(self.PA)
        self.PWMB.ChangeDutyCycle(self.PB)
        GPIO.output(self.IN1, GPIO.HIGH)            #funzione per permettere al robot di girare a sinistra
        GPIO.output(self.IN2, GPIO.LOW)
        GPIO.output(self.IN3, GPIO.HIGH)
        GPIO.output(self.IN4, GPIO.LOW)

    def stop(self):
        self.PWMA.ChangeDutyCycle(0)
        self.PWMB.ChangeDutyCycle(0)
        GPIO.output(self.IN1, GPIO.LOW)             #funzione per permettere al robot di fermarsi
        GPIO.output(self.IN2, GPIO.LOW)
        GPIO.output(self.IN3, GPIO.LOW)
        GPIO.output(self.IN4, GPIO.LOW)

    def right(self):
        self.PWMA.ChangeDutyCycle(self.PA)
        self.PWMB.ChangeDutyCycle(self.PB)
        GPIO.output(self.IN1, GPIO.LOW)             #funzione per permettere al robot di girare a destra
        GPIO.output(self.IN2, GPIO.HIGH)
        GPIO.output(self.IN3, GPIO.LOW)
        GPIO.output(self.IN4, GPIO.HIGH)

    def forward(self, speed =30):
        self.PWMA.ChangeDutyCycle(speed)
        self.PWMB.ChangeDutyCycle(speed)
        GPIO.output(self.IN1, GPIO.LOW)             #funzione per permettere al robot di andare avanti
        GPIO.output(self.IN2, GPIO.HIGH)
        GPIO.output(self.IN3, GPIO.HIGH)
        GPIO.output(self.IN4, GPIO.LOW)
    
    def forward_2(self, speed=15):
        while speed<=100:
            self.PWMA.ChangeDutyCycle(speed)
            self.PWMB.ChangeDutyCycle(speed)
            GPIO.output(self.IN1, GPIO.LOW)         #funzione che, grazie ad uno sleep, permette di far andar avanti il robot
            GPIO.output(self.IN2, GPIO.HIGH)        #con una velocità che aumenta gradualmente fino a 100
            GPIO.output(self.IN3, GPIO.HIGH)
            GPIO.output(self.IN4, GPIO.LOW)
            time.sleep(0.2)
            speed+=2
            print(speed)

    def backward(self, speed =30):
        self.PWMA.ChangeDutyCycle(speed)
        self.PWMB.ChangeDutyCycle(speed)
        GPIO.output(self.IN1, GPIO.HIGH)            #funzione per permettere al robot di andare indietro
        GPIO.output(self.IN2, GPIO.LOW)
        GPIO.output(self.IN3, GPIO.LOW)
        GPIO.output(self.IN4, GPIO.HIGH)
        
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

if __name__ == '__main__':
    s = sck.socket(sck.AF_INET, sck.SOCK_STREAM) #creo un socket TCP tipo ipv4

    s.bind(('0.0.0.0', 5000)) #(indirizzo ip della macchina server (0.0.0.0 = il mio ip), porta
    s.listen() #alloca i dati
    conn, addr = s.accept() #dati ricevuti(data), addr è una tupla con indirizzo ip del client e porta del client
    Ab = AlphaBot()         #creo un nuovo oggetto di tipo Alphabot
    while True:
        data= conn.recv(4096).decode()  #tramite la recv ricevo i messaggi in binario dal client, li decodifico e li metto in una variabile
        print(data)
        if(data=='r'):              # se data, ovvero il messaggio è uguale a r 
            Ab.right()              #verrà svolta la funzione right ovvero il robot girerà verso destra su se stesso
        if(data=='l'):              # se data, ovvero il messaggio è uguale a l
            Ab.left()               #verrà svolta la funzione left ovvero il robot girerà verso sinistra su se stesso
        if(data=='s'):              # se data, ovvero il messaggio è uguale a s
            Ab.stop()               #verrà svolta la funzione stop ovvero il robot si fermerà
        if(data=='i'):              # se data, ovvero il messaggio è uguale a i
            Ab.backward()           #verrà svolta la funzione backward ovvero il robot andrà indietro
        if(data=='a'):              # se data, ovvero il messaggio è uguale a a
            Ab.forward()            #verrà svolta la funzione forward ovvero il robot andrà in avanti
        if(data=='aa'):             # se data, ovvero il messaggio è uguale a aa
            Ab.forward_2()          #verrà svolta la funzione forward_2 ovvero il robot andrà avanti con la velocità che aumenta gradualmente
            
        
        
sck.close()             #chiudo il socket