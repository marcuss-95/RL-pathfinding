#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 26 14:11:12 2020

@author: marcus
"""
import numpy as np



class Robot():
    def __init__(self, R, gamma=0.8, lr=.2):
        self.state = np.nan
        self.Q = np.zeros((6,6))
        self.R = R
        self.gamma = gamma
        self.lr = lr
        
    def move(self):
        # print(self.R[self.state])
        states = self.R[self.state]
        possible_actions = np.where(states!=-1)[0]
        action = np.random.choice(possible_actions)
        self.Q[self.state,action] += self.lr*(self.R[self.state,action]+self.gamma*np.max(self.Q[action])-self.Q[self.state,action])
        self.state = action
        
    def find_path(self, start):
        path = []
        self.state = start
        while(1):
            path.append(self.state)
            if self.state == 5:
                break
            actions = self.Q[self.state]
            # possible_actions = np.where(states!=0)[0]
            action = np.argmax(actions)
            if action.size !=1:
                 if 5 in possible_actions:
                     path.append(5)
                     action = 5
                 else: action = np.random.choice(action)
            self.state = action
         
        print(path)
        
class Environment():
    def __init__(self):
        self.R = np.zeros((6,6))
        
        self.R[0,(0,1,2,3,5)] = -1
        self.R[1,(0,1,2,4)] = -1
        self.R[2,(0,1,2,4,5)] = -1
        self.R[3,(0,3,5)] = -1
        self.R[4,(1,2,4,5)] = -1
        self.R[5,(0,2,3)] = -1
        
        self.R[1,5] = 100
        self.R[4,5] = 100
        self.R[5,5] = 100
        
        self.agent = Robot(self.R)
        self.agent.state = np.random.randint(0,6)
        
    def learn(self, num_episodes):
        for i in range(0,num_episodes):
            self.agent.state = np.random.randint(0,6)
            while(1):
                self.agent.move()
                if self.agent.state == 5:
                    break
    
    def normalize(self):
        np.round(self.agent.Q)
        self.agent.Q /= np.max(self.agent.Q)
        
env = Environment()

env.learn(1000)
env.normalize()

env.agent.find_path(2)