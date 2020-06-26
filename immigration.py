import networkx as nx
import matplotlib.pyplot as plt
import EoN as e
import random
import numpy as np
import math
import csv

percent = 0.0
run_iters = 10

#To perform simulation with unrestricted immigration, set trv_pr_sim to 800. To simulate no immigration, set to 0. 
# To similate discovery of infected travellers, set disc_rate to desired percentage.


# ---- Adjustable Values -----------------------------------
total_fam = int(input("Enter number of families in community [int]: ")) # Number of families in community being studied
fam_size = int(input("Enter average size of family [int]: ")) # Family size
rho = float(input("Enter initial percent infected: ")) #Initial infected population size
gamma = float(input("Enter recovery rate: ")) #Recovery Rate
tau = float(input("Enter transmission rate: ")) #Transmission Rate
time_reading = 1 #Time interval (must be integer) between each graph switch
a = 0.3 # Percent of edges connected between families
imgr_rate = float(input("Enter percentage of immigrants infected: ")) #Percentage of arriving travellers infected
trv_pr_sim = int(input("Enter number travellers arriving per iteration [int]: ")) #Number of travellers arriving per iteration
interactions_per_trv = int(input("Enter interactions per traveller [int]: ")) #Number of edges per traveller node.
iterations = int(input("Enter number of iterations (# of times travellers are added) [int]: ")) # Number of times to change the graph
# -----------------------------------------------------------
with open('immigration.csv', mode='w') as f:
    writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(['Total Population', 'Max Infected', 'Total Infected', 'Time to Peak', 'Percent max infected', 'Percent total infected', 'Total Discovered & Isolated', 'Percent Discovered & Isolated','Discovery Rate'])

    while percent < 1:
        disc_rate = percent # Percentage of infected travellers discovered
        stats = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        for i in range(run_iters):
            # Defining some stats
            max_infected = 0 
            peak_infected = 0
            time_to_peak = 0
            total_pop = total_fam * fam_size
            initial_size = math.floor(rho*total_fam*fam_size)

            # Defining some node lists. Nodes will be identified by unique integer-value IDs
            statuses = list(range(total_pop))
            recovereds = []
            infecteds = random.sample(list(range(total_pop)), math.floor(rho*total_pop))
            discovered = []

            #Creating the initial graph
            G = nx.Graph()
            for fam in range(total_fam):
                H = nx.complete_graph(fam_size)
                G=nx.disjoint_union(H,G)

            edges=G.edges()

            L=[]

            for x in range(total_pop):
                for b in range(total_pop):
                    n=(b,x)
                    L.append(n)
                    
            #for edge in edges:
            #    L.remove(edge)
            L = [edge for edge in L if edge not in edges]

            edge_list=random.sample(L, math.floor(a*total_pop))
            G.add_edges_from(edge_list)

            started = False

            for i in range(iterations):
                
                #Getting the highest value node, so as to not make new nodes with same identity
                highest_value = len(statuses) - 1
                #Changing the graph
                for j in range(trv_pr_sim): 
                    node = highest_value + j + 1
                    G.add_node(node)
                    if j < (trv_pr_sim*imgr_rate * disc_rate):
                        discovered.append(node)
                        infecteds.append(node)
                    else:
                        if j < trv_pr_sim*imgr_rate:
                            infecteds.append(node)
                        for k in range(interactions_per_trv):
                            G.add_edge(node, random.randint(0, node - 1))
                    total_pop += 1 #Adding one to the total population metric

                #Running the simulation
                sim = e.fast_SIR(G, tau, gamma, initial_infecteds=infecteds, initial_recovereds = recovereds, tmax=time_reading, return_full_data=True)

                statuses = list(sim.get_statuses(time=time_reading).values())
                infecteds = []
                recovereds = []
                #sim.display(time=time_reading)
                #plt.show()





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


            #Showing results at the end of the run
            print(" ")
            print("Total Population: " + str(total_pop))
            print("Max # infected at a time: " + str(max_infected))
            print("Total # infected: " + str(len(recovereds)+len(infecteds)))
            print("Time to peak: " + str(time_to_peak))
            print("Max percent infected at a time: " + str(100*max_infected/total_pop) + "%")
            print("Chance of infection: " + str(100*(len(recovereds)+len(infecteds))/total_pop) + "%")
            print(" ")
            stats[0] = total_pop
            stats[1] += max_infected/run_iters
            stats[2] += (len(recovereds)+len(infecteds))/run_iters
            stats[3] += time_to_peak/run_iters
            stats[4] += (100*max_infected/total_pop)/run_iters
            stats[5] += (100*(len(recovereds)+len(infecteds))/total_pop)/run_iters
            stats[6] += len(discovered)/run_iters
            stats[7] += (100*len(discovered)/total_pop)/run_iters
        print('---------------------------- ' + str(percent) + ' --------------------------')
        writer.writerow([str(stats[0]), str(stats[1]), str(stats[2]), str(stats[3]), str(stats[4]), str(stats[5]), str(stats[6]), str(stats[7]), str(percent)])
        print('Row written')
        percent += 0.1
