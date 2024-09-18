import pygame
import random
import time

# This Dot class gets randomly placed.
class Dot:
    def __init__(self):
        self.position = (random.randint(13, 1267), random.randint(13, 707))
        self.circlewidth = 26
        self.color = (255, 0, 0)

        self.start_time = time.time() # To calculate response time.
        self.response_time = 0
        self.response_time_list = [] # To store response times to calculate the average.

        self.counter = 30
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
                    self.response_time = time.time() - self.start_time
                    self.response_time_list.append(self.response_time)
                    print(self.response_time)
                    self.start_time = time.time()
                    self.position = (random.randint(1, 1280), random.randint(1, 720))
                    self.counter -= 1
                    print(self.counter)
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
    def __init__(self):
        pass
    def refresh(self, ui, response_time):
        response_time_str = "Response time: " + str(float(response_time))[:4] + " seconds"
        font = pygame.font.SysFont(None, 24)
        text_surface = font.render(response_time_str, True, (255, 255, 255))
        ui.blit(text_surface, (6, 6))

class CounterLabel:
    def __init__(self):
        pass
    def refresh(self, ui, counter):
        font = pygame.font.SysFont(None, 36)
        text_surface = font.render(str(counter), True, (255, 255, 255))
        ui.blit(text_surface, (1250, 6))

