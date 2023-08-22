import networkx as nx
from evaluation_metric import *
from statistics import mean

def similar_users(graph, start_node, N):
    """
    Finds the most similar users to the given user, using the SimRank function of NetworkX.

    Args:
        graph: The graph to calculate the SimRank on.
        start_node: The node to calculate the SimRank for.

    Returns:
        A list of the most similar users to the given user.
    """

    sim = nx.simrank_similarity(graph, start_node)
    similar_users = []
    for node in sim:
        if node != start_node:
            similar_users.append((node, sim[node]))

    similar_users.sort(key=lambda x: x[1], reverse=True)
    #return similar_users
    
    return [u for u, _ in similar_users if u != start_node][:N]

def rank_nodes_by_similarity(similarity_matrix, target_node):
    # Get the similarity scores for the target node
    target_scores = similarity_matrix[target_node]
    
    # Sort the nodes by similarity score in descending order
    sorted_nodes = sorted(target_scores.items(), key=lambda item: item[1], reverse=True)
    
    return [node for node, _ in sorted_nodes]

if __name__ == "__main__":
    #G = nx.DiGraph()
    #G.add_weighted_edges_from([("A", "B", 1.0), ("A", "C", 0.5), ("B", "C", 0.7), ("B", "D", 0.2), ("C", "D", 0.9)])
    #G = nx.read_weighted_edgelist('user_relationship.csv', delimiter=',', create_using=nx.DiGraph(), encoding='utf-8')
    #similar_users = similar_users(G, "2", 10)
    #print(similar_users)

    #similarity_matrix = nx.simrank_similarity(G)
    # Get a ranking of nodes based on similarity to 'user1'
    #ranked_nodes = rank_nodes_by_similarity(similarity_matrix, '2')
    #print(ranked_nodes)

    G = nx.read_weighted_edgelist('user_relationship.csv', delimiter=',', create_using=nx.DiGraph(), encoding='utf-8')
    recommended = []
    relevant = []
    file = open('ground-truth-relevance-users.csv', 'r')
    for line in file:
        l = line.strip()
        x = l.split("|")
        user_id = str(x[0])
        id_list = x[1].split(",")
        similar_user_list = similar_users(G, user_id, 20)
        recommended.append(similar_user_list)
        relevant.append(id_list)
    file.close()
    p_at_20 = [precision_at_k(r, rel, 20) for r, rel in zip(recommended, relevant)]
    r_at_20 = [recall_at_k(r, rel, 20) for r, rel in zip(recommended, relevant)]
    f_at_20 = [f_measure(p, r) for p, r in zip(p_at_20, r_at_20)]
    print("Precision@10:", mean(p_at_20))
    print("Recall@10:", mean(r_at_20))
    print("F-measure@10:", mean(f_at_20))
    print("MAP@10:", mean_average_precision(recommended, relevant))