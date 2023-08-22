import networkx as nx
from evaluation_metric import *
from statistics import mean

def find_communities(graph):
    """
    Finds the best communities in the given graph, using the Girvan-Newman algorithm.

    Args:
        graph: The graph to find the communities in.

    Returns:
        A list of the communities in the graph.
    """

    communities_generator = nx.community.girvan_newman(graph)
    top_level_communities = next(communities_generator)
    return top_level_communities

def recommend_similar_users(user, communities, N):
    """
    Recommends similar users from the same community as the given user.

    Args:
        user: The user to find similar users for.
        communities: The communities in the graph.

    Returns:
        A list of the similar users from the same community as the given user.
    """

    for community in communities:
        if user in community:
            return [u for u in community if u != user][:N]

if __name__ == "__main__":
    #G = nx.DiGraph()
    #G.add_weighted_edges_from([("A", "B", 1.0), ("A", "C", 0.5), ("B", "C", 0.7), ("B", "D", 0.2), ("C", "D", 0.9)])
    #G = nx.read_weighted_edgelist('user_relationship.csv', delimiter=',', create_using=nx.DiGraph(), encoding='utf-8')

    #communities = find_communities(G)
    #similar_users = recommend_similar_users("8", communities, 10)
    #print(similar_users)

    G = nx.read_weighted_edgelist('user_relationship.csv', delimiter=',', create_using=nx.DiGraph(), encoding='utf-8')
    recommended = []
    relevant = []
    file = open('ground-truth-relevance-users.csv', 'r')
    for line in file:
        l = line.strip()
        x = l.split("|")
        user_id = str(x[0])
        id_list = x[1].split(",")
        communities = find_communities(G)
        similar_user_list = recommend_similar_users(user_id, communities, 20)
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