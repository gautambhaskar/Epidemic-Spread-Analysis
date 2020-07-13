import networkx as nx
import matplotlib.pyplot as plt
import EoN as e
import random
import numpy as np
import math
import csv
from itertools import combinations

G = nx.complete_graph(5)
sim = e.fast_SIR(G, 0.1, 0.1, None, None, 0.4, return_full_data=True)
for i in range(5):
    data = sim.summary(nodelist=[i])
    print(data)