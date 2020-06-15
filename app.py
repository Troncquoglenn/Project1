import time
# time.sleep(10)
from repositories.DataRepository import DataRepository
from flask import Flask, jsonify
from flask_socketio import SocketIO
from flask_cors import CORS
import json

import socket

from subprocess import call

from threading import Timer
import threading

from apa102_pi.driver import apa102


from RPi import GPIO

from datetime import datetime

import serial

ser = serial.Serial('/dev/ttyACM0', 9600)

knop = 21

LCD_RS = 26
LCD_E  = 19
LCD_D4 = 25
LCD_D5 = 24
LCD_D6 = 23
LCD_D7 = 18
 

LCD_WIDTH = 16    
LCD_CHR = True
LCD_CMD = False
 
LCD_LINE_1 = 0x80 
LCD_LINE_2 = 0xC0 
 
E_PULSE = 0.0005
E_DELAY = 0.0005
 
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM) 

clk = 16
dt = 20


GPIO.setup(clk, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(dt, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
clkLastState = GPIO.input(clk)

GPIO.setup(LCD_E, GPIO.OUT)
GPIO.setup(LCD_RS, GPIO.OUT)
GPIO.setup(LCD_D4, GPIO.OUT) 
GPIO.setup(LCD_D5, GPIO.OUT) 
GPIO.setup(LCD_D6, GPIO.OUT) 
GPIO.setup(LCD_D7, GPIO.OUT) 

temp_sensor = 4
GPIO.setup(temp_sensor, GPIO.IN)

now = datetime.now()
datum = now.strftime("%Y-%m-%d %H:%M:%S")


app = Flask(__name__)
app.config['SECRET_KEY'] = 'dit is een wachtwoord'


socketio = SocketIO(app, cors_allowed_origins="*")
CORS(app)


strip = apa102.APA102(num_led=60, order='rgb')
strip.clear_strip()

kleur = 0XFFFFFF
modus = ""
ldr = ""
motion = ""
temperatuur = ""
timer = 0.1
switch = "off"
switchknop = "off"
counter = 0
ip_address = ""


@socketio.on('connect')
def initial_connection():
    print('A new client connect')
    global kleur
    kleur = 0XFFFFFF

@socketio.on('F2B_modus')
def keuzemodus(keuze):
    global modus
    modus = keuze
    main(modus)

@socketio.on('F2B_uitschakelen')
def uitschakelen():
    # strip.clear_strip()
    
    call("sudo shutdown --poweroff", shell=True)


@socketio.on('F2B_kleur')
def keuzekleur(color):
    color = color.replace('#', '0X')
    global kleur
    kleur = int(color, 16)
    if modus == "standaardmodus":
        setled(kleur)


@app.route('/historiek/temperatuur')
def add_temperatuur():
    global temperatuur
    data = DataRepository.update_sensor(1, temperatuur)
    data = DataRepository.update_meting(datum, temperatuur, 1)
 
    data = DataRepository.read_meting(1)
    return jsonify(temperatuur=data), 200
    print("succesvol")

@app.route('/historiek/licht')
def lichtgeschiedenis():
    global ldr
    data = DataRepository.update_sensor(2, ldr)
    data = DataRepository.update_meting(datum, ldr, 2)

    data = DataRepository.read_meting(2)
    return jsonify(licht=data), 200
    print("succesvol")

@app.route('/historiek/beweging')
def motionhistoriek():
    global motion
    if motion == "beweging":
        beweging = 1
    else:
        beweging = 0
    data = DataRepository.update_sensor(3, beweging)
    data = DataRepository.update_meting(datum, beweging, 3)

    data = DataRepository.read_meting(3)
    return jsonify(beweging=data), 200
    print("succesvol")


@app.route('/switch')
def switch():
    global modus
    return jsonify(data = modus), 200

def lcd_init():
    lcd_byte(0x33,LCD_CMD) 
    lcd_byte(0x32,LCD_CMD) 
    lcd_byte(0x06,LCD_CMD) 
    lcd_byte(0x0C,LCD_CMD)
    lcd_byte(0x28,LCD_CMD)
    lcd_byte(0x01,LCD_CMD) 
    time.sleep(E_DELAY)

def lcd_byte(bits, mode):
 
  GPIO.output(LCD_RS, mode)

  GPIO.output(LCD_D4, False)
  GPIO.output(LCD_D5, False)
  GPIO.output(LCD_D6, False)
  GPIO.output(LCD_D7, False)
  if bits&0x10==0x10:
    GPIO.output(LCD_D4, True)
  if bits&0x20==0x20:
    GPIO.output(LCD_D5, True)
  if bits&0x40==0x40:
    GPIO.output(LCD_D6, True)
  if bits&0x80==0x80:
    GPIO.output(LCD_D7, True)
 
  lcd_toggle_enable()
 
  GPIO.output(LCD_D4, False)
  GPIO.output(LCD_D5, False)
  GPIO.output(LCD_D6, False)
  GPIO.output(LCD_D7, False)
  if bits&0x01==0x01:
    GPIO.output(LCD_D4, True)
  if bits&0x02==0x02:
    GPIO.output(LCD_D5, True)
  if bits&0x04==0x04:
    GPIO.output(LCD_D6, True)
  if bits&0x08==0x08:
    GPIO.output(LCD_D7, True)
 
  lcd_toggle_enable()
 
def lcd_toggle_enable():
  time.sleep(E_DELAY)
  GPIO.output(LCD_E, True)
  time.sleep(E_PULSE)
  GPIO.output(LCD_E, False)
  time.sleep(E_DELAY)
def lcd_string(message,line):
  # Send string to display
 
  message = message.ljust(LCD_WIDTH," ")
 
  lcd_byte(line, LCD_CMD)
 
  for i in range(LCD_WIDTH):
    lcd_byte(ord(message[i]),LCD_CHR)

def main(keuze):
    if keuze == "standaardmodus":
        setled(kleur)
    
    elif keuze == "automodus":
        print(keuze)
        
    elif keuze == "temperatuurmodus":
        print(keuze)
        settemperatuur()
        
        
    elif keuze == "bewegingsmodus":
        bewegingsmodus()
        
    else:
        global switchknop
        switchknop = "off"
        print("Uit")
        strip.clear_strip()

def settemperatuur():
    
    if modus == "temperatuurmodus":
        global temperatuur
        if temperatuur <= 10:
            setled(0X0400ff)
        elif temperatuur <= 20 and temperatuur > 10:
            setled(0Xff8800)
        elif temperatuur > 20 and temperatuur <27:
            setled(0xff0000)
        elif temperatuur > 27:
            setled(0xffffff)

        Timer(2, settemperatuur).start()
        print(temperatuur)

def automodus():
    global ldr
    global modus

    if modus == "automodus":
        print(ldr)
        if int(ldr)>150:
            strip.clear_strip()
        else:
            setled(0xFFFFFF)
    
    Timer(0.1, automodus).start()

def bewegingsmodus():
    global modus
    global timer
    timer = 0.1
    
    if modus == "bewegingsmodus":
        if (motion == "beweging"):
            data = DataRepository.update_sensor(3, 1)
            data = DataRepository.update_meting(datum, 1, 3)
            print(motion)
            setled(0xFFFFFF)
            timer = 300
        
        else:
            strip.clear_strip()
            

    
    Timer(timer, bewegingsmodus).start()

def setled(kleur):
    for i in range(1,30):
            strip.set_pixel_rgb(i, kleur)
            strip.show()


# SENSORS CONTINU INLEZEN

def temperatuur_ophalen():
    global temperatuur
    sensor_file_name = '/sys/bus/w1/devices/28-011610c843ee/w1_slave'
    sensor_file = open(sensor_file_name, 'r')
    temperatuur = sensor_file.readlines()
    temperatuur = temperatuur[1].rstrip('\n')
    temperatuur = int(temperatuur[temperatuur.find('t=')+2:])
    temperatuur = float(temperatuur/1000.0)
    sensor_file.close()
    Timer(0.1, temperatuur_ophalen).start()

def communicatie_arduino():
    print("Beweging + ldr continu ophalen arduino")
        
    while True:
        if(ser.in_waiting >0):
            line = ser.readline()
            line = line.decode('utf-8')
            line = line.replace('\r', '')
            line = line.replace('\n', '')
            global ldr
            ldr = line.split("-")[1]
            global motion
            motion = line.split("-")[0]
          
            

# 1temperatuur, 2ldr, 3motion
def database():
    time.sleep(2)
    global ldr
    global temperatuur
    global motion
    print(temperatuur)
    print(ldr)
    data = DataRepository.update_sensor(1, temperatuur)
    data = DataRepository.update_meting(datum, temperatuur, 1)

    data = DataRepository.update_sensor(2, ldr)
    data = DataRepository.update_meting(datum, ldr, 2)

    data = DataRepository.update_sensor(3, 0)
    data = DataRepository.update_meting(datum, 0, 3)

    Timer(300, database).start()

def call_back_knop_event(pin):
    
    if GPIO.event_detected(knop):
        global switchknop 
        global modus

        if (switchknop == "off"):
            switchknop = "on"
            modus = "standaardmodus"
            setled(kleur)

        else:
            switchknop = "off"
            modus = "off"
            strip.clear_strip()

def kleurknop():
    global counter
    global clkLastState
    global modus
    while True:
        clkState = GPIO.input(clk)
        dtState = GPIO.input(dt)
        if clkState != clkLastState:
                if modus == "standaardmodus":
                    counter +=1
                    if counter >=9:
                        counter = 1
                    if counter == 1:
                        setled(0x000000)
                    elif counter == 2:
                        setled(0xFF0000)
                    elif counter == 3:
                        setled(0x00ff00)
                    elif counter == 4:
                        setled(0x0000ff)
                    elif counter == 5:
                        setled(0xffffff)
                    elif counter == 6:
                        setled(0x00ffff)
                    elif counter == 7:
                        setled(0xff00ff)
                    elif counter == 8:
                        setled(0xffff00)
            
        clkLastState = clkState

def get_ip_address():
    global ip_address
    
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8",80))
    ip_address = s.getsockname()[0]
    s.close()
    return ip_address

proces = threading.Thread(target=communicatie_arduino)
proces.start()

temperatuur_ophalen()
automodus()
lcd_init()
database()
proces = threading.Thread(target=kleurknop)
proces.start()

get_ip_address()


lcd_string(ip_address,LCD_LINE_1)



if __name__ == "__main__":
    
    try:
        GPIO.setup(knop, GPIO.IN, GPIO.PUD_UP)
        GPIO.add_event_detect(knop, GPIO.FALLING, bouncetime=1)
        GPIO.add_event_callback(knop, call_back_knop_event)
        
        
        socketio.run(app, debug = False, host='0.0.0.0')
        
    except KeyboardInterrupt:
        strip.clear_strip()
        strip.cleanup()
        print("einde")