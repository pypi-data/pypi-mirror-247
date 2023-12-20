# FILENAME: matching.pxd
# cython: language_level=3

cdef extern from "driver.h":
    
    cdef int match(int nn, int *edge_list, int **result)
