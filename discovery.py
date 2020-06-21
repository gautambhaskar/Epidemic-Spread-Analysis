import networkx as nx
import matplotlib.pyplot as plt
import EoN as e
import random
import numpy as np
import math



#To perform simulation without discovery and isolation, set disc_rate to 0. 
#To perform with discovery and isolation, set disc_rate to desired percent value.


# ---- Adjustable Values -----------------------------------
total_fam = int(input("Number of families in community [int]: ")) # Number of families in community being studied
fam_size = int(input("Average family size [int]: ")) # Family size
rho = float(input("Enter initial percent infected: "))
gamma = float(input("Enter recovery rate: ")) #Recovery Rate
tau = float(input("Enter transmission rate: ")) #Transmission Rate
time_reading = 2 #Time interval (must be integer) between each graph switch
iterations = int(input("Enter number of iterations of graph [int]: ")) # Number of times to change the graph
disc_rate = float(input("Enter discovery rate: ")) # Percentage of infected travellers discovered
# -----------------------------------------------------------

# Defining some stats
max_infected = 0 
peak_infected = 0
time_to_peak = 0
total_pop = total_fam * fam_size
initial_size = math.floor(rho*total_fam*fam_size) #Initial infected population size

# Defining some node lists. Nodes will be identified by unique integer-value IDs
statuses = []
recovereds = []
infecteds = list(range(initial_size))
discovered = []

#Creating the initial graph
G = nx.relaxed_caveman_graph(total_fam, fam_size, 0.3, seed=42)



for i in range(iterations):
    #Running the simulation
    sim = e.fast_SIR(G, tau, gamma, initial_infecteds = infecteds, initial_recovereds = recovereds, tmax=time_reading return_full_data=True)
    statuses = list(sim.get_statuses(time=time_reading).values())
    infecteds = []
    recovereds = []

    #Storing infected and recovered node info for next graph
    for j in range(len(statuses)):
        if statuses[j]=='I':
            infecteds.append(j)
        if statuses[j]=='R':
            recovereds.append(j)
    
    # Getting the peak value
    t, D = sim.summary()
    local_max = np.amax(D['I'])
    if local_max > max_infected:
        max_infected = local_max
        time_to_peak = t[np.where(D['I']==max_infected)][0] + i*time_reading

    # Printing time to the console
    print("t = " + str(i*time_reading))

    #Changing the graph to isolate discovered nodes
    for k in range(len(infecteds)):
        if k < disc_rate*len(infecteds): 
            node = infecteds[k]
            G.remove_node(node)
            G.add_node(node)
            discovered.append(node)

#Showing results at the end of the run
print(" ")
print("Total Population: " + str(total_pop))
print("Max # infected at a time: " + str(max_infected))
print("Total # infected: " + str(len(recovereds)+len(infecteds)))
print("Time to peak: " + str(time_to_peak))
print("Max percent infected at a time: " + str(100*max_infected/total_pop) + "%")
print("Chance of infection: " + str(100*(len(recovereds)+len(infecteds))/total_pop) + "%")
print("Total Discovered & Isolated: " + str(len(discovered)))
print(" ")
