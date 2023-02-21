from snake import Snake, Point, DIRECTIONS
import torch
import numpy
import random
from collections import deque
import matplotlib
import pygame

MAX_MEMORY = 100000
BATCH_SIZE = 1000
LR = 0.01

class Agent:
    
    def __init__(self, game:Snake) -> None:
        self.n_games = 0
        self.randomness = 0
        self.gamma = 0
        self.memory = deque(maxlen=MAX_MEMORY) #--> Pops left when to big
        self.game = game
        self.model = None #TODO
        self.trainer = None #TODO
    
    def get_state(self):
        #Get threat nearby
        #Get direction of food
        return [
            #Check for danger ahead
            [
            self.game.is_collision(self.game.get_new_point(self.game.mov_dir)),
            
            #Check for danger on left side
            self.game.is_collision(self.game.get_new_point(DIRECTIONS[DIRECTIONS.index(self.game.mov_dir) - 1])),
            
            #Chekc for danger on right side
            self.game.is_collision(self.game.get_new_point(DIRECTIONS[DIRECTIONS.index(self.game.mov_dir) + 1]))
            ],
            self.game.mov_dir,
            [
                self.game.food.x < self.game.head.x,
                self.game.food.x > self.game.head.x,
                self.game.food.y < self.game.head.y,
                self.game.food.y > self.game.head.y
            ]
        ]
    def remember(self, state, action, reward, next_state, end):
        self.memory.append((state, action, reward, next_state, end)) # Popleft if max memory
    def train_long_mem(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE) # List of tuples
        else:
            mini_sample = self.memory
            
        self.trainer.train_step(states, actions, rewards, next_states, end)
    def train_short_mem(self, state, action, reward, next_state, end):
        self.trainer.train_step(state, action, reward, next_state, end)
    def get_action(self, state):
        pass
    
def train():
    plot_scores = []
    avg = []
    total_score = 0
    record = 0
    game = Snake()
    agent = Agent(game)
    while True:
        state_old = agent.get_state(game)
        last_move = agent.get_action(state_old)
        reward, score, has_ended = game.run(last_move)
        state_new = agent.get_state(game)
        agent.train_short_mem(state_old, last_move, reward, state_new, has_ended)
        agent.remember(state_old, last_move, reward, state_new, has_ended)
        
        if has_ended:
            agent.train_long_mem()
            agent.n_games += 1
            
            if score > record:
                record = score
            print("Game: {}, Score: {}, Record: {}".format(agent.n_games, score, record))
            #TODO plotting
            
if __name__ == "__main__":
    train()