from mfrc522 import SimpleMFRC522
from utils.file import*
from db.db_function import*
from datetime import date, datetime, timedelta
from gpiozero import Buzzer
import RPi.GPIO as GPIO
import time

print("reader run")
GPIO.setwarnings(False)
buzzer = Buzzer(24)
reader = SimpleMFRC522()

oldId = ""

def beepOnce():
    buzzer.on()
    time.sleep(0.5)
    buzzer.off()

def beepTwice(lastTime):
    buzzer.on()
    time.sleep(lastTime)
    buzzer.off()
    time.sleep(lastTime)
    buzzer.on()
    time.sleep(lastTime)
    buzzer.off()

try:
    while True:
        newId, text = reader.read()
        print("OK I got it")
        if(oldId != newId and newId != None):
            oldId = newId
            writeFile(newId)
            todayDate = datetime.now().replace(microsecond=0)

            try:
                memebrsipByChip = getMembershipsByChipId(int(newId))
                lastSaveDate = datetime.strptime(memebrsipByChip[0][1], '%Y-%m-%d')
                endDate = lastSaveDate + timedelta(days = int(memebrsipByChip[0][2]))
                group = getGroupById(memebrsipByChip[0][8])
                current_hour = datetime.now().hour
                start_hour = datetime.strptime(group[0][2], '%H:%M').hour
                end_hour = datetime.strptime(group[0][3], '%H:%M').hour
               
                if todayDate <= endDate:
                    if(start_hour < current_hour and current_hour < end_hour):
                        newReport = (todayDate, memebrsipByChip[0][3])
                        insertReport(newReport)
                        beepOnce()
                    else:
                        beepTwice(0.5)
                        print("van grupe")
                else:
                    beepTwice(1)
                    print("nema clanarinu")
            except IndexError:
                beepTwice(1)
                print("not found")

            print(memebrsipByChip)
            print("Card id:", newId)         
finally:
    GPIO.cleanup()