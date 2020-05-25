#!/usr/bin/python
import smtplib,ssl  
from picamera import PiCamera  
from time import sleep  
from email.mime.multipart import MIMEMultipart  
from email.mime.base import MIMEBase  
from email.mime.text import MIMEText  
from email.utils import formatdate  
from email import encoders  
import RPi.GPIO as gpio
import time
import Adafruit_ADXL345
#Pin
pir = 16
buz = 18
sw = 22

pir_flag=200
accel = Adafruit_ADXL345.ADXL345()
cal_x = 1
cal_y = 2
cal_z = 3
toaddr = 'shubhamkr.1307@gmail.com'         # To id 
me = 'projectimage40@gmail.com'     # your id
thres = 60


def initialize_adxl345():
    global cal_x, cal_y
    cal_x, cal_y, cal_z = accel.read()
    
def check_adxl345():
    x, y, z = accel.read()
    print('X={0}, Y={1}, Cal_X={2}, Cal_Y={3} '.format(x, y, cal_x, cal_y))
    if(x>cal_x+thres or x<cal_x-thres or y>cal_y+thres or y<cal_y-thres):
        gpio.output(buz, 1)
        print("Tow Alert")
        send_an_email1()
        gpio.output(buz, 0)
    
    
   
def capture_image():  
    camera = PiCamera()  
    camera.start_preview()  
    sleep(1)  
    camera.capture('/home/pi/image.jpg')     # image path set
    sleep(1)  
    camera.stop_preview()  
    sleep(1)  
    camera.close()

def send_an_email1():  
    
    
    subject = "Hey! Tow Alert"       # Subject
    msg = MIMEMultipart()  
    msg['Subject'] = subject  
    msg['From'] = me  
    msg['To'] = toaddr  
    msg.preamble = "test "
    #msg.set_content('Your car is being towed')
    #msg.attach(MIMEText(text))  
  
    #part = MIMEBase('application', "octet-stream")  
    #part.set_payload(open("/home/pi/image.jpg", "rb").read())  
    #encoders.encode_base64(part)  
    #part.add_header('Content-Disposition', 'attachment; filename="image.jpg"')   # File name and format name
    #msg.attach(part)  
  
    try:  
       s = smtplib.SMTP('smtp.gmail.com', 587)  # Protocol
       s.ehlo()  
       s.starttls()  
       s.ehlo()  
       s.login(user = 'projectimage40@gmail.com', password = 'Testing@123')  # User id & password
       #s.send_message(msg)  
       s.sendmail(me, toaddr, msg.as_string())  
       s.quit()  
    #except:  
    #   print ("Error: unable to send email")    
    except SMTPException as error:  
          print ("Error")                # Exception

def send_an_email2():  
    subject = "Hey! Alert Motion Detected"       # Subject
  
    msg = MIMEMultipart()  
    msg['Subject'] = subject  
    msg['From'] = me  
    msg['To'] = toaddr  
    msg.preamble = "test "   
    #msg.attach(MIMEText(text))  
  
    part = MIMEBase('application', "octet-stream")  
    part.set_payload(open("/home/pi/image.jpg", "rb").read())  
    encoders.encode_base64(part)  
    part.add_header('Content-Disposition', 'attachment; filename="image.jpg"')   # File name and format name
    msg.attach(part)  
  
    try:  
       s = smtplib.SMTP('smtp.gmail.com', 587)  # Protocol
       s.ehlo()  
       s.starttls()  
       s.ehlo()  
       s.login(user = 'projectimage40@gmail.com', password = 'Testing@123')  # User id & password
       #s.send_message(msg)  
       s.sendmail(me, toaddr, msg.as_string())  
       s.quit()  
    #except:  
    #   print ("Error: unable to send email")    
    except SMTPException as error:  
          print ("Error")                # Exception


gpio.setmode(gpio.BOARD) # Set pin numbering to board numbering
gpio.setwarnings(False)
gpio.setup(buz, gpio.OUT)
gpio.output(buz, 1)
sleep(0.25)
gpio.output(buz, 0)
sleep(0.25)
gpio.output(buz, 1)
sleep(0.25)
gpio.output(buz, 0)
gpio.setup(pir, gpio.IN)
gpio.setup(sw, gpio.IN)
sleep(1)
initialize_adxl345()
while True:
    if(gpio.input(sw) == False):
        print("Armed")
        if (pir_flag==200):
            if (gpio.input(pir) == True):
                gpio.output(buz, 1)
                print("Motion Detected")
                capture_image()
                send_an_email2()
                sleep(1)
                gpio.output(buz, 0)
                pir_flag=0
        if (pir_flag<200):
            pir_flag=pir_flag+1
            print(pir_flag)
        check_adxl345()
        sleep(0.2)
    else:
        print("Disarmed")
        sleep(0.2)
