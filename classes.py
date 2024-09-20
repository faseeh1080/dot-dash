import pygame
import random
import time

# This Dot class gets randomly placed.
class Dot:
    def __init__(self, screen_width, screen_height):
        self.circlewidth = 26
        self.color = (255, 0, 0)

        self.pos_x_min = self.circlewidth
        self.pos_x_max = screen_width - self.circlewidth
        self.pos_y_min = self.circlewidth
        self.pos_y_max = screen_height - self.circlewidth
        self.position = (random.randint(self.pos_x_min, self.pos_x_max),
                        random.randint(self.pos_y_min, self.pos_y_max))

        self.start_time = time.time() # To calculate response time.
        self.response_time = 0
        self.response_time_list = [] # To store response times to calculate the average.

        self.remaining = 5
        self.game_started = False
        self.game_over = False
    
    # Refresh the mouse position when clicked. Returns the response time.
    def refresh(self, screen,mse_buttons, mse_buttons_previous_frame, mse_pos):
        if self.remaining > 0:
            self.game_over = False
            if mse_buttons[0] and not mse_buttons_previous_frame[0]:
                x = self.position[0] - mse_pos[0]
                y = self.position[1] - mse_pos[1]
                hyp = (x**2 + y**2) ** 0.5
                distance_to_mse = hyp
                if distance_to_mse < (self.circlewidth):
                    if self.game_started:
                        self.response_time = time.time() - self.start_time
                        self.response_time_list.append(self.response_time)
                    self.start_time = time.time()
                    self.position = (random.randint(self.pos_x_min, self.pos_x_max),
                                    random.randint(self.pos_y_min, self.pos_y_max))
                    self.remaining -= 1
                    self.game_started = True
            pygame.draw.circle(screen, self.color, self.position, self.circlewidth)
        else:
            self.game_over = True

    # Returns the average response time from response_time_list. !--- Can return None value --!
    def calculate_avg_response_time(self):
        if self.response_time_list:
            average_response_time = sum(self.response_time_list) / len(self.response_time_list)
        else: average_response_time = None

        return average_response_time

class Label: # align can be "center", "left" and "right".
    def __init__(self, ypos, text, SCREEN_WIDTH, SCREEN_HEIGHT, font_size=24, align="left", padding=6, color=(255, 255, 255)) -> None:
        self.text = text
        self.SCREEN_WIDTH = SCREEN_WIDTH
        self.SCREEN_HEIGHT = SCREEN_HEIGHT
        self.font_size = font_size
        self.align = align
        self.padding = padding
        self.font = pygame.font.SysFont(None, self.font_size)
        self.size = self.font.size(self.text)
        self.color = color
        self.pos = [padding, ypos] # Default align left.
        if self.align == "right":
            self.pos[0] = self.SCREEN_WIDTH - self.padding - self.size[0]
        elif self.align == "center":
            self.pos[0] = (self.SCREEN_WIDTH / 2) - (self.size[0] / 2)
        self.text_surface = self.font.render(self.text, True, self.color)

    def render(self, surface):
        surface.blit(self.text_surface, self.pos)

    def change_text(self, new_text: str):
        self.text = new_text
        self.size = self.font.size(self.text)
        self.calculate_positions()
        self.text_surface = self.font.render(self.text, True, self.color)
        
    def calculate_positions(self):
        self.pos[0] = self.padding # Default align left.
        if self.align == "right":
            self.pos[0] = self.SCREEN_WIDTH - self.padding - self.size[0]
        elif self.align == "center":
            self.pos[0] = (self.SCREEN_WIDTH / 2) - (self.size[0] / 2)
