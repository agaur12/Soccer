import numpy as np
import random
import math
import gym
from gym import spaces


class GridEnvironment(gym.Env):

    def __init__(self, size_x: int, size_y: int, rand_goal: bool = False, rand_start: bool = False):
        super(GridEnvironment, self).__init__()
        self.actions = ["up", "right", "down", "left"]
        self.rand_start = rand_start
        self.rand_goal = rand_goal
        self.max_x = size_x - 1
        self.max_y = size_y - 1
        self.done = False
        self.episode_length = 0
        self.distances = []
        if rand_start:
            self.init_x, self.init_y = random.randint(1, self.max_x), random.randint(1, self.max_x)
            self.x, self.y = self.init_x, self.init_y
        else:
            self.x, self.y = 0, 0
        if rand_goal:
            self.goal = [random.randint(1, self.max_x), random.randint(1, self.max_x)]
            while self.goal == [self.x, self.y]:
                self.goal = [random.randint(1, self.max_x), random.randint(1, self.max_x)]
        else:
            self.goal = [self.max_x, self.max_y]
        self.state = [self.x, self.y]
        self.action_space = spaces.Discrete(len(self.actions))
        self.observation_space = spaces.Box(low=0, high=max(self.max_x, self.max_y), shape=(2,), dtype=np.float32)

    def reset(self):
        if self.rand_start:
            self.x, self.y = self.init_x, self.init_y
        else:
            self.x, self.y = 0, 0
        if self.rand_goal:
            self.goal = [random.randint(1, self.max_x), random.randint(1, self.max_x)]
        #self.x, self.y = random.randint(1, self.max_x), random.randint(1, self.max_x)
        """
        self.goal = [random.randint(1, self.max_x), random.randint(1, self.max_x)]
        while self.goal == [self.x, self.y]:
            self.goal = [random.randint(1, self.max_x), random.randint(1, self.max_x)]
        """
        self.done = False
        self.episode_length = 0
        self.state = [self.x, self.y]
        return np.array(self.state)

    def step(self, action):
        if self.state == self.goal or self.episode_length > 200:
            self.done = True

        self.action = self.actions[action]
        self.distances.append(math.hypot(self.state[0] - self.goal[0], self.state[1] - self.goal[1]))
        self.state = self.take_action()
        self.reward = self.get_reward()
        self.episode_length += 1

        if self.state == self.goal or self.episode_length > 200:
            self.done = True
        return self.state, self.reward, self.done

    def get_reward(self):
        if self.episode_length > 200:
            reward = -1
        elif self.state == self.goal:
            reward = 10
        else:
            reward = -0.01
            reward += (self.distances[-1] - math.hypot(self.state[0] - self.goal[0], self.state[1] - self.goal[1])) / 1000
        return reward

    def take_action(self):
        if (self.action == "left" and self.x == 0) or (self.action == "right" and self.x == self.max_x):
            self.x = self.x
            self.episode_length -= 1
        elif self.action == "left":
            self.x -= 1
        elif self.action == "right":
            self.x += 1
        else:
            self.x = self.x
        if (self.action == "down" and self.y == 0) or (self.action == "up" and self.y == self.max_x):
            self.y = self.y
            self.episode_length -= 1
        elif self.action == "down":
            self.y -= 1
        elif self.action == "up":
            self.y += 1
        else:
            self.y = self.y

        return [self.x, self.y]