import utils
import matplotlib.pyplot as plt

# Anzahl aller Knoten im Netzwerk
nodes_number = 256
# Anzahl der korrumpierten Knoten
corrupted_number = 112
# Anzahl der Cluster im Netzwerk
cluster_number = 32
# Anzahl der ausgewählten Nodes pro Cluster
picked_nodes_number = 0
# Anzahl der Iterationen für die Simulation
iteration_number = 10000
# Anzahl der gleichen Ergebnisse im gesamten Quorum
threshold = 0.5
# Anzahl der gleichen Ergebnisse im Nested Quorum
nested_threshold = 0.5

nodes_per_cluster = int(nodes_number / cluster_number)

debug = False

x = []
y = []

selection = list(range(nodes_per_cluster+1))
for count in selection:

    picked_nodes_number = count
    if nodes_per_cluster < picked_nodes_number:
        break

    x.append(count)
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

        corrupted_clusters_after_selection = utils.select_nodes_in_clusters(corrupted_clusters, picked_nodes_number, debug)
        if debug:
            print('corrupted clusters after selection:' + str(corrupted_clusters_after_selection))

        successful_corrupted_cluster_number = 0
        for cluster in corrupted_clusters_after_selection:
            if sum(cluster) > (nested_threshold * picked_nodes_number):
                successful_corrupted_cluster_number += 1

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
plt.show()