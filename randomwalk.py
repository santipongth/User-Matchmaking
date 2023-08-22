import networkx as nx
import random
from evaluation_metric import *
from statistics import mean

def random_walk(G, start_node, max_steps):
    """
    Performs a random walk on the graph, starting at the given node, for the given number of steps.

    Args:
        graph: The graph to perform the random walk on.
        start_node: The node to start the random walk at.
        max_steps: The maximum number of steps to take in the random walk.

    Returns:
        A list of the nodes that were visited during the random walk.
    """
    
    visited_nodes = []
    visited_nodes = [start_node]
    current_node = start_node

    for _ in range(max_steps):
        neighbors = list(G.neighbors(current_node))
        if len(neighbors) > 0:
            next_node = random.choice(neighbors)
            visited_nodes.append(next_node)
            current_node = next_node
        else:
            break    
    return visited_nodes

def random_walk_weight(G, start_node, max_steps):
    visited_nodes = []
    visited_nodes = [start_node]
    current_node = start_node

    for _ in range(max_steps):
        neighbors = list(G.neighbors(current_node))
        if len(neighbors) > 0:
            #Select neighbor by edge weight
            weights = [G[current_node][neighbor]['weight'] for neighbor in neighbors]
            total_weight = sum(weights)
            weights = [weight / total_weight for weight in weights]

            next_node = random.choices(neighbors, weights)[0]
            visited_nodes.append(next_node)
            current_node = next_node
        else:
            break
    return visited_nodes

def similar_users_weight(graph, start_node, max_steps):
  visited_nodes = random_walk_weight(graph, start_node, max_steps)
  similar_users = []
  for node in visited_nodes:
    if node != start_node:
      similar_users.append(node)

  return similar_users

def similar_users(graph, start_node, max_steps):
  """
  Finds the most similar users to the given user, using a random walk algorithm.

  Args:
    graph: The graph to perform the random walk on.
    start_node: The node to start the random walk at.
    max_steps: The maximum number of steps to take in the random walk.

  Returns:
    A list of the most similar users to the given user.
  """

  visited_nodes = random_walk(graph, start_node, max_steps)
  similar_users = []
  for node in visited_nodes:
    if node != start_node:
      similar_users.append(node)

  return similar_users

if __name__ == "__main__":
    
  # Create a directed, weighted graph
  #G = nx.DiGraph()
  #edges = [("A", "B", 0.7), ("A", "C", 0.3), ("B", "D", 0.9), ("B", "E", 0.1), ("C", "F", 1.0)]
  #G.add_weighted_edges_from(edges)

  # check if Graph is directed
  #print('Directed:', nx.is_directed(G))

  # check if Graph is weighted
  #print('Weighted:', nx.is_weighted(G))
  #print()

  #similar_users = similar_users(G, "A", 10)
  #print(similar_users)
  #similar_users = similar_users_weight(G, "A", 10)
  #print(similar_users)

  #G = nx.read_weighted_edgelist('user_relationship.csv', delimiter=',', create_using=nx.DiGraph(), encoding='utf-8')
  #similar_users = similar_users(G, "2", 10)
  #print(similar_users)
  #similar_users = similar_users_weight(G, "2", 10)
  #print(similar_users)
