# FILENAME: matching.pyx
# cython: language_level=3

import networkx
import numpy as np
from typing import Optional
# This file contains python wrappers for our C functions.
# The whole purpose of that is to make it easier for
# auto-completions to know our function definitions.
import array
import cython

#define NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION
import numpy as np
cimport numpy as np

def convert_to_numpy_array(list_of_tuples):
    cdef np.ndarray[np.int32_t, ndim=1] result_array

    # Determine the size of the resulting array
    cdef int array_size = sum(len(t) for t in list_of_tuples)

    # Create a flat NumPy array
    result_array = np.empty(array_size, dtype=np.int32)

    # Copy the data from the list of tuples to the NumPy array
    cdef int i, j
    cdef int[:] flat_view = result_array
    for i, tuple_data in enumerate(list_of_tuples):
        for j in range(len(tuple_data)):
            flat_view[i * len(tuple_data) + j] = tuple_data[j]

    return result_array

from libc.stdlib cimport free

def max_cardinality_matching(G: networkx.Graph):
    import time
    very_first_start_time = time.time()
    start_time = time.time()
    edge_list = convert_to_numpy_array(list(G.edges))
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"NetworkX EdgeView to edge list : {elapsed_time} seconds")
    cdef int[:] arr
    # Convert array to memory view
    arr = edge_list

    # Extract the pointer from the memory view
    cdef int *ptr = &arr[0]
    cdef int *result_ptr
    edge_list_length = len(edge_list)//2
    init_list = []
    result_matching = []
    start_time = time.time()
    num_matched_edges = match(edge_list_length,ptr,&result_ptr)
    end_time = time.time()
    # Calculate the 
    elapsed_time = end_time - start_time
    print(f"C Wrapper : {elapsed_time} seconds")
    print("Num matched edges in python",num_matched_edges)
    start_time = time.time()
    cdef int[:] values_view = <int[:2*num_matched_edges]> result_ptr
    cdef np.ndarray[np.int32_t, ndim=1, mode='c'] result = np.asarray(values_view, dtype=np.int32)
    set_of_tuples = set(map(tuple, result.reshape(-1, 2)))
    free(result_ptr)
    end_time = time.time()
    # Calculate the 
    elapsed_time = end_time - start_time
    print(f"Extract matching to set : {elapsed_time} seconds")
    very_last_end_time = time.time()
    elapsed_time = very_last_end_time - very_first_start_time
    print(f"Total Cython wall time: {elapsed_time} seconds")
    return set_of_tuples

