import networkx as nx
import matplotlib.pyplot as plt
import EoN as e
import random
import numpy as np
import math




#To perform simulation with unrestricted immigration, set trv_pr_sim to 800. To simulate no immigration, set to 0. 
# To similate discovery of infected travellers, set disc_rate to desired percentage.


# ---- Adjustable Values -----------------------------------
total_fam = int(input("Enter number of families in community [int]: ")) # Number of families in community being studied
fam_size = int(input("Enter average size of family [int]: ")) # Family size
rho = float(input("Enter initial percent infected: ")) #Initial infected population size
gamma = float(input("Enter recovery rate: ")) #Recovery Rate
tau = float(input("Enter transmission rate: ")) #Transmission Rate
time_reading = 1 #Time interval (must be integer) between each graph switch
imgr_rate = float(input("Enter percentage of immigrants infected: ")) #Percentage of arriving travellers infected
trv_pr_sim = int(input("Enter number travellers arriving per iteration [int]: ")) #Number of travellers arriving per iteration
interactions_per_trv = int(input("Enter interactions per traveller [int]: ")) #Number of edges per traveller node.
iterations = int(input("Enter number of iterations (# of times travellers are added) [int]: ")) # Number of times to change the graph
disc_rate = float(input("Enter discovery rate: ")) # Percentage of infected travellers discovered
# -----------------------------------------------------------

# Defining some stats
max_infected = 0 
peak_infected = 0
time_to_peak = 0
total_pop = total_fam * fam_size
initial_size = math.floor(rho*total_fam*fam_size)

# Defining some node lists. Nodes will be identified by unique integer-value IDs
statuses = []
recovereds = []
infecteds = list(range(initial_size))
discovered = []

#Creating the initial graph
G = nx.relaxed_caveman_graph(total_fam, fam_size, 0.3, seed=42)



for i in range(iterations):
    #Running the simulation
    sim = e.fast_SIR(G, tau, gamma, initial_infecteds = infecteds, initial_recovereds = recovereds, tmax=time_reading, return_full_data=True)
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
        max_infected = local_max)
        time_to_peak = t[np.where(D['I']==max_infected)][0] + i*time_reading

    # Printing time to the console
    print("t = " + str(i*time_reading))
    
    #Getting the highest value node, so as to not make new nodes with same identity
    highest_value = len(statuses) - 1

    #Changing the graph
    for j in range(trv_pr_sim): 
        node = highest_value + j + 1
        G.add_node(node)
        if j < (trv_pr_sim*imgr_rate) * disc_rate:
            discovered.append(node)
            infecteds.append(node)
        else:
            if j < trv_pr_sim*imgr_rate:
                infecteds.append(node)
            for k in range(interactions_per_trv):
                G.add_edge(node, random.randint(0, node - 1))
        total_pop += 1 #Adding one to the total population metric

#Showing results at the end of the run
print(" ")
print("Total Population: " + str(total_pop))
print("Max # infected at a time: " + str(max_infected))
print("Total # infected: " + str(len(recovereds)+len(infecteds)))
print("Time to peak: " + str(time_to_peak))
print("Max percent infected at a time: " + str(100*max_infected/total_pop) + "%")
print("Chance of infection: " + str(100*(len(recovereds)+len(infecteds))/total_pop) + "%")
print(" ")

