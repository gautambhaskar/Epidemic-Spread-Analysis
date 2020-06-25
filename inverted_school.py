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
    size=math.floor(int(input("What is the average class size? ")))
    periods=int(input("how many periods? "))
    students=(size*classes)
    tau =float(input('what is the transmition rate? '))            #transmission rate
    gamma =float(input('what is the recovery rate? '))             #recovery rate
    rho = float(input('what percent is radomly initialized? '))
    days=int(input('how many days to run for '))
    counter=0
    tmin=0
    tmax=2

    
    max_infected_list=[]
    peak_time_list=[]

    teachers=[]
    students_list=[]

    #creates graph of just students#
    for x in range(classes):
        H=nx.complete_graph(size)
        G=nx.disjoint_union(H,G)
        


    bottom=0
    top=size
        
    time=0
    counter=0
    var_list=[]

    #creates a list of nodes for each class for just students#
    for x in range(classes):

        var_list.append("class_"+str(x))

    for x in var_list:
        globals()[x]=[]
        for b in range(bottom,top):
            globals()[x].append(b)
        bottom=top
        top=top+size

    infected=[]
    recovered=[]
    #this is where the 'school day' starts#
    for period in range(periods*days):
        
        #creates list of teachers#
        for x in range(students,students+classes):
            teachers.append(x)
        
        new_edges=[]
        #adds edges to the graph between teachers and students#
        if counter==0:
            
            for x in var_list:
                node=random.choice(teachers)
                G.add_node(node)
                for h in globals()[x]:
                    G.add_edge(node,h)
                    edge=[node,h]
                    new_edges.append(edge)
                teachers.remove(node)
        else:
            for x in var_list:
                node=random.choice(teachers)
                for h in globals()[x]:
                    G.add_edge(node,h)
                    edge=[node,h]
                    new_edges.append(edge)
                teachers.remove(node)
            





        if (period/periods==int(period/periods)) and (counter!=0):
            
            SIR=EoN.fast_SIR(G, 0, gamma, tmin=tmin, tmax = 32, initial_infecteds=infected, initial_recovereds=recovered, return_full_data=True)
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






        #for the first iteration, the infecteds are distributed randomly. The rest of the periods depend on the previous infected and recovered lists.
        if counter==0:
            SIR=EoN.fast_SIR(G, tau, gamma, rho=rho, tmax = tmax,return_full_data=True)
        else:
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
            if node_stats[i]=='R':
                recovered.append(i)
                
        #gets the metrics needed#
        max_infected_list.append(max(d['I']))
        
        peak_time_list.append(t[np.where(d['I']==max(d['I']))]+time)
        time=time+2


        #deletes edges between teachers and students to get ready for next period/switch#
        new_edges.sort()
        edges2 = list(new_edges for new_edges,_ in itertools.groupby(new_edges))
        for x in edges2:
            G.remove_edge(x[0],x[1])


    #gets all the disered metrics#
    total_infected=len(set(recovered))+len(set(final_infected))
    max_infected=max(max_infected_list)
    peak_time=peak_time_list[max_infected_list.index(max_infected)]
    print('total_infected= ',total_infected)
    print('max infected= ',max_infected)
    print('peak time= ',peak_time)
    print('population size= ', students+classes)
    print('percent infected= ',100*total_infected/(students+classes),'%')
    
    
  
