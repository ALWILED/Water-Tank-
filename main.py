from machine import Pin, PWM, time_pulse_us
from time import sleep_us, sleep

from machine import Pin
from machine import Pin, SoftI2C
from lcd_api import LcdApi
from i2c_lcd import I2cLcd
# Ultrasonic sensor

I2C_ADDR = 0x27 # 0x3F	
totalRows = 2
totalColumns = 16
i2c = SoftI2C(scl=Pin(22), sda=Pin(21), freq=10000) #I2C for ESP32
lcd = I2cLcd(i2c, I2C_ADDR, totalRows, totalColumns)

TRIGGER_PIN = 26
ECHO_PIN = 27
SPEED = 0.0343

# LED
LEDGREN_PIN = 14
LEDRED_PIN = 25

# BUZZER/SPEAKER
SPEAKER_PIN = 12

# Initialize Pin
trigger = Pin(TRIGGER_PIN, Pin.OUT)
echo = Pin(ECHO_PIN, Pin.IN)
ledgren = Pin(LEDGREN_PIN, Pin.OUT)
ledred = Pin(LEDRED_PIN, Pin.OUT)
buzzer = Pin(SPEAKER_PIN, Pin.OUT)
buz = PWM(buzzer)

C6 = 1047
CS6 = 1109
D6 = 1175
DS6 = 1245
E6 = 1319 
F6 = 1397
FS6 = 1480
G6 = 1568
GS6 = 1661
A6 = 1760
AS6 = 1865
B6 = 1976
C7 = 2093
CS7 = 2217
D7 = 2349
DS7 = 2489
E7 = 2637
F7 = 2794
FS7 = 2960
G7 = 3136
GS7 = 3322
A7 = 3520
AS7 = 3729
B7 = 3951
C8 = 1046 + 2093 + 1000

song1 = [C6, D6, F6, D6, A6, 0, A6, 0, G6, 0, 0, C6, D6, F6, D6, G6, 0, G6, 0, F6, E6, D6, 0, 0, 0, 0, 0, 0]
song2 = [F7, 0, G7, 0, A7, 0, F7, 0, F7, 0, A7, 0, A7, 0, 0, 0, G7, 0, F7, 0, G7, 0, C8, 0, C8, 0, C8, 0, C8, 0, 0, 0, F7, 0, E7, 0, F7, 0, F7, 0, F7, 0, F7, 0, F7, 0, 0, 0, E7, 0, F7, 0, E7, 0, F7, 0, E7, 0, D7, 0, C7, 0, 0, 0, C7, 0, C7, 0, D7, 0, D7, 0, D7, 0, D7, 0, D7, 0, 0, 0, C7, 0, A6, 0, C7, 0, A6, 0, C7, 0, G7, 0, F7, 0, 0, 0, C7, 0, A7, 0, A7, 0, A7, 0, AS7, 0, C8, 0, F7, 0, F7, 0, A7, 0, G7, 0, 0, 0, 0, 0, 0, 0, 0, 0 ]
song3 = [AS6, 0, DS7, 0, 0, AS6, 0, 0, C7, 0, D7, 0, 0, G6, 0, G6, 0, C7, 0, 0, AS6, 0, 0, GS6, 0, AS6, 0, 0, DS6, 0, DS6, 0, F6, 0, 0, F6, 0, G6, 0, GS6, 0, 0, GS6, 0, AS6, 0, C7, 0, 0, D7, 0, DS7, 0, F7, 0, 0, 0,  0, 0, 0, 0]

while True :
    # Reset Trigger
    trigger.value(0)
    sleep_us(5) # stabilize and wait 5 us

    trigger.value(1)
    # send pulse for 10 us
    sleep_us(10)
    # Stop the pulse
    trigger.value(0)
    # Read pulse time for 1 value
    pulse_time = time_pulse_us(echo, 1)
    # Calculate distance
    distance = (SPEED * pulse_time) / 2
    
    #assume the height of the bottle is 20cm
    if (distance < 11) and (distance >= 10): #full
        print('full', distance)
        lcd.clear()
        step1 = distance - 10
        step2 = 5 * step1
        result = 100 -step2
        if (result > 95):
            print("Bottle Full " + str(int(result)) +"%")
            lcd.putstr("Bottle Full " + str(int(result)) +"%")
        else:
            print(str(int(result)) +"%")
            lcd.putstr("Bottle Full " + str(int(result)) +"%")
        ledgren.value(1)
        for note in song3: 
            if note == 0: # Special case for silence 
                buz.duty(0) 
            else: 
                buz.freq(note) 
                buz.duty(50) 
            sleep(0.2) 
        buz.duty(0)
        #sleep(1)
        ledred.value(0)
        
    elif (distance > 20) and (distance < 30): #half
        print('half', distance)
        lcd.clear()
        step1 = distance - 10
        step2 = 5 * step1
        result = 100 -step2
        print("Bottle refilling " + str(int(result)) +"%")
        lcd.putstr("Bottle refilling " + str(int(result)) +"%")
        ledred.value(1)
        for note in song1: 
            if note == 0: # Special case for silence 
                buz.duty(0) 
            else: 
                buz.freq(note) 
                buz.duty(50) 
            sleep(0.2) 
        buz.duty(0)
        #sleep(1)
        ledgren.value(0)
    sleep(0.2)
