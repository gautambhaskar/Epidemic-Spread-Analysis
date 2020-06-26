import networkx as nx
import matplotlib.pyplot as plt
import EoN as e
import random
import math
import itertools
import numpy as np
from itertools import chain
import csv

percent = 1
run_iters = 2

G=nx.Graph()
#Input Values
class_number=int(input("How many classes at a time? "))
period_number = int(input("How many periods per day? "))
size=math.floor(float(input("What is the average class size? ")))
group_number = percent
iterations = int(input("How many times should we iterate? ")) # Number of times each group of students runs on the model
students=list(range(size*class_number*group_number))
tau = float(input("Transmission Rate:  "))          #transmission rate
gamma = float(input("Recovery Rate: "))    #recovery rate
rho = float(input("Percentage of initial pop. infected: "))       #initial percent infected
time_reading = 1 # Interval of time sim is run for during each period

with open('school_percent.csv', mode='w') as f:
    writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(['Total Population', 'Max Infected', 'Total Infected', 'Time to Peak', 'Percent max infected', 'Percent total infected', 'Number of Groups'])
    while percent < 10:
        stats = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        for i in range(run_iters):
                    
            # Initializing Statistics
            iter_num = 0 # Used for iterating through each set of days
            groups = [] # Used to assign students to one of the day-specific groups
            max_infected = 0 
            peak_infected = 0
            time_to_peak = 0
            total_pop = size*class_number*group_number
            time_completed = 0
            infected = []
            recovered = []
            started = False


            # Creating the initial groups and classes
            for i in range(group_number):
                groups.append([]) #Creating data structure to hold nodes of each group

            #Running the simulation and changing classes
            while iter_num < iterations:
                for day in range(group_number): # Iterating through each group-specific day. 

                    print("--------- Day " + str((day+1)+(group_number*iter_num)) + "-----------")
                    print("Group " + str(day + 1) + " at school today")
                    #Iterating through each class period of the day
                    for period in range(period_number):
                        G.clear()
                        G.add_nodes_from(students)
                        groups[day].clear()
                        #Adding new edges to graph
                        group_students = list(students[(day*class_number*size):((day+1)*class_number*size)]) # Holder of nodes of the group being considered.
                        for class_x in range(class_number): # Random classes are assigned 
                            new_class = random.sample(group_students, size)

                            #Clearing and editing class selections

                            groups[day].append(list(new_class))
                            group_students = list(set(group_students).difference(set(new_class))) # Removes nodes, as they are added to classes to prevent node being present in multiple classes.
                            # Creates complete graph for each class
                            for student_1 in groups[day][class_x]:
                                for student_2 in groups[day][class_x]:
                                    G.add_edge(student_1, student_2)
                    
                        # Running the simulation
                        if started == False:
                            started = True
                            sim = e.fast_SIR(G, tau, gamma, rho=rho, initial_recovereds = recovered, return_full_data=True, tmax=time_reading)

                        else:
                            sim = e.fast_SIR(G, tau, gamma, initial_infecteds = infected, initial_recovereds = recovered, return_full_data=True, tmax=time_reading)

                        # Runs simulation
                        # Retrieves node statuses as given time of 'time_reading'
                        statuses = list(sim.get_statuses(time=time_reading).values())
                        #Clears all previous infected and retrieved data so as to accept new data from the simulation
                        infected.clear()
                        recovered.clear()
                        # Simple statement used to hold a time value, used to calculate time to peak and so on.
                        time_completed += time_reading

                        #Storing infected and recovered node info from the simulation 
                        for j in range(len(statuses)):
                            if statuses[j]=='I':
                                infected.append(j)
                            if statuses[j]=='R':
                                recovered.append(j)
                        
                        # Getting the peak value
                        t, D = sim.summary()

                        # If the max of the sliced list from the array is greater than the max_infected value
                        # (max number of ppl infected at a particular time so far), then the max_infected is
                        #  changed to this value.
                        local_max = np.amax(D['I'])
                        if local_max > max_infected:
                            max_infected = local_max
                            time_to_peak = t[np.where(D['I']==max_infected)][0] + time_completed
                        
                        # Print statement used to show the number of students infected during the specific period,
                        #  including those not attending school right now.
                        print("Max infected this period: " + str(local_max))

                        

                        # Printing time to the console
                        print("t = " + str(time_completed))
                iter_num += 1

                                
            # Gets all the desired metrics
            print(" ")
            print("Total Population: " + str(total_pop))
            print("Max # infected at a time: " + str(max_infected))
            print("Total # infected: " + str(len(recovered)+len(infected)))
            print("Time to peak: " + str(time_to_peak))
            print("Max percent infected at a time: " + str(100*max_infected/total_pop) + "%")
            print("Chance of infection: " + str(100*(len(recovered)+len(infected))/total_pop) + "%")
            print(" ")
            stats[0] = total_pop
            stats[1] += max_infected/run_iters
            stats[2] += (len(recovered)+len(infected))/run_iters
            stats[3] += time_to_peak/run_iters
            stats[4] += (100*max_infected/total_pop)/run_iters
            stats[5] += (100*(len(recovered)+len(infected))/total_pop)/run_iters
        print('---------------------------- ' + str(percent) + ' --------------------------')
        writer.writerow([str(stats[0]), str(stats[1]), str(stats[2]), str(stats[3]), str(stats[4]), str(stats[5]), str(percent)])
        print('Row written')
        percent += 1


