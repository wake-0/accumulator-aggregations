import random
import copy

# ATTENTION: Actually the clusters are all the same size if possible
def create_clusters(nodes_number, cluster_number):
    clusters = []
    nodes_per_cluster = nodes_number // cluster_number
    nodes_remainder = nodes_number % cluster_number
    for _ in range(cluster_number):
        cluster = [0] * nodes_per_cluster
        if nodes_remainder > 0:
            cluster.append(0)
            nodes_remainder -= 1
        clusters.append(cluster)
    return clusters

def create_equaly_corrupted_clusters(clusters, corrupted_number):
    # Gleichverteilung der Angreifer
    cluster_number = len(clusters)
    corrupted_per_cluster = corrupted_number // cluster_number
    corrupted_remainder = corrupted_number % cluster_number

    corrupted_clusters = []
    for index, cluster in enumerate(clusters):
        number_to_corrupt = corrupted_per_cluster
        if corrupted_remainder > 0:
            # Versuchen die korrumpierten Knoten gleichmaessig zu verteilen
            number_to_corrupt += 1
            corrupted_remainder -= 1

        nodes_in_cluster = len(cluster)
        corrupted_cluster = [0] * nodes_in_cluster

        index_to_corrupt = list(range(nodes_in_cluster))
        random.shuffle(index_to_corrupt)
        index_to_corrupt = index_to_corrupt[:number_to_corrupt]
        for index in index_to_corrupt:
            corrupted_cluster[index] = 1

        corrupted_clusters.append(corrupted_cluster)

    return corrupted_clusters

def create_corrupted_clusters(clusters, corrupted_number):
    all_possibilities = []
    for i, cluster in enumerate(clusters):
        for j, node in enumerate(cluster):
            all_possibilities.append([i, j])
    random.shuffle(all_possibilities)
    corrupted_nodes = all_possibilities[:corrupted_number]

    # Set corrupted nodes
    for c in corrupted_nodes:
        clusters[c[0]][c[1]] = 1
    return clusters

def filter_corrupted_clusters(corrupted_clusters, picked_nodes_number, nested_threshold, debug=False):
    # Anzahl der erfolgreich korrumpierten Cluster
    successful_corrupted_clusters = []

    # Reset alle nicht verwendeten Nodes
    all_nodes = sum([len(cluster) for cluster in corrupted_clusters])
    unused_nodes = random_nodes_in_clusters(corrupted_clusters, all_nodes - picked_nodes_number)
    corrupted_clusters = copy.deepcopy(corrupted_clusters)
    for c in unused_nodes:
        corrupted_clusters[c[0]][c[1]] = 0

    if debug:
        print('corrupted clusters after selection:' + str(corrupted_clusters))

    # Berechnen aller erfolgreich korrumpierter Knoten
    for cluster in corrupted_clusters:
        number_corrupted_nodes = sum(cluster)
        ratio = number_corrupted_nodes / picked_nodes_number
        if ratio > nested_threshold:
            successful_corrupted_clusters.append(cluster)
    
    return successful_corrupted_clusters

def select_nodes_in_clusters(corrupted_clusters, picked_nodes_number, debug=False):
    corrupted_clusters = copy.deepcopy(corrupted_clusters)

    # Reset alle nicht verwendeten Nodes
    for cluster in corrupted_clusters:
        select_count = len(cluster) - picked_nodes_number
        selected_nodes = random_nodes_in_cluster(cluster, select_count)
        if debug:
            print(str(selected_nodes))
        for c in selected_nodes:
            cluster[c] = 0

    return corrupted_clusters

# Select random nodes in cluster
def random_nodes_in_cluster(cluster, node_count):
    random_nodes = list(range(len(cluster)))
    random.shuffle(random_nodes)
    return random_nodes[:node_count]

# Select random nodes in clusters
def random_nodes_in_clusters(clusters, node_count):
    random_nodes = []
    for i, cluster in enumerate(clusters):
        for j, node in enumerate(cluster):
            random_nodes.append([i, j])
    random.shuffle(random_nodes)
    return random_nodes[:node_count]
