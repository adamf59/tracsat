
#This code is meant to test the control system with manually inputted laser locations
#It is not integrated with actual laser sensors
#Location 0 is off of the laser array
import time
from easygopigo3 import EasyGoPiGo3
import RPi.GPIO as GPIO
#Defining objects

gpg =EasyGoPiGo3()

servo = gpg.init_servo("SERVO2")
servo.gpg.set_servo(servo.gpg.SERVO_2,int(1490))
keepWorking = True
GPIO.setmode(GPIO.BOARD)
#setup gpio pins
#Sensor Numbers are Connected to the Numbered Pins as follows
sensor1 = 37 #need to be replaced
sensor2= 36
sensor3 = 35
sensor4 = 33
sensor5 = 31
sensorlist = [sensor1,sensor2,sensor3,sensor4,sensor5]
GPIO.setup(sensorlist,GPIO.IN)

time.sleep(20)
CLoc = 0
PLoc = 0
starting = True
while starting:
    c = GPIO.input(sensor3)
    servo.gpg.set_servo(servo.gpg.SERVO_2,int(1400))
    if (c==True):
        servo.gpg.set_servo(servo.gpg.SERVO_2,int(1490))
        starting = False
        CLoc = 3
        PLoc = 3
        
time.sleep(3)       
startTime = time.time()   

while keepWorking:
    a = GPIO.input(sensor1)
    b = GPIO.input(sensor2)
    c = GPIO.input(sensor3)
    d = GPIO.input(sensor4)
    e = GPIO.input(sensor5)
    tCurr = time.time()
    gpg.forward()
    tElapsed = tCurr - startTime
    
    if (tElapsed >=10):
        servo.gpg.set_servo(servo.gpg.SERVO_2,int(1490))
        gpg.stop()
        time.sleep(.5)
        break
    
    if (CLoc != 0):
       PLoc = CLoc
    if (a==True):
        CLoc= 1
    elif (b==True):
        CLoc = 2
    elif (c==True):
        CLoc = 3
    elif (d==True):
        CLoc = 4
    elif (e==True):
        CLoc = 5
    else:
        CLoc = 0
    
    if CLoc == 3: #if Laser is hitting center detector, don't move
        servo.gpg.set_servo(servo.gpg.SERVO_2,int(1490))
        time.sleep(2)
        print("Laser on 3, no adjustment needed!")
    elif CLoc == 1 or CLoc == 2: #if Laser is hitting left detectors
        servo.gpg.set_servo(servo.gpg.SERVO_2,int(1450))
        print("Laser on detector ",CLoc)
        
    elif CLoc == 4 or CLoc == 5: #if Laser is hitting right detectors
        servo.gpg.set_servo(servo.gpg.SERVO_2,int(1550))
        print("Laser on detector ",CLoc)
        
    elif CLoc == 0: #If laser is not hitting any detectors
        if PLoc == 1 or PLoc == 2 or PLoc == 3: #If last detector with laser communications was 1,2,3
            servo.gpg.set_servo(servo.gpg.SERVO_2,int(1450))
            print("Laser off. It last was on detector ",PLoc)
            
        elif PLoc == 5 or PLoc ==4: #If laser exited the right side of the laser array
            servo.gpg.set_servo(servo.gpg.SERVO_2,int(1550))
            print("Laser off. It last was on detector",PLoc)
            
        elif PLoc == 0: #Initial Lock Code
            servo.gpg.set_servo(servo.gpg.SERVO_2,int(1700))
            print("Initial Lock")
            print("Moving CounterClockwise")
        else:
            print("PLoc Error")
            keepWorking= False
            servo.gpg.set_servo(servo.gpg.SERVO_2,int(1490))
    elif CLoc == 7:
        servo.gpg.set_servo(servo.gpg.SERVO_2,int(1490))
        keepWorking = False
    else:
        print("CLoc Error")
        keepWorking = False
        servo.gpg.set_servo(servo.gpg.SERVO_2,int(1490))
        
print("Code Done")
