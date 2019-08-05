import pygame
import time
import math 
import colorsys

BAR_WIDTH = 40
NOTES = 87

SIDE_LENGTH = 400

black = [0, 0, 0]
white = [255, 0, 255]
red = [255, 0, 0]
        
class CircleAnalyzerOutputSource:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode([SIDE_LENGTH,SIDE_LENGTH])
        self.max_radius = SIDE_LENGTH/2
        self.min_radius = 1
        self.screen.fill(black)
        pygame.display.set_caption("My program")
        pygame.display.flip()

    # red green blue values are between 0 and 1
    def display(self, red, green, blue):
        center = (int(SIDE_LENGTH/2), int(SIDE_LENGTH/2))
        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                pygame.quit()

        hsv = colorsys.rgb_to_hsv(red, green, blue)
        color = [int(x * 255) for x in colorsys.hsv_to_rgb(hsv[0], hsv[1], 1)]
        radius = (hsv[2] * (self.max_radius - self.min_radius) ) + self.min_radius 
        self.screen.fill(black)
        pygame.draw.circle(self.screen, color, center, int(radius), int(0))
        pygame.display.flip()
        # yield
        time.sleep(0)

    def shutdown(self):
        pygame.quit()
