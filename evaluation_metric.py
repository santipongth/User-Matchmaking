def precision_at_k(recommended, relevant, k):
    top_k = recommended[:k]
    relevant_count = sum([1 for item in top_k if item in relevant])
    return relevant_count / k

def recall_at_k(recommended, relevant, k):
    top_k = recommended[:k]
    relevant_count = sum([1 for item in top_k if item in relevant])
    return relevant_count / len(relevant)

def f_measure(precision, recall):
    if precision + recall == 0:
        return 0
    return (2 * precision * recall) / (precision + recall)

def average_precision(recommended, relevant):
    precisions = [precision_at_k(recommended, relevant, i+1) for i, item in enumerate(recommended) if item in relevant]
    if not precisions:
        return 0
    return sum(precisions) / len(relevant)

def mean_average_precision(recommendations, relevants):
    return sum([average_precision(recommended, relevant) for recommended, relevant in zip(recommendations, relevants)]) / len(recommendations)

# Example:
#recommended = [['A', 'B', 'C', 'D', 'E'], ['X', 'Y', 'A', 'B', 'C']]
#relevant = [['A', 'C', 'E', 'F', 'G'], ['A', 'C', 'E']]
#p_at_5 = [precision_at_k(r, rel, 5) for r, rel in zip(recommended, relevant)]
#r_at_5 = [recall_at_k(r, rel, 5) for r, rel in zip(recommended, relevant)]
#f_at_5 = [f_measure(p, r) for p, r in zip(p_at_5, r_at_5)]
#print("Precision@5:", p_at_5)
#print("Recall@5:", r_at_5)
#print("F-measure@5:", f_at_5)
#print("MAP:", mean_average_precision(recommended, relevant))