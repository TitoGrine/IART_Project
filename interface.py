import pygame
import levels
import math
import constants

pygame.init()

pygame.display.set_caption("Zhed")
window = pygame.display.set_mode((800, 800))

level = levels.Levels().get_level(1)
width = 100
heigth = 100


run = True
while run:
    pygame.time.delay(100)

    for i in range(0, 64):
        x_pos = (i % 8) * 100
        y_pos = (math.floor(i / 8)) * 100
        tile = level[i]

        if   (tile == constants.GOAL):
            pygame.draw.rect(window, (255, 102,   0), (x_pos, y_pos, width, heigth))
        elif (tile == constants.EMPTY):
            pygame.draw.rect(window, (192, 192, 192), (x_pos, y_pos, width, heigth))
        elif (tile == constants.FILLED):
            pygame.draw.rect(window, (255, 204,   0), (x_pos, y_pos, width, heigth))
        else:
            pygame.draw.rect(window, (255, 255, 255), (x_pos, y_pos, width, heigth))
        
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()