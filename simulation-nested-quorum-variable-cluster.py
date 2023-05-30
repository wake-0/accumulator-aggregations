import utils

# Anzahl aller Knoten im Netzwerk
nodes_number = 256
# Anzahl der korrumpierten Knoten
corrupted_number = 200
# Anzahl der Cluster im Netzwerk
cluster_number = 2
# Anzahl der ausgewählten Nodes pro Cluster
picked_nodes_number = 8
# Anzahl der Iterationen für die Simulation
iteration_number = 100
# Anzahl der gleichen Ergebnisse im gesamten Quorum
threshold = 0.5
# Anzahl der gleichen Ergebnisse im Nested Quorum
nested_threshold = 0.5

debug = False

for v in [4, 8, 16, 32, 64]:

    for c in [1, 2, 4, 8, 16, 32, 64]:
        successful_corrupted_number = 0
        cluster_number = c
        picked_nodes_number = int(v / c)
        corrupted_number = picked_nodes_number

        if picked_nodes_number == 0:
            break

        for _ in range(iteration_number):
            # Create clusters
            clusters = utils.create_clusters(nodes_number, cluster_number)
            if debug:
                print('clusters:' + str(clusters))

            # Create corrupted nodes
            corrupted_clusters = utils.create_corrupted_clusters(clusters, corrupted_number)
            if debug:
                print('corrupted clusters:' + str(corrupted_clusters))

            successful_corrupted_clusters = utils.filter_corrupted_clusters(corrupted_clusters, picked_nodes_number, nested_threshold)
            if debug:
                print('successful corrupted clusters:' + str(successful_corrupted_clusters))

            successful_corrupted_cluster_number = len(successful_corrupted_clusters)
            successful_corrupted_ratio = successful_corrupted_cluster_number / cluster_number
            if successful_corrupted_ratio > threshold:
                successful_corrupted_number += 1

        print('V: ' + str(v))
        print('Cluster count: ' + str(cluster_number))
        print('Picked nodes count: ' + str(picked_nodes_number))
        print('Successful corrupted: ' + str(successful_corrupted_number))
        print('Successful corrupted ratio: ' + str(successful_corrupted_number / iteration_number))
        print('-'*100)