import pygame
from classes import *

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True

mse_buttons_previous_frame = (False, False, False)
response_time = 0

font = pygame.font.SysFont(None, 24)
score = font.render("Response time: " + str(response_time), True, (255, 255, 255))
circle1 = Dot()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    mse_buttons = pygame.mouse.get_pressed()
    mse_pos = pygame.mouse.get_pos()

    screen.fill("black")

    response_time = circle1.refresh(screen,mse_buttons, mse_buttons_previous_frame, mse_pos)
    shrinked_response_time = str(response_time)[:4]
    score = font.render("Response time: " + shrinked_response_time + " seconds", True, (255, 255, 255))
    screen.blit(score, (4, 4))


    pygame.display.flip()

    clock.tick(60)
    mse_buttons_previous_frame = mse_buttons
pygame.quit()