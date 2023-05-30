import utils
import matplotlib.pyplot as plt

# Anzahl aller Knoten im Netzwerk
nodes_number = 256
# Anzahl der korrumpierten Knoten
corrupted_number = 127
# Anzahl der Cluster im Netzwerk
cluster_number = 1
# Anzahl der ausgewählten Nodes pro Cluster
picked_nodes_number = 2
# Anzahl der Iterationen für die Simulation
iteration_number = 1000
# Anzahl der gleichen Ergebnisse im gesamten Quorum
threshold = 0.0
# Anzahl der gleichen Ergebnisse im Nested Quorum
nested_threshold = 0.5

debug = False

x = []
y = []

selection = [1, 2, 4, 8, 16, 32, 64, 96, 128, 160, 192]
for count in selection:

    x.append(count)
    picked_nodes_number = count
    successful_corrupted_number = 0

    for _ in range(iteration_number):
        # Create clusters
        clusters = utils.create_clusters(nodes_number, cluster_number)
        if debug:
            print('clusters:' + str(clusters))

        # Create corrupted nodes
        corrupted_clusters = utils.create_equaly_corrupted_clusters(clusters, corrupted_number)
        if debug:
            print('corrupted clusters:' + str(corrupted_clusters))

        successful_corrupted_clusters = utils.filter_corrupted_clusters(corrupted_clusters, picked_nodes_number, nested_threshold)
        if debug:
            print('successful corrupted clusters:' + str(successful_corrupted_clusters))

        successful_corrupted_cluster_number = len(successful_corrupted_clusters)
        successful_corrupted_ratio = successful_corrupted_cluster_number / cluster_number
        if successful_corrupted_ratio > threshold:
            successful_corrupted_number += 1

    success_rate = successful_corrupted_number / iteration_number
    y.append(success_rate)

    print('Picked nodes in cluster: ' + str(picked_nodes_number))
    print('Successful corrupted: ' + str(successful_corrupted_number))
    print('Successful corrupted ratio: ' + str(success_rate))
    print('-'*100)

fig = plt.figure()
ax = fig.add_axes([0.1, 0.1, 0.8, 0.8])
ax.plot(x, y)
# ax.set_xticks(selection)
# ax.set_yticks([0,1])
plt.show()