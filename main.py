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
    
    step1 = distance - 10
    step2 = 5 * step1
    result = 100 -step2
    
    #assume the height of the bottle is 20cm
    if (distance < 11) and (distance > 9): #full
        print('full', distance)
        lcd.clear()
        print("Bottle Full " + str(int(result)) +"%")
        lcd.putstr("Bottle Full " + str(int(result)) +"%")
        ledgren.value(1)
        #sleep(1)
        ledred.value(0)
        
    elif (distance > 20) and (distance < 30): #half
        print('half', distance)
        lcd.clear()
        print("Bottle refilling " + str(int(result)) +"%")
        lcd.putstr("Bottle refilling " + str(int(result)) +"%")
        ledred.value(1)
        #sleep(1)
        ledgren.value(0)
    sleep(0.2)
