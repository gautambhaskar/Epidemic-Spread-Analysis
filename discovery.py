import networkx as nx
import matplotlib.pyplot as plt
import EoN as e
import random
import numpy as np
import math
import csv

percent = 0.0
run_iters = 10
#To perform simulation without discovery and isolation, set disc_rate to 0. 
#To perform with discovery and isolation, set disc_rate to desired percent value.


# ---- Adjustable Values -----------------------------------
total_fam = int(input("Number of families in community [int]: ")) # Number of families in community being studied
fam_size = int(input("Average family size [int]: ")) # Family size
rho = float(input("Enter initial percent infected: "))
gamma = float(input("Enter recovery rate: ")) #Recovery Rate
tau = float(input("Enter transmission rate: ")) #Transmission Rate
time_reading = 2 #Time interval (must be integer) between each graph switch
a = 0.3 # Percent of edges connected between families
iterations = int(input("Enter number of iterations of graph [int]: ")) # Number of times to change the graph
# -----------------------------------------------------------

with open('discovery.csv', mode='w') as f:
    writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(['Total Population', 'Max Infected', 'Total Infected', 'Time to Peak', 'Percent max infected', 'Percent total infected', 'Total Discovered & Isolated', 'Percent Discovered & Isolated','Discovery Rate'])

    while percent < 1:
        stats = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        for i in range(run_iters):
            disc_rate = percent # Percentage of infected travellers discovered
            # Defining some stats
            max_infected = 0 
            peak_infected = 0
            time_to_peak = 0
            total_pop = total_fam * fam_size
            initial_size = math.floor(rho*total_fam*fam_size) #Initial infected population size

            # Defining some node lists. Nodes will be identified by unique integer-value IDs
            statuses = []
            recovereds = []
            infecteds = random.sample(list(range(total_pop)), math.floor(rho*total_pop))
            discovered = []

            #Creating the initial graph
            print("Creating the initial graph")
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
                #L.remove(edge)
            L = [edge for edge in L if edge not in edges]

            edge_list=random.sample(L, math.floor(a*total_pop))
            G.add_edges_from(edge_list)


            edge_list=random.sample(L, math.floor(a*total_pop))
            G.add_edges_from(edge_list)

            started = False

            for i in range(iterations):
                #Running the simulation
                sim = e.fast_SIR(G, tau, gamma, initial_infecteds=infecteds, initial_recovereds = recovereds, tmax=time_reading, return_full_data=True)

                statuses = list(sim.get_statuses(time=time_reading).values())
                #sim.display(time=time_reading)
                #plt.show()
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

                #Changing the graph to isolate discovered nodes
                infected_not_discovered = []
                for node in infecteds:
                    if node not in discovered:
                        infected_not_discovered.append(node)
                for k in range(len(infected_not_discovered)):
                    if k < disc_rate*len(infected_not_discovered): 
                        node = infected_not_discovered[k]
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
            stats[0] = total_pop
            stats[1] += max_infected/run_iters
            stats[2] += (len(recovereds)+len(infecteds))/run_iters
            stats[3] += time_to_peak/run_iters
            stats[4] += (100*max_infected/total_pop)/run_iters
            stats[5] += (100*(len(recovereds)+len(infecteds))/total_pop)/run_iters
            stats[6] += len(discovered)/run_iters
            stats[7] += (100*len(discovered)/total_pop)/run_iters
            print(" ")
        print('---------------------------- ' + str(percent) + ' --------------------------')
        writer.writerow([str(stats[0]), str(stats[1]), str(stats[2]), str(stats[3]), str(stats[4]), str(stats[5]), str(stats[6]), str(stats[7]), str(percent)])
        print('Row written')
        percent += 0.01