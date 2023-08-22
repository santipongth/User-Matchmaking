import networkx as nx
from evaluation_metric import *
from statistics import mean

# Compute Personalized PageRank scores
'''
def personalized_pagerank(G, personalization_node):
    personalization = {node: 0 for node in G.nodes}
    personalization[personalization_node] = 1
    return nx.pagerank(G, personalization = personalization)
'''

def similar_users(G, start_node, N):
    # Compute Personalized PageRank scores
    #pagerank_scores = personalized_pagerank(G, user)
    pagerank_scores = nx.pagerank(G, personalization={start_node: 1.0})
    
    # Sort users by score in descending order
    sorted_users = sorted(pagerank_scores.items(), key=lambda item: item[1], reverse=True)
    
    # Return the top N users, excluding the user itself
    similar_users = [u for u, _ in sorted_users if u != start_node][:N]
    
    return similar_users

if __name__ == "__main__":
    #G = nx.DiGraph()
    #G.add_weighted_edges_from([("A", "B", 1.0), ("A", "C", 0.5), ("B", "C", 0.7), ("B", "D", 0.2), ("C", "D", 0.9)])
    G = nx.read_weighted_edgelist('user_relationship.csv', delimiter=',', create_using=nx.DiGraph(), encoding='utf-8')

    #similar_users = similar_users(G, "A")
    #print(similar_users)

    # Find similar users to 'user1'
    #pagerank_scores = personalized_pagerank(G, '2')

    # Print PageRank scores
    #for user, score in sorted(pagerank_scores.items(), key=lambda item: item[1], reverse=True):
    #print(f"{user}: {score}")

    #similar_users = similar_users(G, '8', 10)
    #print("Users similar:", similar_users)


    # Print the results
    #for user, similar_users in similar_users_dict.items():
    #print(f"Users similar to '{user}': {similar_users}")

    #https://www.briggsby.com/personalized-pagerank
    #https://kiani.info/mathematicians-relations-and-communities-with-each-other
    #simple_pagerank = nx.pagerank(G, alpha=0.85)
    #personalized_pagerank = nx.pagerank(G, alpha=0.85, personalization={'A': 0, 'B': 0, 'C': 1, 'D': 0})
    #weighted_pagerank = nx.pagerank(G_weighted, alpha=0.85)
    #weighted_personalized_pagerank = nx.pagerank(G_weighted, alpha=0.85, personalization={'A': 0, 'B': 0, 'C': 1, 'D': 0})
    
    G = nx.read_weighted_edgelist('user_relationship.csv', delimiter=',', create_using=nx.DiGraph(), encoding='utf-8')
    recommended = []
    relevant = []
    file = open('ground-truth-relevance-users.csv', 'r')
    for line in file:
        l = line.strip()
        x = l.split("|")
        user_id = str(x[0])
        id_list = x[1].split(",")
        similar_user_list = similar_users(G, user_id, 15)
        recommended.append(similar_user_list)
        relevant.append(id_list)
    file.close()
    p_at_15 = [precision_at_k(r, rel, 15) for r, rel in zip(recommended, relevant)]
    r_at_15 = [recall_at_k(r, rel, 15) for r, rel in zip(recommended, relevant)]
    f_at_15 = [f_measure(p, r) for p, r in zip(p_at_15, r_at_15)]
    print("Precision@10:", mean(p_at_15))
    print("Recall@10:", mean(r_at_15))
    print("F-measure@10:", mean(f_at_15))
    print("MAP@10:", mean_average_precision(recommended, relevant))