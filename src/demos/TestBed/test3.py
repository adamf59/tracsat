import time
from easygopigo3 import EasyGoPiGo3
print("This is the third test code")
print("This code tests the  turning and  distance commands")

time.sleep(5)
gpg = EasyGoPiGo3()
gpg.drive_cm(100,True)
gpg.stop()
time.sleep(1)
gpg.turn_degrees(90)
time.sleep(1)
gpg.drive_cm(100,True)
time.sleep(1)
gpg.turn_degrees(90)
time.sleep(1)
gpg.drive_cm(100,True)
time.sleep(1)
gpg.turn_degrees(90)
time.sleep(1)
gpg.drive_cm(100,True)
time.sleep(1)
gpg.turn_degrees(90)
time.sleep(1)