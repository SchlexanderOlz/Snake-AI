import pygame
import torch
import matplotlib
from collections import namedtuple
import random
from enum import Enum


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
        self.WINDOWSIZE = tuple(block_x_length * block_size, block_y_length * block_size)
        self.blocks_x = block_x_length
        self.blocks_y = block_y_length
        self.BLOCKSIZE = block_size
        
        self.display = pygame.display.set_mode(self.WINDOWSIZE)

        self.head = Point(self.WINDOWSIZE[0] / 2, self.WINDOWSIZE[1] / 2)
        self.snake = [self.head, Point(self.head.x - self.BLOCKSIZE), Point(self.head.x  - 2 * self.BLOCKSIZE)]
        self.mov_dir = Directions.RIGHT
        self.place_food()
        
    def place_food(self):
        self.food = Point(random.randint(0, self.blocks_x), random.randint(0, self.blocks_y))
        
    def run(self):

        while True:
            for event in pygame.event.get():
                match event:
                    case pygame.QUIT:
                        pygame.quit()
                        quit(0)
                    case pygame.K_UP:
                        self.head.y += self.BLOCKSIZE
                    case pygame.K_DOWN:
                        self.head.y -= self.BLOCKSIZE
                    case pygame.K_LEFT:
                        self.head.x -= self.BLOCKSIZE
                    case pygame.K_RIGHT:
                        self.head.x += self.BLOCKSIZE
                    case _:
                        pass
                        #Add code to go the same direction as before
                self.create_environment()
    
    def create_environment(self):
        self.display.fill(BLACK)
        for block in self.snake:
            pygame.draw.rect(self.display, RED, pygame.Rect(block.x, block.y, self.BLOCKSIZE, self.BLOCKSIZE))
            
        pygame.draw.rect(self.display, BLUE, pygame.Rect(self.food.x, self.food.y, self.BLOCKSIZE, self.BLOCKSIZE))

