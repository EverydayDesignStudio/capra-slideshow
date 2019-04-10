#!/usr/bin/env python3

# Imports
#import queue                       # Queue functions for threading
import sys                          # System functions
from gpiozero import Button         # Rotary encoder, detected as button
from PIL import ImageTk, Image      # Pillow image functions
# from RPi import GPIO                # GPIO pin detection for Raspberry Pi
from time import sleep              # sleeping functions
from tkinter import Tk, Label       # Tkinter, GUI framework in use

# Setup GPIO
clk = 17
cnt = 18
button1 = 26
button2 = 19
button3 = 13
# GPIO.setmode(GPIO.BCM)
# GPIO.setup(clk, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
# GPIO.setup(cnt, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# GPIO.setup(button1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
# GPIO.setup(button2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
# GPIO.setup(button3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# Slideshow class which is the main class that runs and is listening for events
class Slideshow:
    # Setup for the batch of images
    # TODO - these will be changed when connected with database
    EXTENSION = '.jpg'
    DIRECTORY = 'hike10/'
    CAM1 = '_cam1'
    CAM2 = '_cam2'
    CAM3 = '_cam3'
    PICTURE = 2
    LIMIT = 48

    # CURRENT_RAW_PATH = DIRECTORY + '1' + EXTENSION
    # NEXT_RAW_PATH = DIRECTORY + '2' + EXTENSION

    CURRENT_RAW_PATH_TOP = DIRECTORY + '1' + CAM3 + EXTENSION
    CURRENT_RAW_PATH_MID = DIRECTORY + '1' + CAM2 + EXTENSION
    CURRENT_RAW_PATH_BOT = DIRECTORY + '1' + CAM1 + EXTENSION

    NEXT_RAW_PATH_TOP = DIRECTORY + '2' + CAM3 + EXTENSION
    NEXT_RAW_PATH_MID = DIRECTORY + '2' + CAM2 + EXTENSION
    NEXT_RAW_PATH_BOT = DIRECTORY + '2' + CAM1 + EXTENSION

    # Initialization for rotary encoder
    # clkLastState = GPIO.input(clk)
    ROTARY_COUNT = 1       # Used exclusively for testing


    def __init__(self, win):
        # Setup the window
        self.window = win
        self.window.title("Capra")
        self.window.geometry("1280x720")
        self.window.configure(background='white')

        # Bind to events in which to listen
        self.window.bind('<Left>', self.leftKey)
        self.window.bind('<Right>', self.rightKey)
        self.window.bind('<space>', self.space_key)
        self.window.bind('<z>', self.z_key)
        self.window.bind('<x>', self.x_key)
        self.window.bind('<c>', self.c_key)
        self.window.bind('<v>', self.v_key)

        # self.window.bind(GPIO.add_event_detect(clk, GPIO.BOTH, callback=self.detectedRotaryChange))
        # self.window.bind(GPIO.add_event_detect(button1, GPIO.RISING, callback=self.button1_pressed))
        # self.window.bind(GPIO.add_event_detect(button2, GPIO.RISING, callback=self.button2_pressed))
        # self.window.bind(GPIO.add_event_detect(button3, GPIO.RISING, callback=self.button3_pressed))

        # Initialization for images and associated properties
        self.alpha = 0

        # Initialize current and next Top images
        current_raw_top = Image.open(self.CURRENT_RAW_PATH_TOP, 'r')
        self.current_raw_top = current_raw_top.transpose(Image.ROTATE_270).resize((427, 720), Image.ANTIALIAS)
        next_raw_top = Image.open(self.NEXT_RAW_PATH_TOP, 'r')
        self.next_raw_top = next_raw_top.transpose(Image.ROTATE_270).resize((427, 720), Image.ANTIALIAS)

        # Initialize current and next Middle images
        current_raw_mid = Image.open(self.CURRENT_RAW_PATH_MID, 'r')
        self.current_raw_mid = current_raw_mid.transpose(Image.ROTATE_270).resize((427, 720), Image.ANTIALIAS)
        next_raw_mid = Image.open(self.NEXT_RAW_PATH_MID, 'r')
        self.next_raw_mid = next_raw_mid.transpose(Image.ROTATE_270).resize((427, 720), Image.ANTIALIAS)

        # Initialize current and next Bottom images
        current_raw_bot = Image.open(self.CURRENT_RAW_PATH_BOT, 'r')
        self.current_raw_bot = current_raw_bot.transpose(Image.ROTATE_270).resize((427, 720), Image.ANTIALIAS)
        next_raw_bot = Image.open(self.NEXT_RAW_PATH_BOT, 'r')
        self.next_raw_bot = next_raw_bot.transpose(Image.ROTATE_270).resize((427, 720), Image.ANTIALIAS)

        # Display the first 3 images to the screen
        self.display_photo_image_top = ImageTk.PhotoImage(self.current_raw_top)
        self.image_label_top = Label(master=root, image=self.display_photo_image_top)
        self.image_label_top.pack(side='right', fill='both', expand='no')

        self.display_photo_image_mid = ImageTk.PhotoImage(self.current_raw_mid)
        self.image_label_mid = Label(master=root, image=self.display_photo_image_mid)
        self.image_label_mid.pack(side='right', fill='both', expand='no')

        self.display_photo_image_bot = ImageTk.PhotoImage(self.current_raw_bot)
        self.image_label_bot = Label(master=root, image=self.display_photo_image_bot)
        self.image_label_bot.pack(side='right', fill='both', expand='no')

        # Start continual fading function, will loop for life of the class
        root.after(100, func=self.fade_image)


    # Updates the pointer to the NEXT image
    # command could be a '+' or '-' move in the database
    def update_raw_images(self, command):
        if command == '+':
            if self.PICTURE + 1 > self.LIMIT:
                self.PICTURE = 1

            self._help_build_next_raw_images(self.PICTURE + 1)
            self.PICTURE += 1

        elif command == '-':
            if self.PICTURE < 2:
                self.PICTURE = self.LIMIT

            self._help_build_next_raw_images(self.PICTURE - 1)
            self.PICTURE -= 1
        
        else:
            raise Exception('command should be either '+' or '-'')


    # Takes the current picture count and updates the next raw images
    def _help_build_next_raw_images(self, current_count):
        self.NEXT_RAW_PATH_TOP = self.DIRECTORY + str(current_count) + self.CAM3 + self.EXTENSION
        next_raw_top = Image.open(self.NEXT_RAW_PATH_TOP, 'r')
        self.next_raw_top = next_raw_top.transpose(Image.ROTATE_270).resize((427, 720), Image.ANTIALIAS)

        self.NEXT_RAW_PATH_MID = self.DIRECTORY + str(current_count) + self.CAM2 + self.EXTENSION
        next_raw_mid = Image.open(self.NEXT_RAW_PATH_MID, 'r')
        self.next_raw_mid = next_raw_mid.transpose(Image.ROTATE_270).resize((427, 720), Image.ANTIALIAS)

        self.NEXT_RAW_PATH_BOT = self.DIRECTORY + str(current_count) + self.CAM1 + self.EXTENSION
        next_raw_bot = Image.open(self.NEXT_RAW_PATH_BOT, 'r')
        self.next_raw_bot = next_raw_bot.transpose(Image.ROTATE_270).resize((427, 720), Image.ANTIALIAS)


    # Loops for the life of the program, fading between the current image and the NEXT image
    def fade_image(self):
        print('Fading the image at alpha of: ', self.alpha)
        if self.alpha < 1.0:

            # Top image
            self.current_raw_top = Image.blend(self.current_raw_top, self.next_raw_top, self.alpha)
            self.display_photo_image_top = ImageTk.PhotoImage(self.current_raw_top)
            self.image_label_top.configure(image=self.display_photo_image_top)

            # Middle image
            self.current_raw_mid = Image.blend(self.current_raw_mid, self.next_raw_mid, self.alpha)
            self.display_photo_image_mid = ImageTk.PhotoImage(self.current_raw_mid)
            self.image_label_mid.configure(image=self.display_photo_image_mid)

            # Bottom image
            self.current_raw_bot = Image.blend(self.current_raw_bot, self.next_raw_bot, self.alpha)
            self.display_photo_image_bot = ImageTk.PhotoImage(self.current_raw_bot)
            self.image_label_bot.configure(image=self.display_photo_image_bot)

            self.alpha = self.alpha + 0.01
        root.after(20, self.fade_image)


    # Detects right key press
    def rightKey(self, event):
        print('increment the count')
        self.update_raw_images('+')
        # Sets amount of fade between pictures
        self.alpha = .2


    # Detects left key press
    def leftKey(self, event):
        print("decrement the count")
        self.update_raw_images('-')
        # Sets amount of fade between pictures
        self.alpha = .2


    def space_key(self, event):
        print('space key pressed')
        

    def z_key(self, event):
        print('Z key pressed')
        self.DIRECTORY = 'hike1/'

    def x_key(self, event):
        print('X key pressed')
        self.DIRECTORY = 'hike2/'

    
    def c_key(self, event):
        print('C key pressed')
        self.DIRECTORY = 'hike3/'


    def v_key(self, event):
        print('V key pressed')
        self.DIRECTORY = 'hike4/'


    # Detects rotary encoder change
    def detectedRotaryChange(self, event):
        clkState = GPIO.input(clk)
        cntState = GPIO.input(cnt)
        if clkState != self.clkLastState:
            # Increment
            if cntState != clkState:
                self.ROTARY_COUNT += 1
                print("Rotary +: ", self.ROTARY_COUNT)
                self.update_raw_images('+')
                # Sets amount of fade between pictures
                self.alpha = .2
            # Decrement
            else:
                self.ROTARY_COUNT -= 1
                print("Rotary -: ", self.ROTARY_COUNT)
                self.update_raw_images('-')
                # Sets amount of fade between pictures
                self.alpha = .2
        self.clkLastState = clkState
        # sleep(0.1)


    # Detect button presses
    def button1_pressed(self, event):
        print('Button 1 pressed')
        self.DIRECTORY = 'hike1/'


    def button2_pressed(self, event):
        print('Button 2 pressed')
        self.DIRECTORY = 'hike2/'


    def button3_pressed(self, event):
        print('Button 3 pressed')
        self.DIRECTORY = 'hike4/'


# Create the root window
root = Tk()
slide_show = Slideshow(root)
root.mainloop()
