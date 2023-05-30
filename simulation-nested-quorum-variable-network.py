import utils

# Anzahl aller Knoten im Netzwerk
nodes_number = 64
# Anzahl der korrumpierten Knoten
corrupted_number = 32
# Anzahl der Cluster im Netzwerk
cluster_number = 16
# Anzahl der ausgewählten Nodes pro Cluster
picked_nodes_number = 4
# Anzahl der Iterationen für die Simulation
iteration_number = 1000
# Anzahl der gleichen Ergebnisse im gesamten Quorum
threshold = 0.5
# Anzahl der gleichen Ergebnisse im Nested Quorum
nested_threshold = 0.5

debug = False

for t in [[0.25,0.25], [0.25,0.5], [0.25,0.75], [0.5,0.5], [0.5,0.75], [0.75,0.25], [0.75,0.5], [0.75,0.75]]:

    successful_corrupted_number = 0
    threshold = t[0]
    nested_threshold = t[1]

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

    print('Picked nodes in cluster: ' + str(picked_nodes_number))
    print('Successful corrupted: ' + str(successful_corrupted_number))
    print('Successful corrupted ratio: ' + str(success_rate))
    print('-'*100)



















