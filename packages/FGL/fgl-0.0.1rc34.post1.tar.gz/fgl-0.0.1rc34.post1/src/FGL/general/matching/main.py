import pyximport; pyximport.install()
from matching import max_cardinality_matching
import networkx as nx
import cProfile
G = nx.karate_club_graph()
G = nx.erdos_renyi_graph(5000, 0.08)
print(G)
import time
start_time = time.time()
matching = max_cardinality_matching(G)
end_time = time.time()
elapsed_time = end_time - start_time
print(f"Elapsed time: {elapsed_time} seconds")
print(len(matching))

