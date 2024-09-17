import pygame
import random
import time

# This Dot class gets randomly placed.
class Dot:
    def __init__(self):
        self.position = (random.randint(1, 1267), random.randint(1, 707))
        self.circlewidth = 26
        self.color = (255, 0, 0)

        self.start_time = time.time() # To calculate response time.
        self.response_time = 0
        self.response_time_list = [] # To store response times to calculate the average.
    
    # Refresh the mouse position when clicked. Returns the response time.
    def refresh(self, screen,mse_buttons, mse_buttons_previous_frame, mse_pos):
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
        pygame.draw.circle(screen, self.color, self.position, self.circlewidth)
        return self.response_time

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
        font = pygame.font.SysFont(None, 24)
        text_surface = font.render("Response time: " + str(response_time) + " seconds", True, (255, 255, 255))
        ui.blit(text_surface, (6, 6))
