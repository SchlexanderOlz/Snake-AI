import pygame
#import torch
import matplotlib
from collections import namedtuple
import random
from enum import Enum
import time


pygame.init()
Point = namedtuple("Point", "x, y")

BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)


class Directions(Enum):
    UP = 1,
    RIGHT = 2,
    DOWN = 3,
    LEFT = 4


class Snake:
    
    def __init__(self, block_size=20, block_x_length=32, block_y_length=20) -> None:
        self.WINDOWSIZE = (block_x_length * block_size, block_y_length * block_size)
        self.blocks_x = block_x_length
        self.blocks_y = block_y_length
        self.BLOCKSIZE = block_size
        
        self.display = pygame.display.set_mode(self.WINDOWSIZE)

        self.head = Point(self.WINDOWSIZE[0] / 2, self.WINDOWSIZE[1] / 2)
        self.snake = [self.head, Point(self.head.x - self.BLOCKSIZE, self.head.y), Point(self.head.x  - 2 * self.BLOCKSIZE, self.head.y)]
        self.mov_dir = Directions.RIGHT
        self.place_food()
        
    def place_food(self):
        self.food = Point(random.randint(0, self.blocks_x) * self.BLOCKSIZE, random.randint(0, self.blocks_y) * self.BLOCKSIZE)
        
    def run(self):
        notfound = True

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit(0)
                if event.type == pygame.KEYDOWN:
                    match event.dict.get("key"):
                        case pygame.K_UP:
                            self.mov_dir = Directions.UP
                            self.snake.insert(0, Point(self.head.x, self.head.y - self.BLOCKSIZE))
                            notfound = False
                            break
                        case pygame.K_DOWN:
                            self.mov_dir = Directions.DOWN
                            self.snake.insert(0, Point(self.head.x, self.head.y + self.BLOCKSIZE))
                            notfound = False
                            break
                        case pygame.K_LEFT:
                            self.mov_dir = Directions.LEFT
                            self.snake.insert(0, Point(self.head.x - self.BLOCKSIZE, self.head.y))
                            notfound = False
                            break
                        case pygame.K_RIGHT:
                            self.mov_dir = Directions.RIGHT
                            self.snake.insert(0, Point(self.head.x + self.BLOCKSIZE, self.head.y))
                            notfound = False
                            break
                        case _:
                            notfound = True
            if notfound:
                match self.mov_dir:
                    case Directions.UP:
                        self.snake.insert(0, Point(self.head.x, self.head.y - self.BLOCKSIZE))
                    case Directions.DOWN:
                        self.snake.insert(0, Point(self.head.x, self.head.y + self.BLOCKSIZE))
                    case Directions.LEFT:
                        self.snake.insert(0, Point(self.head.x - self.BLOCKSIZE, self.head.y))
                    case Directions.RIGHT:
                        self.snake.insert(0, Point(self.head.x + self.BLOCKSIZE, self.head.y))
                            #Add code to go the same direction as before
            self.head = self.snake[0]
            self.snake.pop(-1)
            print(self.snake)
            self.create_environment()
            time.sleep(0.5)

    
    def create_environment(self):
        self.display.fill(BLACK)
        for block in self.snake:
            pygame.draw.rect(self.display, RED, pygame.Rect(block.x, block.y, self.BLOCKSIZE, self.BLOCKSIZE))
            
        pygame.draw.rect(self.display, BLUE, pygame.Rect(self.food.x, self.food.y, self.BLOCKSIZE, self.BLOCKSIZE))
        pygame.display.flip()

    def move(self):
        pass

if __name__ == "__main__":
    snake = Snake()
    snake.run()