import os
import _thread
from datetime import datetime
from pygame import mixer
import cv2.cv2

# GLOBALS
MODES = ["default", "bluetooth", "alarm"]
POTTY = 0
BUTTON = False
SUBTASK = None
CLOSE_REQUEST = False
IMAGE = None


# TODO: On Raspberry PI (the code here is temporary and just toggles the button)
def update_io():
    global BUTTON
    global POTTY
    choice = str(input("\nBUTTON?/POTTY?: "))
    if choice == "t":
        BUTTON = True
    elif choice == "f":
        BUTTON = False
    elif choice.startswith("p"):
        POTTY = float(choice[1::])
    print("Button: " + str(BUTTON) + ", Potty: " + str(POTTY))


# TODO: play the portal radio audio file on repeat (just needs testing and a proper path...) (also, please use the
#  10h version, as the cuts can get annoying, but consider trying the other one first, because i made some tweaks
#  just now...)
def play_radio():
    global SUBTASK
    global BUTTON
    global CLOSE_REQUEST
    # radio code goes here
    path = "C:\\Users\\" + os.getlogin() + "\\Music\\portal-radio.mp3"
    print("Radio Thread Running")
    mixer.init()
    mixer.music.load(path)
    while not CLOSE_REQUEST:
        mixer.music.play()
        while mixer.music.get_busy() and not CLOSE_REQUEST:  # wait for music to stop
            continue
    mixer.music.fadeout(2000)
    SUBTASK = None


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
    # alarm code goes here
    print("Alarm Thread Running")
    hour = 0
    minute = 0

    # 1.: setup alarm
    while BUTTON:
        continue
    print("Hours...")
    while not BUTTON:   #Annahme: Potty kann zwischen 0 und 1 sein          0,375   ,   0,5833
        hour = int(POTTY / (1.0 / 24.0))
        if CLOSE_REQUEST:
            SUBTASK = None
            return
    while BUTTON:
        continue
    print("Minutes")
    while not BUTTON:
        minute = int((POTTY / (1.0 / 12.0)) * 5)
        if CLOSE_REQUEST:
            SUBTASK = None
            return
    while BUTTON:
        continue
    print("Alarm set to: {"+str(hour)+", "+str(minute)+"}")

    # 2.: wait for set amount of time...
    now = datetime.now()
    while not CLOSE_REQUEST and (now.hour != hour or now.minute != minute):
        now = datetime.now()

    # 3.: ring... ring...
    path = "C:\\Users\\" + os.getlogin() + "\\Music\\portal-radio.mp3"
    print("Alarm Ringing!")
    mixer.init()
    mixer.music.load(path)
    mixer.music.set_volume(2)
    while not CLOSE_REQUEST:
        mixer.music.play()
        while mixer.music.get_busy() and not CLOSE_REQUEST:  # wait for music to stop
            continue
    mixer.music.fadeout(2000)
    SUBTASK = None


def initGui():
    global IMAGE
    IMAGE = cv2.imread("C://", cv2.IMREAD_ANYCOLOR)
    cv2.imshow("Portal Radio", IMAGE)


def update_gui(mode, potty):
    global IMAGE


def main():
    global MODES
    global POTTY
    global BUTTON
    global SUBTASK
    global CLOSE_REQUEST
    current = 0
    previous = BUTTON
    initGui()

    while True:
        update_io()
        if not previous and BUTTON and POTTY < 0.02:
            # do GUI stuff
            if cv2.waitKey(0):
                cv2.destroyAllWindows()
                exit(0)
            update_gui(MODES[current], POTTY)
            # do mode stuff
            if SUBTASK is not None:
                print("SUBTASK ALREDY RUNNING (close request sent)")
                CLOSE_REQUEST = True
            elif current == 0:
                CLOSE_REQUEST = False
                SUBTASK = "default"
                _thread.start_new_thread(play_radio, ())
                current = (current + 1) % len(MODES)
            elif current == 1:
                CLOSE_REQUEST = False
                SUBTASK = "bluetooth"
                _thread.start_new_thread(enable_bluetooth, ())
                current = (current + 1) % len(MODES)
            elif current == 2:
                CLOSE_REQUEST = False
                SUBTASK = "alarm"
                _thread.start_new_thread(alarm, ())
                current = (current + 1) % len(MODES)
        previous = BUTTON


if __name__ == "__main__":
    main()
