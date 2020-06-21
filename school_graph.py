import networkx as nx
import matplotlib.pyplot as plt
import EoN
import random
import math
import itertools
import numpy as np
while(True):
    G=nx.Graph()
    #statistics#
    classes=int(input("How many classes? "))
    size=int(input("What is the average class size? "))
    periods=int(input("how many periods? "))
    students=(size*classes)
    tau =float(input('what is the transmition rate? '))            #transmission rate
    gamma =float(input('what is the recovery rate? '))             #recovery rate
    rho = float(input('what percent is radomly initialized? '))
    counter=0
    tmin=0
    tmax=2

    
    max_infected_list=[]
    peak_time_list=[]


    #creats node for each student in the school#
    for x in range(students):
        G.add_node(x)
    time=0

    infected=[]
    recovered=[]

    #this is where the 'school day' starts#
    for periods in range(periods):
        L=[]
        var_list=[]



        #creats list of nodes where we will randomly choose nodes to assign to classes#
        for x in range(students):
            L.append(x)
        #creates an arbitrary number of variables to assign lists of students in each class for each period#
        for x in range(classes):
            var_list.append("class_"+str(x))

        
        #Creats the classes for each period where each student is randomly assigned#
        for x in var_list:
            globals()[x]=[]
            for b in range(size):
                node=random.choice(L)
                globals()[x].append(node)
                L.remove(node)
            


        #adds edges to create a complete graph within each new class#
        edges=[]
        for x in var_list:
            for b in globals()[x]:
                for y in globals()[x]:
                    G.add_edge(b,y)
                    edges.append([b,y])
        

        #for the first iteration, the infecteds are distributed randomly. The rest of the periods depend on the previous infected and recovered lists.#
        if counter==0:
            SIR=EoN.fast_SIR(G, tau, gamma, rho=rho, tmax = tmax,return_full_data=True)
        elif counter!=0:
            SIR=EoN.fast_SIR(G, tau, gamma, tmin=tmin, tmax = tmax, initial_infecteds=infected, initial_recovereds=recovered, return_full_data=True)
            
        counter=counter+1
        t,d=SIR.summary()
        
        
        
        node_stats=list(SIR.get_statuses(nodelist=None, time=tmax).values())

        #creates list of infecteds and recoverds after each iteration to feed into the next#
        final_infected=[]
        for i in range(len(node_stats)):
            if node_stats[i]=='I':
                infected.append(i)
                final_infected.append(i)
            elif node_stats[i]=='R':
                recovered.append(i)
        

        max_infected_list.append(max(d['I']))

        
        time_max=t[np.where(d['I']==max(d['I']))]+time

        peak_time_list.append(time_max)
        time=time+2
        #removes edges from G to get ready for next period where the edges will be completely different#
        edges1=[]
        edges2=[]
        for x in edges:
            if (x[0]==x[1]):
                continue
            elif (x[0]>x[1]):
                edges1.append([x[1],x[0]])
            else:
                edges1.append(x)
        
        edges1.sort()
        edges2 = list(edges1 for edges1,_ in itertools.groupby(edges1))
        #nx.draw(G)
        #plt.show()
        for x in edges2:
            G.remove_edge(x[0],x[1])
                        
    #gets all the disered metrics#
    total_infected=len(set(recovered))+len(set(final_infected))
    

    max_infected=max(max_infected_list)

    peak_time=peak_time_list[max_infected_list.index(max_infected)]
    print('total_infected= ',total_infected)
    print('max infected= ',max_infected)
    print('peak time= ',peak_time)
    print('population size= ', students)
    print('percent infected= ',100*total_infected/students,'%')
    
    
    
    
