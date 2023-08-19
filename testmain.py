import _thread
from datetime import datetime
from subprocess import call

from pygame import mixer
import pygame

import gui

# GLOBALS
MODES = ["Standby", "Default", "Bluetooth", "Alarm"]
POTTY = 0
BUTTON = False
SUBTASK = None
CLOSE_REQUEST = False
STATUS = "Standby"


# TODO: On Raspberry PI (the code here is temporary and just toggles the button)
def update_io():
    global BUTTON
    global POTTY

    while True:
        POTTY = float(input("POTTY "))


def play_radio():
    global SUBTASK
    global BUTTON
    global CLOSE_REQUEST
    global STATUS
    # radio code goes here
    path = "C:\\Users\\Admin\\Music\\Vienna-Calling_Nightcore.mp3"
    print("Radio Thread Running")
    mixer.init()
    mixer.music.load(path)
    while not CLOSE_REQUEST:
        mixer.music.play()
        while mixer.music.get_busy() and not CLOSE_REQUEST:  # wait for music to stop
            STATUS = "Playing"
            #call(["amixer", "-D", "pulse", "sset", "Master", str(POTTY) + "%"]) # TODO: try on linux
    mixer.music.fadeout(2000)
    SUBTASK = None
    STATUS = "Done"


# TODO: execute bluetooth scripts here
def enable_bluetooth():
    global SUBTASK
    # bluetooth code goes here
    print("Bluetooth Thread Running")

    SUBTASK = None


# TODO: put alarm cycle here
def alarm():
    global SUBTASK
    global BUTTON
    global POTTY
    global STATUS
    # alarm code goes here
    print("Alarm Thread Running")
    hour = 0
    minute = 0
    STATUS = "00h:00m"

    # 1.: setup alarm
    while BUTTON:
        continue
    print("Hours...")
    while not BUTTON:  # Annahme: Potty kann zwischen 0 und 1 sein          0,375   ,   0,5833
        hour = int(POTTY / (1.0 / 24.0))
        STATUS = "{:02d}h:00m".format(hour)
    while BUTTON:
        continue
    print("Minutes")
    while not BUTTON:
        minute = int((POTTY / (1.0 / 12.0)) * 5)
        STATUS = "{:02d}h:{:02d}m".format(hour, minute)
    while BUTTON:
        continue
    print("Alarm set to: {" + str(hour) + ", " + str(minute) + "}")

    # 2.: wait for set amount of time...
    now = datetime.now()
    while not CLOSE_REQUEST and (now.hour != hour or now.minute != minute):
        now = datetime.now()
    if CLOSE_REQUEST:
        SUBTASK = None
        return

    # 3.: ring... ring...
    path = "C:\\Users\\Admin\\Music\\Vienna-Calling_Nightcore.mp3"
    print("Alarm Ringing!")
    mixer.init()
    mixer.music.load(path)
    #call(["amixer", "-D", "pulse", "sset", "Master", "100%"])  # TODO: try on linux
    while not CLOSE_REQUEST:
        mixer.music.play()
        while mixer.music.get_busy() and not CLOSE_REQUEST:  # wait for music to stop
            continue
    mixer.music.fadeout(2000)
    SUBTASK = None


def update_gui(mode, potty):
    global POTTY
    global BUTTON
    print("POTTY: " + str(POTTY) + ", BUTTON: " + str(BUTTON))


def main():
    global MODES
    global POTTY
    global BUTTON
    global SUBTASK
    global CLOSE_REQUEST
    global STATUS
    current = 0
    previous = BUTTON
    gui.initGui()

    _thread.start_new_thread(update_io, ())

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:            # update FULLSCREEN/BUTTON on PC
                pressed = pygame.key.get_pressed()      # update FULLSCREEN/BUTTON on PC
                if pressed[pygame.K_f]:                 # update FULLSCREEN on PC
                    pygame.display.toggle_fullscreen()  # update FULLSCREEN on PC
                if pressed[pygame.K_SPACE]: # update BUTTON on PC
                    BUTTON = True           # update BUTTON on PC
                else:                       # update BUTTON on PC
                    BUTTON = False          # update BUTTON on PC

        gui.handleGui(POTTY*100, MODES[current], STATUS)
        if not previous and BUTTON:
            # do mode stuff
            if SUBTASK is not None:
                print("SUBTASK ALREADY RUNNING (close request sent)")
                CLOSE_REQUEST = True
            elif current == 0:
                CLOSE_REQUEST = False
                SUBTASK = "Default"
                _thread.start_new_thread(play_radio, ())
                current = (current + 1) % len(MODES)
            elif current == 1:
                CLOSE_REQUEST = False
                SUBTASK = "Bluetooth"
                _thread.start_new_thread(enable_bluetooth, ())
                current = (current + 1) % len(MODES)
            elif current == 2:
                CLOSE_REQUEST = False
                SUBTASK = "Alarm"
                _thread.start_new_thread(alarm, ())
                current = (current + 1) % len(MODES)
        previous = BUTTON


if __name__ == "__main__":
    main()
