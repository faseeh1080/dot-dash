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

        self.counter = 5
        self.game_started = False
        self.game_over = False
    
    # Refresh the mouse position when clicked. Returns the response time.
    def refresh(self, screen,mse_buttons, mse_buttons_previous_frame, mse_pos):
        if self.counter > 0:
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
                    self.counter -= 1
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
    
class ResponseTimeLabel:
    def __init__(self, padding):
        self.pos = (padding, padding)
    def refresh(self, ui, response_time):
        response_time_str = "Response time: " + str(float(response_time))[:4] + " seconds"
        font = pygame.font.SysFont(None, 24)
        text_surface = font.render(response_time_str, True, (255, 255, 255))
        ui.blit(text_surface, self.pos)

class CounterLabel:
    def __init__(self):
        pass
    def refresh(self, ui, screen_width, padding, counter):
        font = pygame.font.SysFont(None, 36)
        text = str(counter)
        text_surface = font.render(str(counter), True, (255, 255, 255))
        text_width = font.size(text)[0]
        position = (screen_width - text_width - padding, padding)
        ui.blit(text_surface, (position))

class GameOverLabel:
    def __init__(self) -> None:
        pass
    def refresh(self, ui, screen_width):
        font = pygame.font.SysFont(None, 56)
        text = "Good Job!"
        text_width = font.size(text)[0]
        text_surface = font.render(text, True, (255, 255, 255))
        text_x_pos = (screen_width / 2) - (text_width / 2)
        ui.blit(text_surface, (text_x_pos, 300))

class AverageResponseTimeLabel:
    def __init__(self) -> None:
        pass
    def refresh(self, ui, screen_width, average_response_time):
        font = pygame.font.SysFont(None, 36)
        text = "Average response time: " + str(average_response_time)[:4]
        text_width = font.size(text)[0]
        text_surface = font.render(text, True, (255, 255, 255))
        text_x_pos = (screen_width / 2) - (text_width / 2)
        ui.blit(text_surface, (text_x_pos, 380))
