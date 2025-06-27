The test instances start with a line providing basic information about the number of nodes (|V|), the number of clusters (K) and the value for Tmax. 
The second line contains the string "NODE_COORD_SECTION" which is followed by one line for each node each consisting of three (integer) values defining the node number (between 1 and |V|), the X and Y-coordinate of that node. 
After specifying all nodes a line containing the string "SET_SECTION" follows. 
Subsequently, there are K lines each containing the cluster number (i.e., an integer between 1 and K), the score of this cluster (score), and the list of nodes contained in this cluster. 

The (symmetric) travel time t_{ij} between two nodes i and j is defined as the Euclidean distance between them rounded up to the next integer, i.e., equal to t_{ij}=\lceil \sqrt{(x_i-x_j)^2 + (y_i-y_j)^2} \rceil if the x_\ell and y_\ell are the x- and y-coordinates of node \ell\in V, respectively.



Example: 

	5 2 10
	NODE_COORD_SECTION
	1 1 5 
	2 2 3
	3 4 4
	4 2 2
	5 6 4
	SET_SECTION
	1 10 2 3 5
	2 8 2 3 4

In this example, an instance with 5 nodes, 2 clusters and a maximum travel time of 10 is defined in which cluster 1 has a score of 10 and contains nodes 2, 3, and 5 while cluster 2 has a score of 8 and contains nodes 2, 3 and 4.