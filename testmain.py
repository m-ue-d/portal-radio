import numpy
import pygame
import gui
import time


def main():
    gui.initGui(1200, 800)
    modes = ["default", "bluetooth", "alarm", "phone-app"]
    special = ["12:10 UTC+1", "connected", "TheFatRat - Unity"]  # used by the modes to resemble a state clearly
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        gui.handleGui(numpy.random.random_sample()*50+50, modes[int(numpy.random.random_sample()*4)], special[int(numpy.random.random_sample()*3)])
        time.sleep(0.5)


main()
pygame.quit()
