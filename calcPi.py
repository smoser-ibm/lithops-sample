from time import time
from random import random
import logging
import sys
import os
from ipywidgets import IntProgress
import lithops
MAP_INSTANCES = 50
class EstimatePI:
    randomize_per_map = 100000000
    def __init__(self):
        self.total_randomize_points = MAP_INSTANCES * self.randomize_per_map
    def __str__(self):
        return "Total Randomize Points: {:,}".format(self.randomize_per_map * MAP_INSTANCES)
    @staticmethod
    def predicate():
        x = random()
        y = random()
        return (x ** 2) + (y ** 2) <= 1
    def randomize_points(self, data):
        in_circle = 0
        for _ in range(self.randomize_per_map):
            in_circle += self.predicate()
        return float(in_circle / self.randomize_per_map)
    def process_in_circle_points(self, results):
        in_circle_percent = 0
        for map_result in results:
            in_circle_percent += map_result
        estimate_PI = float(4 * (in_circle_percent / MAP_INSTANCES))
        return estimate_PI
iterdata = [0] * MAP_INSTANCES
est_pi = EstimatePI()
print("Monte Carlo simulation for estimating PI spawing over {} IBM Code Engine".format(MAP_INSTANCES))
# obtain lithops executor
lt = lithops.FunctionExecutor(mode="serverless", backend='code_engine', runtime = 'ibmfunctions/lithops-ce-v385:233', remote_invoker = True)
#lt = lithops.FunctionExecutor()
# execute the code
t0 = time()
lt.map_reduce(est_pi.randomize_points, iterdata, est_pi.process_in_circle_points)
#get results
result = lt.get_result()
t1 = time()
print (t1-t0)
print(str(est_pi))
print("Estimation of Pi: ", result)
