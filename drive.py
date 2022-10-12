
# Import required libraries
import time
import RPi.GPIO as GPIO

# Use BCM GPIO references
# instead of physical pin numbers
GPIO.setmode(GPIO.BCM)
# Define GPIO signals to use
TRIG = 17
ECHO = 27

INA = 23
INB = 24
INC = 25
IND = 8

GPIO.setup(TRIG , GPIO.OUT)
GPIO.setup(ECHO , GPIO.IN)

GPIO.setup(INA , GPIO.OUT)
GPIO.setup(INB , GPIO.OUT)
GPIO.setup(INC , GPIO.OUT)
GPIO.setup(IND , GPIO.OUT)

time.sleep(5)

def stop():
    GPIO.output(INA, 0)
    GPIO.output(INB, 0)
    GPIO.output(INC, 0)
    GPIO.output(IND, 0)

def forward():
    GPIO.output(INA, 1)
    GPIO.output(INB, 0)
    GPIO.output(INC, 1)
    GPIO.output(IND, 0)
    
 def left():
    GPIO.output(INA, 1)
    GPIO.output(INB, 0)
    GPIO.output(INC, 0)
    GPIO.output(IND, 0)
    
stop()
while True:
    GPIO.output(TRIG, 0)
    time.sleep(0.1)
    GPIO.output(TRIG, 1)
    time.sleep(0.00001)
    GPIO.output(TRIG, 0)
    
    while GPIO.input(ECHO)==0:
        pulse_start =time.time()
    
    while GPIO.input(ECHO)==1:
        pulse_end =time.time()
    
    pulse_duration =pulse_end - pulse_start
    distance = pulse_duration*17150
    distance = round(distance ,2)
    print(distance)
    
    if distance < 15:
        left()
        time.sleep(1)
    else:
        forward()
        
    
