import networkx as nx
import matplotlib.pyplot as plt
import EoN
import random
import math
import numpy as np
families=int(input("How many families? "))
N=int(input("Members in each family? "))

G=nx.Graph()
for x in range(families):
     H=nx.complete_graph(N)
     G=nx.disjoint_union(H,G)

     edges=[]
for line in nx.generate_edgelist(G, data=False):
     a=int(line[:(line.find(" "))])
     b=int(line[(line.find(" ")+1):])
     c=[a,b]
     edges.append(c)



L=[]
maximum=(families*N)

for x in range (maximum):
     for b in range(maximum):
          n=[b,x]
          L.append(n)
          
for x in edges:
     L.remove(x)


a=int(input("percent connected? "))## fix the extra edge thing
a=math.floor(maximum*a/100) # NOTE: Shouldn't this use len(L) instead of maximum????
for x in range(a):
     edge=random.choice(L)
     G.add_edge(edge[0],edge[1])
     L.remove(edge)
tmax = 20
#iterations = 5  #run 5 simulations
tau =float(input('what is the transmition rate? '))            #transmission rate
gamma =float(input('what is the recovery rate? '))             #recovery rate
rho = float(input('what percent is radomly initialized? '))

SIR=EoN.fast_SIR(G, tau, gamma, rho=rho, tmax = tmax,return_full_data=True)
#SIR.animate()
t,d=SIR.summary()
max_infected= max(d['I'])
total_infected=max(d['R'])
time_to_peak=t[np.where(d['I']==max(d['I']))]
print('max infected= ',max_infected)
print('total infected= ',total_infected)
print('time to peak= ',time_to_peak)
print('total population_= ', maximum)
print('percent infected_= ', total_infected/maximum,'%')

#plt.show()


