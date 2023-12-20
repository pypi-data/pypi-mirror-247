#include <stdio.h>
#include "graph.h"
#include "matching.h"
#include <time.h>
#include <unistd.h>
#include <string.h>
#include <libgen.h>

#include <sys/time.h>
double getTimeOfDay()
{
    struct timeval tv;
    gettimeofday(&tv, NULL);
    return (double)tv.tv_sec + (double)tv.tv_usec / 1000000.0;
}

typedef ListCell Cell;
int main(int argc, char **argv) {}
//void match(int nn, int nr, int *edge_list, int *matching, int *result)
int match(int nn, int *edge_list, int **result)
{
    //int *edge_list;
    int *matching;
    //int *result;
    long N;
    List *M;
    Cell *P;

    Graph *G;
    Vertex *V;
    Edge *E;
    int *matching_array;
    int matching_length = 0;
    // Function logic for the first list
    //int nc = nr;
    int nr = GetNumberNodesFromEdgeList(edge_list, nn);
    nr = nr + 1;
    int nc = nr;
#ifndef NDEBUG
    printf("NR %d\n", nr);
    printf("NC %d\n", nc);
    printf("NN %d\n", nn);
#endif
    // int * rows;
    // int * cols;
    // int * matching;
    double start_time_wall, end_time_wall;
    double start_time_csc_2_g, end_time_csc_2_g;
    double start_time_match, end_time_match;
    start_time_wall = getTimeOfDay();
    start_time_csc_2_g = getTimeOfDay();
    if (matching_length)
    {
        // Number of elements in the array
        size_t num_elements = nr;

        // Size of each element in bytes
        size_t element_size = sizeof(int);

        // Allocate memory for the array and initialize to zero
        matching_array = (int *)calloc(num_elements, element_size);
        InitializeMatching(matching, matching_array, nn);
    }
    else
    {
        matching_array = 0x0;
    }
    // G = CreateGraphFromCSC(rows, cols, matching_array, nr, nc, nn, !matching_length);
    G = CreateGraphFromEdgeList(edge_list, matching_array, nr, nc, nn, !matching_length);
    if (matching_length)
        free(matching_array);
    end_time_csc_2_g = getTimeOfDay();
    printf("Edge list to Graph conversion time: %f seconds\n", end_time_csc_2_g - start_time_csc_2_g);
#ifndef NDEBUG
    const char *extensionX = ".augP";
    char outputFilenameX[500];
    strcpy(outputFilenameX, argv[1]);
    strcat(outputFilenameX, extensionX);
    const char *extensionY = ".augT";
    char outputFilenameY[500];
    strcpy(outputFilenameY, argv[1]);
    strcat(outputFilenameY, extensionY);
    const char *extensionZ = ".dead";
    char outputFilenameZ[500];
    strcpy(outputFilenameZ, argv[1]);
    strcat(outputFilenameZ, extensionZ);
    FILE *output_fileX;
    FILE *output_fileY;
    FILE *output_fileZ;
    output_fileX = fopen(outputFilenameX, "w");
    output_fileY = fopen(outputFilenameY, "w");
    output_fileZ = fopen(outputFilenameZ, "w");
#endif

#ifndef NDEBUG
    M = MaximumCardinalityMatchingTrack(G, output_fileX, output_fileY, output_fileZ);
    fclose(output_fileX);
    fclose(output_fileY);
    fclose(output_fileZ);
#endif
    // Record the starting time
    start_time_match = getTimeOfDay();
    M = MaximumCardinalityMatching(G);
    end_time_match = getTimeOfDay();
    end_time_wall = getTimeOfDay();

    printf("Match time: %f seconds\n", end_time_match - start_time_match);

    // Calculate and print the elapsed time
    printf("Total Wall time: %f seconds\n", end_time_wall - start_time_wall);
    fprintf(stdout, "There are %d edges in the maximum-cardinality matching.\n",
            ListSize(M));
    // N = 1;
    int num_matched_edges = ListSize(M);
    *result = (int*)malloc(sizeof(int) * num_matched_edges * 2);
    N = 0;
    ForAllGraphVertices(V, G, P)
        VertexRelabel(V, (VertexData)N++);
    int edgeCounter = 0;
    ForAllEdges(E, M, P)
    {
        (*result)[2*edgeCounter]=(long) VertexLabel(EdgeFrom(E));
        (*result)[(2*edgeCounter)+1]=(long) VertexLabel(EdgeTo(E));
        edgeCounter++;
// fprintf(stdout, "Appended (%d, %d)\n",(int) VertexLabel(EdgeFrom(E)), (int) VertexLabel(EdgeTo(E)));
#ifndef NDEBUG
        fprintf(stdout, "Appended (%ld, %ld)\n", (long)VertexLabel(EdgeFrom(E)), (long)VertexLabel(EdgeTo(E)));
#endif
    }
    // fprintf(stdout, "(%d, %d)\n",(int) VertexLabel(EdgeFrom(E)), (int) VertexLabel(EdgeTo(E)));

    DestroyList(M);

    DestroyGraph(G);
    return num_matched_edges;
}
