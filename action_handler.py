# Required for Hardware Camera
from picamera import PiCamera

# Required for LED Display
import lcddriver
display = lcddriver.lcd()

# Other requirements
from time import sleep
import threading
import time
import datetime
from datetime import date

# For GPIO Pins
import RPi.GPIO as GPIO

# Globals
status = "Operational"
gpio_pin = 16

###################################
# <------- CAMERA METHODS -------->
###################################

# Initialize Camera
def get_video_feed():
  camera = PiCamera()
  camera.start_preview()
  camera.capture('static/image.jpg')
  camera.close()
  
###################################
# <-------  MOTOR CONTROL -------->
###################################


# Motor Initialization
def motor_setup():
  GPIO.setwarnings(False)
  GPIO.setmode(GPIO.BCM)
  GPIO.setup(gpio_pin, GPIO.OUT)
  GPIO.output(gpio_pin, 1)

def scheduled_thread(date):
  while True:
    time.sleep(15)
    if date == datetime.datetime.now().strftime('%I:%M %p'):
      enable_motor(6)
      break
    else:
      print(datetime.datetime.now().strftime('%I:%M %p'))
      print(date)


def scheduled(date):
  try:
    t2 = threading.Thread(target=scheduled_thread, args=[date])
    t2.start()
  except Exception as e:
    print(e)


def enable_motor_thread(seconds):
  set_message("Manual Feed", "In Progress")
  GPIO.output(gpio_pin, 0)
  time.sleep(seconds)
  GPIO.output(gpio_pin, 1)
  clear_screen()
  set_message("Manual Feed", "Complete")
  time.sleep(3)
  set_time()


def enable_motor(seconds):
  try:
    t1 = threading.Thread(target=enable_motor_thread, args=[seconds])
    t1.start()
  except Exception as e:
    print(e, "set_message")

def disable_motor():
  GPIO.output(gpio_pin, 1)

###################################
# <------- LED METHODS --------->
###################################

def clear_screen():
  display.lcd_clear()
  

def countdown_clock_thread():
  try:
      display.lcd_display_string("Time Until Feeding", 1) 
      while True:
          display.lcd_display_string(str(datetime.datetime.now().time()), 2) 
  except Exception as e: 
      print(e)
  finally:
    display.lcd_clear()


def set_countdown_clock():
  try:
    thread1 = countdown_clock_thread();
    thread1.start()
  except Exception as e:
    print(e)
    

def set_time():
  try:
    clear_screen()
    set_message("Last Fed", datetime.datetime.now().strftime('%A %I:%M%p'))
  except Exception as e:
    print(e)

def set_message_thread(msg_top, msg_btm):
  try:
    clear_screen()
    display.lcd_display_string(msg_top, 1)
    display.lcd_display_string(msg_btm, 2)
  except Exception as e:
    print(e, "set_message_thread")  
    
    
def set_message(msg_top, msg_btm):
  try:
    t1 = threading.Thread(target=set_message_thread, args=(msg_top, msg_btm))
    t1.start()
  except Exception as e:
    print(e, "set_message")