from turtle import right
import requests
import time

lato=input('inserisci lato: ')

while True:
    
    pwm = 80
    t = 0.3
    indietro=f'http://192.168.0.127:5000/api/v1/motors/both?pwmL=-90&pwmR=-{pwm}&time=0.15'
    data=requests.get(f'http://192.168.0.127:5000/api/v1/sensors/obstacles')
    r=data.json()

    if r['destra']==1 and r['sinistra']==1 :
        
        requests.get(f'http://192.168.0.127:5000/api/v1/motors/both?pwmL={pwm}&pwmR={pwm}&time={t}')
        
    elif r['destra']==1 and r['sinistra']==0:
        requests.get(indietro)
        requests.get(f'http://192.168.0.127:5000/api/v1/motors/left?pwm={pwm}&time={t}')
        
    elif r['destra']==0 and r['sinistra']==1:
        requests.get(indietro)
        requests.get(f'http://192.168.0.127:5000/api/v1/motors/right?pwm={pwm}&time={t}')    
        
    elif r['destra']==0 and r['sinistra']==0:
        requests.get(indietro)
        requests.get(f'http://192.168.0.127:5000/api/v1/motors/{lato}?pwm={pwm}&time={t}')

    time.sleep(0.1)