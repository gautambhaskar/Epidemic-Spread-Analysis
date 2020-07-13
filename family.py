import networkx as nx
import matplotlib.pyplot as plt
import EoN
import random
import math
import numpy as np
import csv
import ast




percent = 0.0
families=int(input("# families: "))
tau =float(input('Transmission Rate: '))            #transmission rate
gamma =float(input('Recovery Rate: '))             #recovery rate
rho = float(input('Initial Percent Infected '))
N=int(input("Members in each family? "))


G=nx.Graph()
J=nx.complete_graph(N*families)
print('creating graph')
for x in range(families):
     H=nx.complete_graph(N)
     G=nx.disjoint_union(H,G)
print('creating edgelists')
edges=list(G.edges(nbunch=None, data=False, default=None))
edges1=list(J.edges(nbunch=None, data=False, default=None))
maximum=(families*N)
for i in range(len(edges)):
    edges[i]=str(edges[i])

for i in range(len(edges1)):
    edges1[i]=str(edges1[i])
print('creating final edge list')
main_list = np.setdiff1d(edges1,edges)
edges2=[]
for i in main_list:
    edges2.append(ast.literal_eval(i))




run_iters = 1
with open('family.csv', mode='w') as f:
     writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
     writer.writerow(['Max Infected', 'Total Infected', 'Time to Peak', 'Total Population', 'Percent total infected', 'Percent max infected', 'Percent edges connected'])

     while percent <= 1:
          stats = [0.0,0.0,0.0,0.0,0.0, 0.0]

          
          for i in range(run_iters):

               L=edges2
               edges3=[]
               a=percent
               a = math.floor(a*maximum) # NOTE: Shouldn't this use len(L) instead of maximum????
               
               for x in range(a):
                    edge=random.choice(L)
                    G.add_edge(edge[0],edge[1])
                    edges3.append(edge)
                    L.remove(edge)
                    
               tmax = 40
               print('finished')
           
               SIR=EoN.fast_SIR(G, tau, gamma, initial_infecteds=random.sample(list(range(maximum)), math.floor(rho*maximum)), tmax = tmax,return_full_data=True)
               SIR.display(time=5)
               plt.show()

               for c in edges3:
                    G.remove_edge(c[0],c[1])

                    
                
              
               t,d=SIR.summary()
               max_infected= max(d['I'])
               total_infected=max(d['R'])
               time_to_peak=t[np.where(d['I']==max(d['I']))]
               print('max infected= ',max_infected)
               print('total infected= ',total_infected)
               print('time to peak= ',time_to_peak)
               print('total population_= ', maximum)
               print('percent infected_= ', 100*total_infected/maximum,'%')
               stats[0] += max_infected/run_iters
               stats[1] += total_infected/run_iters
               stats[2] += time_to_peak[0]/run_iters
               stats[3] = maximum
               stats[4] += 100*total_infected/(maximum*run_iters)
               stats[5] += 100*max_infected/(maximum*run_iters)
               
          print('-----------------------------------------')
          #
          writer.writerow([str(stats[0]), str(stats[1]), str(stats[2]), str(stats[3]), str(stats[4]), str(stats[5]), str(percent)])
          print('Row written')
          percent += 0.2
          
