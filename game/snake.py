import pygame
from collections import namedtuple
import random
import time
import numpy


pygame.init()
Point = namedtuple("Point", "x, y")
Direction = namedtuple("Direction", "straight, left, right")

BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

SPEED = 0.1

DIRECTIONS = [pygame.K_RIGHT, pygame.K_DOWN, pygame.K_LEFT, pygame.K_UP]


class Snake:
    
    def __init__(self, block_size=20, block_x_length=32, block_y_length=20, agent_controlled=True) -> None:
        self.WINDOWSIZE = (block_x_length * block_size, block_y_length * block_size)
        self.blocks_x = block_x_length
        self.blocks_y = block_y_length
        self.BLOCKSIZE = block_size
        
        self.display = pygame.display.set_mode(self.WINDOWSIZE)
        pygame.display.set_caption("Snake")
        
        self.is_agent_controlled = agent_controlled
        if self.is_agent_controlled:
            self.reward = 0

        self.reset()
        
    def reset(self):
        self.head = Point(self.WINDOWSIZE[0] / 2, self.WINDOWSIZE[1] / 2)
        self.snake = [self.head, Point(self.head.x - self.BLOCKSIZE, self.head.y), Point(self.head.x  - 2 * self.BLOCKSIZE, self.head.y)]
        self.mov_dir = pygame.K_RIGHT
        self.frame_iteration = 0
        self.score = 0
        self.place_food()


    def place_food(self):
        self.food = Point(random.randint(0, self.blocks_x) * self.BLOCKSIZE, random.randint(0, self.blocks_y) * self.BLOCKSIZE)
        if self.is_collision(self.food):
            self.place_food()

        
    def run(self, move_dir = None):
        # for move_dir --> [straigth, left, right]
        time.sleep(SPEED)
        end = False
        self.frame_iteration += 1
        new_point = None
        if not self.is_agent_controlled:
            self.frame_iteration += 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit(0)
                if event.type == pygame.KEYDOWN:
                    val = event.dict.get("key")
                    new_point = self.get_new_point(val)
                    if new_point != None:
                        break
        else:
            if numpy.array_equal(move_dir, Direction(False, True, False)):
                self.mov_dir = DIRECTIONS[(DIRECTIONS.index(self.mov_dir) + 1) % 4]
            elif numpy.array_equal(move_dir, Direction(True, False, False)):
                self.mov_dir = DIRECTIONS[(DIRECTIONS.index(self.mov_dir) - 1) % 4]

        if new_point == None:
            new_point = self.get_new_point(self.mov_dir)

        self.snake.insert(0, new_point)
        self.head = new_point
        is_food = self.handle_food()
        if self.is_collision(self.head) or self.frame_iteration > 100 * len(self.snake):
            print("You lost!")
            print("Score: {}".format(self.score))
            self.reset()
            self.reward = -10
            end = True
        else:
            if not is_food:
                self.reward = 0
            self.snake.pop(-1)
        self.create_environment()
        return self.reward, self.score, end

    
    def create_environment(self):
        self.display.fill(BLACK)
        for block in self.snake:
            pygame.draw.rect(self.display, RED, pygame.Rect(block.x, block.y, self.BLOCKSIZE, self.BLOCKSIZE))
            
        pygame.draw.rect(self.display, BLUE, pygame.Rect(self.food.x, self.food.y, self.BLOCKSIZE, self.BLOCKSIZE))
        pygame.display.flip()


    def is_collision(self, point):
        return point in self.snake[1:] or point.x >= self.WINDOWSIZE[0] \
           or point.x < 0 or point.y >= self.WINDOWSIZE[1] or point.y < 0

    def handle_food(self):
        if self.head == self.food:
            if self.is_collision(Point(self.snake[-1].x - self.BLOCKSIZE, self.snake[-1].y)):
                new_point = Point(self.snake[-1].x, self.snake[-1].y - self.BLOCKSIZE)
            else:
                new_point = Point(self.snake[-1].x - self.BLOCKSIZE, self.snake[-1].y)
            self.snake.append(new_point)
            self.place_food()
            self.score += 1
            self.reward = 10
            return True
        return False

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

#if __name__ == "__main__":
    #snake = Snake()
  #  while True:
     #   print(snake.run([0, 1, 0]))