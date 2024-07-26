import pygame
import random
import numpy as np
from Utils.Snake import Snake

class Board():
    def __init__(self):
        self.__grid = None
        self.__food_pos = None
        self.__last_food_pos = None
        self.__snake = None
        self.__score = 0
        self.__game_over = False
        self.__cell_size = 0
        self.__current_state = None

    def create_board(self, diff=1) -> None:
        self.__init_grid(diff)
        self.__snake = Snake(self.__grid)
        self.__spawn_food()

    def __spawn_food(self):
        empty_positions = list(zip(*np.where(self.__grid == 0)))
        self.__food_pos = random.choice(empty_positions)
        while self.__food_pos == self.__last_food_pos or self.__food_pos in self.__snake.get_body():
            self.__food_pos = random.choice(empty_positions)
            
        self.__grid[self.__food_pos] = 2
        print("Spawned possition: (", self.__food_pos[0], ",",self.__food_pos[1], ")")
        print(self.__grid)
        print()
        return
    
    def __destroy_food(self):
        self.__grid[self.__food_pos] = 0
        self.__last_food_pos = self.__food_pos
        self.__food_pos = None
        return
        
    def __init_grid(self, diff):
        if diff == 1:
            self.__grid_width = 10 + 2 # 1 plus to de size for each side of the screen for the death zone
            self.__grid_height = 10 + 2
            self.__cell_size = 50
        elif diff == 2:
            self.__grid_width = 20 + 2
            self.__grid_height = 20 + 2
            self.__cell_size = 40
        elif diff == 3:
            self.__grid_width = 30 + 2
            self.__grid_height = 30 + 2
            self.__cell_size = 30
        elif diff == 4:
            self.__grid_width = 60 + 2
            self.__grid_height = 40 + 2
            self.__cell_size = 25
            
        self.__grid = np.zeros((self.__grid_width, self.__grid_height), dtype=int)
        self.__grid[0, :] = -1  # Borde superior
        self.__grid[:, 0] = -1  # Borde izquierdo
        self.__grid[-1, :] = -1  # Borde inferior
        self.__grid[:, -1] = -1  # Borde derecho
        
    def get_cell_size(self):
        return self.__cell_size
        
    def get_grid_size(self):
        return (self.__grid_width, self.__grid_height)
    
    def update(self, input, surface, size):
        self.__check_collisions(input)
        if not self.__game_over:
            self.__snake.move()
            self.__draw_grid(surface)
        else:
            self.reset(size)
    
    def __check_collisions(self, input):
        x, y = self.__snake.get_head()
        self.__snake.set_direction(input)
        new_x, new_y = x, y

        direction = self.__snake.get_direction()
        if direction == 0: new_x += 1
        elif direction == 1: new_y -= 1
        elif direction == 2: new_x -= 1
        elif direction == 3: new_y += 1

        if self.__grid[new_x][new_y] == -1 or (new_x, new_y) in self.__snake.get_body()[1:]:
            self.__game_over = True
        elif self.__grid[new_x][new_y] == 2:
            self.__food_collision()
    
    def __food_collision(self):
        self.__destroy_food()
        self.__snake.grow()
        self.__score += 1
        self.__spawn_food()
        self.__game_over = False
        return
        
    def get_score(self):
        return self.__score
    
    def __draw_grid(self, surface):
        for x in range(1, self.__grid_width - 1):
            for y in range(1, self.__grid_height - 1):
                rect = pygame.Rect((x - 1) * self.__cell_size, (y - 1) * self.__cell_size, self.__cell_size, self.__cell_size)
                color = (0, 0, 0)  # Empty cell color
                if self.__grid[x][y] == 1:
                    color = (0, 255, 0)  # Snake color
                elif self.__grid[x][y] == 2:
                    color = (255, 0, 0)  # Food color
                pygame.draw.rect(surface, color, rect)
                pygame.draw.rect(surface, (55, 55, 55), rect, 1)
        
    def reset(self, size):
        # Create new instances
        self.__destroy_food()
        self.__snake.destroy()
        self.__snake = None
        self.__grid = None
        self.__snake = None
        self.__score = 0
        self.__food_pos = None
        self.__last_food_pos = None
        self.__game_over = False
        self.create_board(size)
        
    def get_grid(self):
        return self.__grid
    
    def print_grid(self):
        print("Current food possition: (", self.__food_pos[0], ",",self.__food_pos[1], ")")
        print(self.__grid)
        
