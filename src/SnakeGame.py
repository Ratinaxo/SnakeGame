import pygame
from Utils.Board import Board

class SnakeGame:
    def __init__(self):
        self.__tickrate = 8
        self.__difficulty = 1
        pygame.init()
        pygame.display.set_caption("Snake for RL (Ratin)")
        self.__board = Board()
        self.__board.create_board(self.__difficulty)  # 1: 15x15 board; 2: 20x20; 3: 30x30; 4: 60x40
        self.__cell_size = self.__board.get_cell_size()
        self.__init_surface()
        self.__running = False
        self.__paused = False
        self.__last_input_time = 0  # Initialize the last input time for delay
        self.__input_delay = 100  # Delay in milliseconds between inputs

    def __init_surface(self):
        screen_width = (self.__board.get_grid_size()[0] - 2) * self.__cell_size
        screen_height = (self.__board.get_grid_size()[1] - 2) * self.__cell_size
        self.__surface = pygame.display.set_mode((screen_width, screen_height))
        self.__font = pygame.font.Font(None, 36)
        self.__font.set_italic(True)

    def run(self, running):
        self.__running = running
        while self.__running:
            pygame.time.Clock().tick(self.__tickrate)
            self.__surface.fill((0, 0, 0))
            score_text = self.__font.render(f"Score: {self.__board.get_score()}", True, (255, 255, 255))
            self.__event_handler()
            if not self.__paused:
                self.__board.update(self.__input_handler(), self.__surface, self.__difficulty)
                self.__surface.blit(score_text, (self.__cell_size, self.__cell_size))
                pygame.display.update()
        pygame.quit()

    def __input_handler(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.__last_input_time < self.__input_delay:
            return None

        key = pygame.key.get_pressed()
        if key[pygame.K_d]:
            self.__last_input_time = current_time
            return 0
        if key[pygame.K_w]:
            self.__last_input_time = current_time
            return 1
        if key[pygame.K_a]:
            self.__last_input_time = current_time
            return 2
        if key[pygame.K_s]:
            self.__last_input_time = current_time
            return 3
        if key[pygame.K_r]:
            self.__reset_game()
        return None

    def __event_handler(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (pygame.key.get_pressed()[pygame.K_ESCAPE]):
                self.__running = False
                return
            if event.type == pygame.KEYDOWN:
                if pygame.key.get_pressed()[pygame.K_p]:
                    self.__paused = not self.__paused
                if pygame.key.get_pressed()[pygame.K_q]:
                    print()
                    self.__board.print_grid()
                    
    def __reset_game(self):
        self.__board.reset(self.__difficulty)
        self.__running = True

if __name__ == "__main__":
    game = SnakeGame()
    game.run(True)
