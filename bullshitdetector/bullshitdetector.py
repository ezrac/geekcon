import speech_recognition as sr
import re
import pygame.camera
import pygame.image
import time
import subprocess
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import serial
import glob


WIT_AI_KEY = "INSERT_YOUR_WIT_AI_KEY"


bullshit=["me", "greatest", "important", "cyber", "monetize", "conversion", "leadership", "vision",
          "apt", "I", "strategy", "IOT", "5g", "gamification", "social"]

def bullshitcounter(text):
    wordcount = dict((x,0) for x in bullshit)
    for w in re.findall(r"\w+", text):
        if w in wordcount:
            wordcount[w] += 1
    return wordcount


def getserial():
    result=[]
    ports = glob.glob('/dev/ttyACM[0-9]*')
    for port in ports:
            try:
                s = serial.Serial(port)
                s.close()
                result.append(port)
            except (OSError, serial.SerialException):
                pass
    return result[0]


def takepicture():
    pygame.camera.init()
    cam = pygame.camera.Camera(pygame.camera.list_cameras()[0])
    cam.start()
    img = cam.get_image()
    pygame.image.save(img, "photo.bmp")
    pygame.camera.quit()
    time.sleep(2)


r = sr.Recognizer()
with sr.Microphone() as source:
    print("Say something!")
    r.adjust_for_ambient_noise(source)
    audio = r.listen(source)





try:
    takepicture()
    a = str(r.recognize_wit(audio, key=WIT_AI_KEY))
    bulls = bullshitcounter(a)
    score = sum(bulls.values())
    print("You said " + a)
    img = Image.open('photo.bmp')
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("Freemono.ttf",50)
    draw.text((0,0), "Bullshit \n Score =  " + str(score) ,(231,61,68), font=font)
    img = img.rotate(180)
    img.save('photo-out.bmp')
    ser = serial.Serial(getserial(), 9600)
    time.sleep(4)
    print "Score" + str(score)
    if score == 1 :
        ser.write('1')
    if score == 2 :
        ser.write('2')
    if score == 3 :
        ser.write('3')
    if score > 3 :
        ser.write('4')
    subprocess.call(['feh','-x','-q','-g','320x240','photo-out.bmp'])


except sr.UnknownValueError:
    print("could not understand audio")
except sr.RequestError:
    print("Could not request results")
except (OSError, serial.SerialException):
    pass
