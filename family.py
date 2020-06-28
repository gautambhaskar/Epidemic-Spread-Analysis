import networkx as nx
import matplotlib.pyplot as plt
import EoN
import random
import math
import numpy as np
import csv





percent = 0.0
families=int(input("# families: "))
tau =float(input('Transmission Rate: '))            #transmission rate
gamma =float(input('Recovery Rate: '))             #recovery rate
rho = float(input('Initial Percent Infected '))
N=int(input("Members in each family? "))


G=nx.Graph()
J=nx.complete_graph(N*families)

for x in range(families):
     H=nx.complete_graph(N)
     G=nx.disjoint_union(H,G)

edges=list(G.edges(nbunch=None, data=False, default=None))
edges1=list(J.edges(nbunch=None, data=False, default=None))

               
               
               #for line in nx.generate_edgelist(G, data=False):
                #    a=int(line[:(line.find(" "))])
                 #   b=int(line[(line.find(" ")+1):])
                  #  c=[a,b]
                   # edges.append(c)

               #for line in nx.generate_edgelist(J, data=False):
                #    a=int(line[:(line.find(" "))])
                 #   b=int(line[(line.find(" ")+1):])
                  #  c=[a,b]
                   # edges1.append(c)


L=[]
maximum=(families*N)



edges2=np.setdiff1d(edges,edges1)





run_iters = 20
with open('family.csv', mode='w') as f:
     writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
     writer.writerow(['Max Infected', 'Total Infected', 'Time to Peak', 'Total Population', 'Percent total infected', 'Percent max infected', 'Percent edges connected'])

     while percent <= 1:
          stats = [0.0,0.0,0.0,0.0,0.0, 0.0]


          for i in range(run_iters):

               print('1')
               #for x in range (maximum):
                #    for b in range(maximum):
                 #        if ([b,x] in edges) or ([x,b] in edges):
                  #            continue
                   #      else:
                    #          n=[b,x]
                     #         L.append(n)

                         
                              
       
               L=edges2
               
               a=percent
               a = math.floor(a*len(L)) # NOTE: Shouldn't this use len(L) instead of maximum????
               for x in range(a):
                    edge=random.choice(L)
                    G.add_edge(edge[0],edge[1])
                    L.remove(edge)
               tmax = 40
               #iterations = 5  #run 5 simulations
          



               

               print('1')
               SIR=EoN.fast_SIR(G, tau, gamma, initial_infecteds=random.sample(list(range(maximum)), math.floor(rho*maximum)), tmax = tmax,return_full_data=True)
               print('1')
               #SIR.animate()
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
               #SIR.display(time=tmax)
               #plt.show()
          print('-----------------------------------------')
          #
          writer.writerow([str(stats[0]), str(stats[1]), str(stats[2]), str(stats[3]), str(stats[4]), str(stats[5]), str(percent)])
          print('Row written')
          percent += 0.01
          
