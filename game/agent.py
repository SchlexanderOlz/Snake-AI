from snake import Snake, Point, DIRECTIONS, SPEED
import torch
import random
from collections import deque
from model import Liner_QNet, QTrainer
import numpy as np
import pygame
import plot
import time

MAX_MEMORY = 100000
BATCH_SIZE = 800
LR = 0.002 # --> 0.002 works well
GENERAL_RANDOMNESS = 500
TRAIN_FOR = 1300

GEN_SPEED = 0.05


class Agent:
    
    def __init__(self, game:Snake) -> None:
        self.n_games = 0
        self.randomness = 0
        self.gamma = 0.8
        self.memory = deque(maxlen=MAX_MEMORY) #--> Pops left when to big
        self.game = game
        self.model = Liner_QNet(11 + (self.game.blocks_x * self.game.blocks_y), 256, 3)
        self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)
    
    def get_state(self):
        #Get threat nearby
        #Get direction of food
        dir_l = self.game.mov_dir == pygame.K_LEFT
        dir_r = self.game.mov_dir == pygame.K_RIGHT
        dir_u = self.game.mov_dir == pygame.K_UP
        dir_d = self.game.mov_dir == pygame.K_DOWN
        return np.array([
            
            #Check for danger ahead
            self.game.is_collision(self.game.get_new_point(self.game.mov_dir)),
            #Check for danger on left side
            self.game.is_collision(self.game.get_new_point(DIRECTIONS[(DIRECTIONS.index(self.game.mov_dir) - 1) % 4])),
            #Chekc for danger on right side
            self.game.is_collision(self.game.get_new_point(DIRECTIONS[(DIRECTIONS.index(self.game.mov_dir) + 1) % 4])),
            
            dir_l,
            dir_r,
            dir_u,
            dir_d,
            
            self.game.food.x < self.game.head.x,
            self.game.food.x > self.game.head.x,
            self.game.food.y < self.game.head.y,
            self.game.food.y > self.game.head.y,
            
            *self.game.get_all_pos()
        ], dtype=int)
    
    
    def remember(self, state, action, reward, next_state, end):
        self.memory.append((state, action, reward, next_state, end)) # Popleft if max memory
    
    
    def train_long_mem(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE) # List of tuples
        else:
            mini_sample = self.memory
            
        states, actions, rewards, next_states, end = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, end)
    
    
    def train_short_mem(self, state, action, reward, next_state, end):
        self.trainer.train_step(state, action, reward, next_state, end)
        

    def get_action(self, state):
        self.randomness = GENERAL_RANDOMNESS - self.n_games
        final_move = [0, 0, 0]
        if random.randint(0, 200) < self.randomness:
            move = random.randint(0, 2)
            final_move[move] = 1
        else:
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state0)
            move = torch.argmax(prediction).item()
            final_move[move] = 1
            
        return final_move


    def will_close_loop(self):
        #TODO --> Write a method to check if the snake will loop inside of itself
        #Write your programm here
        pass


def train():
    plot_scores = []
    avg = []
    total_score = 0
    record = 0
    game = Snake()
    agent = Agent(game)
    while True:
        state_old = agent.get_state()
        last_move = agent.get_action(state_old)
        if agent.n_games < TRAIN_FOR:
            reward, score, has_ended = game.run(last_move, graphics=False)
        else:
            reward, score, has_ended = game.run(last_move)
        state_new = agent.get_state()
        agent.train_short_mem(state_old, last_move, reward, state_new, has_ended)
        agent.remember(state_old, last_move, reward, state_new, has_ended)
        
        if has_ended:
            agent.train_long_mem()
            agent.n_games += 1
            
            if score > record:
                record = score
            print("Game: {}, Score: {}, Record: {}".format(agent.n_games, score, record))
            
            plot_scores.append(score)
            avg.append(np.mean(plot_scores))
            plot.plot(plot_scores, avg)

            
if __name__ == "__main__":
    train()