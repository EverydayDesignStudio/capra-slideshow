#!/usr/bin/env python3

# Imports
import sys
from PIL import ImageTk, Image
from RPi import GPIO
from time import sleep
from tkinter import Tk, Label

# Setup for GPIO
clk = 17
cnt = 18

GPIO.setmode(GPIO.BCM)
GPIO.setup(clk, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(cnt, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# Slideshow class which is the main class that runs and is listening for events
class Slideshow:
    _DIRECTORY = 'hike4/'
    _EXTENSION = '.jpg'
    # FILE_PATH = ''
    FILE_PATH = 'hike4/2.jpg'
    COUNT = 0
    _LIMIT = 241
    
    ROTARY_COUNTER = 1
    clkLastState = GPIO.input(clk)

    def __init__(self, win):
        self.window = win
        self.window.title("Capra")
        self.window.geometry("1280x720")
        self.window.configure(background='black')

        self.moveFilePointer('+')
        self.img = ImageTk.PhotoImage(Image.open(self.FILE_PATH, 'r'))
        self.picture_label = Label(master=self.window, image=self.img)
        self.picture_label.pack(side="bottom", fill="both", expand="yes")

        self.window.bind('<Left>', self.leftKey)
        self.window.bind('<Right>', self.rightKey)
        
        self.window.bind(GPIO.add_event_detect(clk, GPIO.BOTH, callback=self.detectedRotaryChange))
    
    def detectedRotaryChange(self, event):
        clkState = GPIO.input(clk)
        cntState = GPIO.input(cnt)
        if clkState != self.clkLastState:
            if cntState != clkState:
                self.ROTARY_COUNTER += 1
            else:
                self.ROTARY_COUNTER -= 1
        self.clkLastState = clkState
        sleep(0.01)
        
        self.buildFilePointer()
        self.showImage()
    
    def showImage(self):
        self.img = ImageTk.PhotoImage(Image.open(self.FILE_PATH, 'r'))
        self.picture_label.configure(image=self.img)
        
    def buildFilePointer(self):
        if self.ROTARY_COUNTER > self._LIMIT:
            self.ROTARY_COUNTER = 1
        elif self.ROTARY_COUNTER < 1:
            self.ROTARY_COUNTER = self._LIMIT
        print(self.ROTARY_COUNTER)
            
        self.FILE_PATH = self._DIRECTORY + str(self.ROTARY_COUNTER) + self._EXTENSION

    def moveFilePointer(self, command):
        if command == '+':
            self.COUNT += 1
            if self.COUNT > self._LIMIT:
                self.COUNT = 1
        elif command == '-':
            self.COUNT -= 1
            if self.COUNT < 1:
                self.COUNT = self._LIMIT
        else:
            raise Exception('command should be either '+' or '-'')

        self.FILE_PATH = self._DIRECTORY + str(self.COUNT) + self._EXTENSION
        sys.stdout.flush()
        print(self.FILE_PATH)
        sys.stdout.flush()

    def rightKey(self, event):
        print("Increment the count")
        self.moveFilePointer('+')
        self.showImage()

    def leftKey(self, event):
        print("Decrement the count")
        self.moveFilePointer('-')
        self.showImage()
    
# Create the root window
root = Tk()
slide_show = Slideshow(root)
root.mainloop()