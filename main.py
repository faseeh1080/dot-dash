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
dot = Dot(SCREEN_WIDTH, SCREEN_HEIGHT, 5)

# UI classes:
padding = 10
response_time_label = Label(8, "Response time: ", SCREEN_WIDTH, SCREEN_HEIGHT, font_size=24, padding=padding)
counter_label = Label(8, "", SCREEN_WIDTH, SCREEN_HEIGHT, font_size=64, align="right", padding=padding)

game_over_label = Label(280, "Good Job!", SCREEN_WIDTH, SCREEN_HEIGHT, font_size=50, align="center", padding=padding)
average_response_time_label = Label(320, "", SCREEN_WIDTH, SCREEN_HEIGHT, font_size=24, align="center", padding=padding)
restart_label = Label(345, "Press spacebar to restart", SCREEN_WIDTH, SCREEN_HEIGHT, 28, align="center", padding=padding)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                dot.restart()
    mse_buttons = pygame.mouse.get_pressed()
    mse_pos = pygame.mouse.get_pos()


    screen.fill("black")

    # RENDERING THE VIEWPORT:
    viewport.fill((0, 0, 0))
    if not dot.game_over:
        dot.refresh(viewport, mse_buttons, mse_buttons_previous_frame, mse_pos)

    # RENDERING THE UI:
    ui.fill((0, 0, 0, 0))
    if not dot.game_over:
        response_time_text = "Response Time: " + str(dot.response_time)[:4]
        response_time_label.change_text(response_time_text)
        response_time_label.render(ui)
        counter_label.change_text(str(dot.remaining))
        counter_label.render(ui)
    else:
        game_over_label.render(ui)
        average_response_time = dot.calculate_avg_response_time()
        average_response_time_label.change_text("Average Response Time: " + str(average_response_time)[:4])
        average_response_time_label.render(ui)
        restart_label.render(ui)

    screen.blit(viewport, (0, 0))
    screen.blit(ui, (0, 0))
    pygame.display.flip()

    clock.tick(60)
    mse_buttons_previous_frame = mse_buttons
pygame.quit()