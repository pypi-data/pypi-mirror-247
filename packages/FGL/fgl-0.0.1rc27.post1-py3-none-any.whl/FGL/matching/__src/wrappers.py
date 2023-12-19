from .. import __lib
import networkx
import scipy
import copy
from typing import Optional
# This file contains python wrappers for our C functions.
# The whole purpose of that is to make it easier for
# auto-completions to know our function definitions.

# __lib is the compiled library containing our c functions.

def max_cardinality_matching(rows, cols, matching):
    return __lib.match_wrapper(rows, cols, matching)

def max_cardinality_matching(G: networkx.Graph, init_list: Optional[list] = []):
    # Get the number of nodes in the graph
    from scipy.sparse import coo_matrix
    num_nodes = len(G)

    # Initialize COO matrix data
    data = []
    row_indices = []
    col_indices = []

    # Iterate through the edges of the graph and populate the COO matrix data
    for edge in G.edges():
        row_indices.append(edge[0])
        col_indices.append(edge[1])
        data.append(1)  # Assuming unweighted graph, set 1 for the presence of an edge

    # Create the COO matrix
    coo_matrix_representation = coo_matrix((data, (row_indices, col_indices)), shape=(num_nodes, num_nodes), dtype=int)

    # Convert COO matrix to CSR matrix
    csr_matrix_representation = coo_matrix_representation.tocsr()
    rows = csr_matrix_representation.indptr.tolist()
    cols = csr_matrix_representation.indices.tolist()
    """
    sparse = networkx.to_scipy_sparse_array(G,format="csr")
    rows = sparse.indptr.tolist()
    cols = sparse.indices.tolist()
    """
    result_matching = []
    __lib.match_wrapper(rows, cols, init_list, result_matching)
    return copy.deepcopy(result_matching)
