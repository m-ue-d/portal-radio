import pygame
import numpy

# colors
# blue: #34f3f7
# black: #000000
# white: #FFFFFF

X = 1200
Y = 800
CENTER = (X // 2, Y // 2)
SCREEN = None
FONT = None
FONT_SMALL = None


class Colors:
    BRIGHT = (200, 255, 255)
    DARK = (52, 243, 247)


def text_with_blooming(c: str, rotation, radius, color, font):
    text = font.render(c, True, color)
    text = pygame.transform.rotate(text, rotation)
    text = pygame.transform.gaussian_blur(text, radius)
    return text


def initGui(x, y):
    global SCREEN, FONT_SMALL, FONT, X, Y
    X = x
    Y = y
    pygame.init()
    SCREEN = pygame.display.set_mode((X, Y))
    FONT = pygame.font.Font("OxygenMono-Regular.ttf", 200)
    FONT_SMALL = pygame.font.Font("OxygenMono-Regular.ttf", 30)
    pygame.display.set_caption("Portal Radio")


def handleGui(potty, mode, special):
    global SCREEN, FONT, X, Y

    if FONT is None or SCREEN is None:
        exit("Gui not initialized")

    SCREEN.fill((0, 0, 0))

    # potty code

    final_text = "{:.1f} FM".format(potty)

    for i, c in enumerate(final_text):
        text_back = text_with_blooming(c, -(i * 10 - len(final_text) * 10 / 2), 12, Colors.DARK, FONT)
        text_fore = text_with_blooming(c, -(i * 10 - len(final_text) * 10 / 2), 4, Colors.BRIGHT, FONT)
        text_rect = text_fore.get_rect()

        x = CENTER[0] + i * 120 - (len(final_text) * 120 - 60) / 2
        y = CENTER[1] + numpy.power(x - X / 2 + 30, 2) / X
        text_rect.center = (x, y)
        SCREEN.blit(text_back, text_rect)
        SCREEN.blit(text_fore, text_rect)

    # mode code
    off_x = 140
    off_y = 25
    text_mode_fore = text_with_blooming(mode, 75, 2, Colors.BRIGHT, FONT_SMALL)
    text_mode_back = text_with_blooming(mode, 75, 8, Colors.DARK, FONT_SMALL)
    text_mode_rect = text_mode_fore.get_rect()
    text_mode_rect.center = (CENTER[0] + off_x, CENTER[1] + off_y)
    SCREEN.blit(text_mode_fore, text_mode_rect)
    SCREEN.blit(text_mode_back, text_mode_rect)

    # special
    off_x = 0
    off_y = 135
    text_mode_fore = text_with_blooming(special, 0, 2, Colors.BRIGHT, FONT_SMALL)
    text_mode_back = text_with_blooming(special, 0, 8, Colors.DARK, FONT_SMALL)
    text_mode_rect = text_mode_fore.get_rect()
    text_mode_rect.center = (CENTER[0] + off_x, CENTER[1] + off_y)
    SCREEN.blit(text_mode_fore, text_mode_rect)
    SCREEN.blit(text_mode_back, text_mode_rect)

    pygame.display.flip()
