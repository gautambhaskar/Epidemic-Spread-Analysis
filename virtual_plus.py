import networkx as nx
import matplotlib.pyplot as plt
import EoN
import random
import math
import itertools
import numpy as np
from itertools import combinations
import csv
import ast

#statistics#
classes=int(input("How many classes? "))
size=int(input("What is the average class size? "))
periods=int(input("how many periods? "))
tau =float(input('what is the transmition rate? '))            #transmission rate
gamma =float(input('what is the recovery rate? '))             #recovery rate
rho = float(input('what percent is radomly initialized? '))
days=int(input('how many days to run for '))

run_iters = 10
with open('virtual_plus.csv', mode='w') as f:
    writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(['Max Infected', 'Total Infected', 'Time to Peak', 'Total Population', 'Percent total infected', 'Percent max infected', 'Percent edges connected'])
    percent = 0.0
    while percent <= 1:
        stats = [0.0,0.0,0.0,0.0,0.0, 0.0]
        for i in range(run_iters):

            plus_to_inperson=percent

            max_infected_list=[]
            peak_time_list=[]
            students=(size*classes)
            counter=0
            tmin=0
            tmax=1

            #intializes the graphs for each period
            A=nx.Graph()
            B=nx.Graph()
            C=nx.Graph()
            D=nx.Graph()
            E=nx.Graph()
            F=nx.Graph()
            G=nx.Graph()
            H=nx.Graph()
            
            #calculates the number of virtual plus people
            num_plus=plus_to_inperson*(students)
            num_virtual=num_plus
            #initializes a few lists for later use
            class_list=[]
            virtual_class_list=[]
            edges=[]
            class_sort=[]
            #puts the graphs in list to iterate through later
            alpha=[A,B,C,D,E,F,G,H]

            #makes the lists of the nodes for each group
            virtual_plus=list(range(int(students),int(num_virtual+students)))

            in_person=list(range(int(students)))
            #creates a combined list so we can add the isolated nodes later for the nodes which correspond to virtual plus students who are not at school for a particular period
            combined_list_students=in_person+virtual_plus
            
            #creats list of nodes where we will randomly choose nodes to assign to classes#
            #creates an arbitrary number of variables to assign lists of students in each class for each period#

            #initializes the list where the virtual plus nodes which will be present for each period are stored
            for j in range(len(alpha)):
                virtual_class_list.append([])
            #sorts the virtual plus students into which periods they will be present in
            #the virtual_class_list list will hold these values
            for j in virtual_plus:
                in_person_class=random.sample(alpha,3) #Make '3' a variable
                for class_x in (in_person_class):
                    inde=alpha.index(class_x)
                    virtual_class_list[inde].append(j)
                    
        
            #creats all the graphs for each period
            for x in alpha:
                for j in range(classes):
                    class_sort.append([])
                    class_list.append([])
                
                #puts the virtual plus people who already assained to this period into their classes
                
                for person in virtual_class_list[alpha.index(x)]:
                    sort=random.randrange(classes)
                    class_sort[sort].append(person)

                #creates the graph for each period
                for period in range(classes):
                    class_list[period]=random.sample(in_person,size)
                    comb_list=class_list[period]+class_sort[period]
                    
                    people_left_out_list=list(set(combined_list_students).difference(set(comb_list)))
                    
                    in_person=list(set(in_person).difference(set(class_list[period])))
                    edges.extend(list((combinations(comb_list,2))))
                    x.add_edges_from(list(edges))
                    x.add_nodes_from(people_left_out_list)
                
                edges=[]
                
                class_sort=[]
                class_list=[]
                in_person=list(range(int(students)))
                combined_list_students=in_person+virtual_plus

            for x in alpha:
                print(x.number_of_nodes())
                
            time=0

            infected=[]
            recovered=[]

            #this is where the 'school day' starts#
            for days in range(days):


                # goes through each period
                for graphs in alpha:
                

                    #for the first iteration, the infecteds are distributed randomly. The rest of the periods depend on the previous infected and recovered lists.#
                    if counter==0:
                        SIR=EoN.fast_SIR(graphs, tau, gamma, rho=rho, tmax = tmax,return_full_data=True)
                    elif counter!=0:
                        SIR=EoN.fast_SIR(graphs, tau, gamma, tmin=tmin, tmax = tmax, initial_infecteds=infected, initial_recovereds=recovered, return_full_data=True)
                        
                    counter=counter+1
                    t,d=SIR.summary()
                    
                    #nx.draw(G)
                    #plt.show()
                    
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
                    time=time+1

















                    
                SIR=EoN.fast_SIR(G, 0, gamma, tmin=tmin, tmax = 16, initial_infecteds=infected, initial_recovereds=recovered, return_full_data=True)
                t,d=SIR.summary()
                
                
                time += 16
                node_stats=list(SIR.get_statuses(nodelist=None, time=32).values())

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
                    


                

                







            total_infected=len(set(recovered))+len(set(final_infected))

            if (len(max_infected_list)>0):
                max_infected=max(max_infected_list)
            else:
                max_infected = 0
            students=students+num_plus
            if (max_infected != 0):
                peak_time=peak_time_list[max_infected_list.index(max_infected)]
            else:
                peak_time=0
            print('total_infected= ',total_infected)
            print('max infected= ',max_infected)
            print('peak time= ',peak_time)
            print('population size= ', students)
            print('percent infected= ',100*total_infected/students,'%')
            total_pop = students
            stats[0] = total_pop
            stats[1] += max_infected/run_iters
            print(stats[1])
            stats[2] += total_infected/run_iters
            stats[3] += peak_time[0]/run_iters
            stats[4] += (100*max_infected/total_pop)/run_iters
            stats[5] += ((100*total_infected)/total_pop)/run_iters

        print("---------------")
        print(" ")
        print("Total Population: " + str(stats[0]))
        print("Max # infected at a time: " + str(stats[1]))
        print("Total # infected: " + str(stats[2]))
        print("Time to peak: " + str(stats[3]))
        print("Max percent infected at a time: " + str(stats[4]) + "%")
        print("Chance of infection: " + str(stats[5]) + "%")
        print(" ")
        writer.writerow([str(stats[0]), str(stats[1]), str(stats[2]), str(stats[3]), str(stats[4]), str(stats[5]), str(percent)])
        print('Row written')
        percent += 0.2
