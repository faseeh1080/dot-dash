import pygame
from classes import *

pygame.init()
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
ui_margine = 6 # Padding for UI elements.
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
viewport = pygame.Surface((1280, 720))
ui = pygame.Surface((1280, 720), pygame.SRCALPHA) # UI supports transparency.
clock = pygame.time.Clock()
running = True
game_over = False

mse_buttons = (False, False, False)
mse_buttons_previous_frame = (False, False, False)

# Viewport Classes:
circle1 = Dot(SCREEN_WIDTH, SCREEN_HEIGHT)

# UI classes:
response_time_label = ResponseTimeLabel(ui_margine)
counter_label = CounterLabel()
game_over_label = GameOverLabel()
average_response_time_label = AverageResponseTimeLabel()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    mse_buttons = pygame.mouse.get_pressed()
    mse_pos = pygame.mouse.get_pos()


    screen.fill("black")

    # RENDERING THE VIEWPORT:
    viewport.fill((0, 0, 0))
    if not circle1.game_over:
        circle1.refresh(viewport, mse_buttons, mse_buttons_previous_frame, mse_pos)

    # RENDERING THE UI:
    ui.fill((0, 0, 0, 0))
    if not circle1.game_over:
        response_time_label.refresh(ui, circle1.response_time)
        counter_label.refresh(ui, SCREEN_WIDTH, ui_margine, circle1.counter)
    else:
        game_over_label.refresh(ui, SCREEN_WIDTH)
        average_response_time = circle1.calculate_avg_response_time()
        average_response_time_label.refresh(ui, SCREEN_WIDTH, average_response_time)

    screen.blit(viewport, (0, 0))
    screen.blit(ui, (0, 0))
    pygame.display.flip()

    clock.tick(60)
    mse_buttons_previous_frame = mse_buttons
pygame.quit()