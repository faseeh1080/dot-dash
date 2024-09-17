import pygame
import random
import time

# This Dot class gets randomly placed.
class Dot:
    def __init__(self):
        self.position = (random.randint(1, 1267), random.randint(1, 707))
        self.circlewidth = 26
        self.color = (255, 0, 0)
        self.start_time = time.time()
        self.response_time = 0
        self.response_time_list = []
    
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

    def calculate_avg_response_time(self):
        if self.response_time_list:
            average_response_time = sum(self.response_time_list) / len(self.response_time_list)
        else: average_response_time = 0
        return average_response_time