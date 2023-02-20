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




class Snake:
    
    def __init__(self, block_size=20, block_x_length=32, block_y_length=20) -> None:
        self.WINDOWSIZE = (block_x_length * block_size, block_y_length * block_size)
        self.blocks_x = block_x_length
        self.blocks_y = block_y_length
        self.BLOCKSIZE = block_size
        
        self.display = pygame.display.set_mode(self.WINDOWSIZE)

        self.head = Point(self.WINDOWSIZE[0] / 2, self.WINDOWSIZE[1] / 2)
        self.snake = [self.head, Point(self.head.x - self.BLOCKSIZE, self.head.y), Point(self.head.x  - 2 * self.BLOCKSIZE, self.head.y)]
        self.mov_dir = pygame.K_RIGHT
        self.place_food()
        
    def place_food(self):
        self.food = Point(random.randint(0, self.blocks_x) * self.BLOCKSIZE, random.randint(0, self.blocks_y) * self.BLOCKSIZE)
        
    def run(self):
        notfound = True
        while True:
            new_point = None
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit(0)
                if event.type == pygame.KEYDOWN:
                    val = event.dict.get("key")
                    new_point = self.get_new_point(val)
                    if new_point != None:
                        break

            if new_point == None:
                new_point = self.get_new_point(self.mov_dir)

            self.snake.insert(0, new_point)
            self.head = new_point
            self.is_food()
            if self.is_collision(self.head):
                print("You lost!")
                quit(0)
            self.snake.pop(-1)
            self.create_environment()
            time.sleep(0.2)

    
    def create_environment(self):
        self.display.fill(BLACK)
        for block in self.snake:
            pygame.draw.rect(self.display, RED, pygame.Rect(block.x, block.y, self.BLOCKSIZE, self.BLOCKSIZE))
            
        pygame.draw.rect(self.display, BLUE, pygame.Rect(self.food.x, self.food.y, self.BLOCKSIZE, self.BLOCKSIZE))
        pygame.display.flip()


    def is_collision(self, point):
        return point in self.snake[1:] or point.x >= self.WINDOWSIZE[0] \
           or point.x < 0 or point.y >= self.WINDOWSIZE[1] or point.y < 0

    def is_food(self):
        if self.head == self.food:
            if self.is_collision(Point(self.snake[-1].x - self.BLOCKSIZE, self.snake[-1].y)):
                new_point = Point(self.snake[-1].x, self.snake[-1].y - self.BLOCKSIZE)
            else:
                new_point = Point(self.snake[-1].x - self.BLOCKSIZE, self.snake[-1].y)
            self.snake.append(new_point)
            self.place_food()

    def get_new_point(self, val):
        if val == pygame.K_DOWN:
            self.mov_dir = pygame.K_DOWN
            return Point(self.head.x, self.head.y + self.BLOCKSIZE)
        elif val == pygame.K_UP:
            self.mov_dir = pygame.K_UP
            return Point(self.head.x, self.head.y - self.BLOCKSIZE)
        elif val == pygame.K_LEFT:
            self.mov_dir = pygame.K_LEFT
            return Point(self.head.x - self.BLOCKSIZE, self.head.y)
        elif val == pygame.K_RIGHT:
            self.mov_dir = pygame.K_RIGHT
            return Point(self.head.x + self.BLOCKSIZE, self.head.y)
        else:
            return None

if __name__ == "__main__":
    snake = Snake()
    snake.run()