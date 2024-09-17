import pygame
import random
import time

# This Dot class gets randomly placed.
class Dot:
    def __init__(self):
        self.position = (random.randint(1, 1280), random.randint(1, 720))
        self.circlewidth = 26
        self.color = (255, 0, 0)
        self.start_time = time.time()
    
    def refresh(self, screen, mse_pos):
        x = self.position[0] - mse_pos[0]
        y = self.position[1] - mse_pos[1]
        hyp = (x**2 + y**2) ** 0.5
        distance_to_mse = hyp
        if distance_to_mse < (self.circlewidth):
            self.position = (random.randint(1, 1280), random.randint(1, 720))
        pygame.draw.circle(screen, self.color, self.position, self.circlewidth)
