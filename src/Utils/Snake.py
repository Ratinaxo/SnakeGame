class Snake:
    def __init__(self, grid):
        self.__dir = {0: 'right', 1: 'up', 2: 'left', 3: 'down'}
        self.__grid = grid
        self.__body = None
        self.__old_tail = None
        self.__head = None
        self.__tail = None
        self.__size = -1
        self.__direction = None
        self.__opposite_dir = None
        self.create()
        
        
    def create (self, start_size=3):
        self.__body = []  # Initial snake body
        start_pos = (5, 5)
        self.__body = [(start_pos[0] - i, start_pos[1]) for i in range(start_size)]

        for part in self.__body:
            self.__grid[part] = 1
            self.__size += 1
        self.__head = self.__body[0]
        self.__grid[self.__head] = 1
        self.__tail = self.__body[self.__size]
        self.__old_tail = self.__tail
        self.__direction = 0
        self.__opposite_dir = 2
        
    def move(self):
        xHead, yHead = self.__head
            
        if self.__direction == 0:
            new_head = (xHead + 1, yHead)
            self.__opposite_dir = 2
            
        elif self.__direction == 1:
            new_head = (xHead, yHead - 1)
            self.__opposite_dir = 3
            
        elif self.__direction == 2:
            new_head = (xHead - 1, yHead)
            self.__opposite_dir = 0
            
        elif self.__direction == 3:
            new_head = (xHead, yHead + 1)
            self.__opposite_dir = 1
            
        self.__grid[self.__old_tail] = 0
        
        self.__body = [new_head] + self.__body[:-1]
        self.__head = self.__body[0]
        self.__tail = self.__body[self.__size]
        self.__old_tail = self.__tail
        self.__grid[self.__head] = 1
    
    def set_direction(self, direction=None):
        if direction in [0, 1, 2, 3] and direction != self.__opposite_dir:
            self.__direction = direction

    def get_direction(self):
        return self.__direction

    def grow(self):
        self.__body.append(self.__body[-1])  # Grow snake
        self.__size += 1
    
    def get_head(self):
        return self.__body[0]
    
    def get_body(self):
        return self.__body

    def destroy(self):
        self.__body = None
        self.__head = None
        self.__direction = None
        self.__opposite_dir = None