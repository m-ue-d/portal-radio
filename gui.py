import pygame
import numpy

# colors
# blue: #34f3f7
# black: #000000
# white: #FFFFFF

X = 800
Y = 480
CENTER = (X // 2, Y // 2)
SCREEN = None
FONT = None
FONT_SIZE = 80
FONT_SMALL = None
FONT_SIZE_SMALL = 25


class Colors:
    BRIGHT = (200, 255, 255)
    DARK = (52, 243, 247)


def text_with_blooming(c: str, rotation, radius, color, font):
    text = font.render(c, True, color)
    text = pygame.transform.rotate(text, rotation)
    text = pygame.transform.gaussian_blur(text, radius)
    return text


def initGui():
    global SCREEN, FONT_SMALL, FONT, X, Y
    pygame.init()
    SCREEN = pygame.display.set_mode((X, Y))
    FONT = pygame.font.Font("OxygenMono-Regular.ttf", FONT_SIZE)
    FONT_SMALL = pygame.font.Font("OxygenMono-Regular.ttf", FONT_SIZE_SMALL)
    pygame.display.set_caption("Portal Radio")


def handleGui(potty, mode, special):
    global SCREEN, FONT, X, Y

    if FONT is None or SCREEN is None:
        exit("Gui not initialized")

    SCREEN.fill((0, 0, 0))

    # potty code
    final_text = "{:04.1f} FM".format(potty)
    if mode == "Alarm":
        final_text = special

    offset_multiplier_x = 50
    offset_multiplier_y = 4
    rotation_multiplier = 4

    for i, c in enumerate(final_text):
        rotation = -2 * (i - (len(final_text)-1)/2) * rotation_multiplier
        text_fore = text_with_blooming(c, rotation, 2, Colors.BRIGHT, FONT)
        text_back = text_with_blooming(c, rotation, 12, Colors.DARK, FONT)
        x = CENTER[0] + i * offset_multiplier_x - (len(final_text) * offset_multiplier_x - FONT_SIZE/2) / 2
        y = CENTER[1] + numpy.power(i - (len(final_text)-1)/2, 2) * offset_multiplier_y
        text_rect = text_fore.get_rect()
        text_rect.center = (x, y)
        SCREEN.blit(text_back, text_rect)
        SCREEN.blit(text_fore, text_rect)


    # mode code
    x = CENTER[0] + offset_multiplier_x - (len(final_text) * offset_multiplier_x - FONT_SIZE/2) / 2
    y = CENTER[1] + numpy.power(1 - (len(final_text)-1)/2, 2) * offset_multiplier_y + 60
    rotation = -2 * (1 - (len(final_text)-1)/2) * rotation_multiplier
    text_mode_fore = text_with_blooming(mode, rotation, 2, Colors.BRIGHT, FONT_SMALL)
    text_mode_back = text_with_blooming(mode, rotation, 8, Colors.DARK, FONT_SMALL)
    text_mode_rect = text_mode_fore.get_rect()
    text_mode_rect.center = (x, y)
    SCREEN.blit(text_mode_fore, text_mode_rect)
    SCREEN.blit(text_mode_back, text_mode_rect)

    # special
    text = special
    if mode == "Alarm":
        text = "{:04.1f} FM".format(potty)

    i = len(final_text)-2
    x = CENTER[0] + i * offset_multiplier_x - (len(final_text) * offset_multiplier_x - FONT_SIZE / 2) / 2
    y = CENTER[1] + numpy.power(i - (len(final_text) - 1) / 2, 2) * offset_multiplier_y + 60
    rotation = -2 * (i - (len(final_text) - 1) / 2) * rotation_multiplier
    text_mode_fore = text_with_blooming(text, rotation, 2, Colors.BRIGHT, FONT_SMALL)
    text_mode_back = text_with_blooming(text, rotation, 8, Colors.DARK, FONT_SMALL)
    text_mode_rect = text_mode_fore.get_rect()
    text_mode_rect.center = (x, y)
    SCREEN.blit(text_mode_fore, text_mode_rect)
    SCREEN.blit(text_mode_back, text_mode_rect)

    pygame.display.flip()
