import pygame
import random
import time

# This Dot class gets randomly placed.
class Dot:
    def __init__(self, screen_width, screen_height, total_number: int) -> None:
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
        self.response_time_list = [] # To calculate the average.

        self.total_number = total_number
        self.remaining = self.total_number
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
                    #  To not calculate the reponse time for initial click. \/
                    if not self.game_over and  not (self.remaining == self.total_number):
                        self.response_time = time.time() - self.start_time
                        self.response_time_list.append(self.response_time)
                    self.start_time = time.time()
                    self.position = (random.randint(self.pos_x_min, self.pos_x_max),
                                    random.randint(self.pos_y_min, self.pos_y_max))
                    self.remaining -= 1
            pygame.draw.circle(screen, self.color, self.position, self.circlewidth)
        else:
            self.game_over = True

    # Returns the average response time from response_time_list. !--- Can return None value --!
    def calculate_avg_response_time(self):
        if self.response_time_list:
            average_response_time = sum(self.response_time_list) / len(self.response_time_list)
        else: average_response_time = None

        return average_response_time
    
    def restart(self):
        self.remaining = self.total_number
        self.response_time = 0
        self.response_time_list = []
        self.game_over = False

class Label: # align can be "center", "left" and "right".
    def __init__(self, ypos, text, SCREEN_WIDTH, SCREEN_HEIGHT,
                 font_size=24, align="left", margin=6,
                 color=(255, 255, 255)) -> None:
        self.text = text
        self.SCREEN_WIDTH = SCREEN_WIDTH
        self.SCREEN_HEIGHT = SCREEN_HEIGHT
        self.font_size = font_size
        self.align = align
        self.padding = margin
        self.font = pygame.font.SysFont(None, self.font_size)
        self.size = self.font.size(self.text)
        self.color = color
        self.pos = [0, ypos]
        self.calculate_positions()
        self.text_surface = self.font.render(self.text, True, self.color)

    def calculate_positions(self):
        self.pos[0] = self.padding # Default align left.
        if self.align == "right":
            self.pos[0] = self.SCREEN_WIDTH - self.padding - self.size[0]
        elif self.align == "center":
            self.pos[0] = (self.SCREEN_WIDTH / 2) - (self.size[0] / 2)

    def render(self, surface):
        surface.blit(self.text_surface, self.pos)

    def change_text(self, new_text: str):
        self.text = new_text
        self.size = self.font.size(self.text)
        self.calculate_positions()
        self.text_surface = self.font.render(self.text, True, self.color)
        
class Button:
    def __init__(self, ypos, text, SCREEN_WIDTH, SCREEN_HEIGHT,
                 font_size=24, align="left", padding=4, margin=6,
                 color=(255, 255, 255), bg_color=(0,0,100)) -> None:
        self.text = text
        self.SCREEN_WIDTH = SCREEN_WIDTH
        self.SCREEN_HEIGHT = SCREEN_HEIGHT
        self.font_size = font_size
        self.align = align
        self.padding = padding
        self.margin = margin
        self.color = color
        self.bg_color = bg_color
        self.surface = None
        self.text_surface = None
        self.font = pygame.font.SysFont(None, self.font_size)
        self.text_size = None
        self.create_surface()
        self.pos = [0, ypos]
        self.calculate_pos()
        self.clicked = False

    # Draws the button to self.surface.
    def create_surface(self):
        self.text_size = self.font.size(self.text) # Size of the text surface.
        self.surface_size = (self.text_size[0] + self.padding * 2,
                             self.text_size[1] + self.padding * 2)
        self.surface = pygame.Surface((self.surface_size), pygame.SRCALPHA)
        self.surface.fill(self.bg_color)
        self.text_surface = self.font.render(self.text, True, self.color)
        self.surface.blit(self.text_surface, (self.padding, self.padding))

    def calculate_pos(self):
        self.pos[0] = self.padding + self.margin # Default pos left.
        if self.align == "right":
            self.pos[0] = self.SCREEN_WIDTH - self.padding - self.margin - self.text_size[0]
        elif self.align == "center":
            self.pos[0] = (
                (self.SCREEN_WIDTH / 2) - (self.padding / 2) - 
                (self.margin / 2) - (self.text_size[0] / 2)
            )

    def render(self, surface):
        surface.blit(self.surface, self.pos)

    def is_clicked(self, mse_buttons, mse_buttons_previous_frame, mse_pos):
        if (
            (mse_buttons[0] and not mse_buttons_previous_frame[0]) and
            mse_pos[0] > self.pos[0] and
            mse_pos[1] > self.pos[1] and
            mse_pos[0] < self.pos[0] + self.surface.get_width() and
            mse_pos[1] < self.pos[1] + self.surface.get_height()
        ):
            self.clicked = True
        else:
            self.clicked = False
            
class Notification:
    def __init__(self, text="Notification", text_size=12) -> None:
        self.text = text
        self.text_size = text_size
        font_size = 20
        self.font = pygame.font.SysFont(None, font_size)
        self.text_color = (255, 255, 255)
        self.text_surface = self.font.render(self.text, True, self.text_color)
        self.text_surface_width = self.text_surface.get_width()

        self.start_time = time.time()
        self.time_to_hold = 3.0

    def render(self, surface):
        elapsed_time = time.time() - self.start_time
        if elapsed_time > self.time_to_hold:
            return
        surface_width = surface.get_width()
        surface_height = surface.get_height()
        position = ((surface_width / 2) - (self.text_surface_width / 2),
                    surface_height - 26)
        surface.blit(self.text_surface, position)
        
    def change_text(self, new_text):
        self.text = new_text
        self.text_surface = self.font.render(self.text, True, self.text_color)
        self.text_surface_width = self.text_surface.get_width()
        self.start_time = time.time()
