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
padding = 10
response_time_label = Label(8, "Response time: ", SCREEN_WIDTH, SCREEN_HEIGHT, font_size=24, padding=padding)
counter_label = Label(8, "", SCREEN_WIDTH, SCREEN_HEIGHT, font_size=64, align="right", padding=padding)
game_over_label = Label(8, "Good Job!", SCREEN_WIDTH, SCREEN_HEIGHT, font_size=24, align="center", padding=padding)
average_response_time_label = Label(50, "", SCREEN_WIDTH, SCREEN_HEIGHT, font_size=24, align="center", padding=padding)

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
        response_time_text = "Response Time: " + str(circle1.response_time)[:4]
        response_time_label.change_text("Response Time: " + response_time_text)
        response_time_label.render(ui)
        counter_label.change_text(str(circle1.remaining))
        counter_label.render(ui)
    else:
        game_over_label.render(ui)
        average_response_time = circle1.calculate_avg_response_time()
        average_response_time_label.change_text("Average Response Time: " + str(average_response_time)[:4])
        average_response_time_label.render(ui)

    screen.blit(viewport, (0, 0))
    screen.blit(ui, (0, 0))
    pygame.display.flip()

    clock.tick(60)
    mse_buttons_previous_frame = mse_buttons
pygame.quit()