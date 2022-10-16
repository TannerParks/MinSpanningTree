# Tanner Parks
# CS 325 Homework 4
# February 2022

import math
import sys


class Edge:
    def __init__(self, edge: list, distance: int):
        self.edge = edge
        self.dist = distance


def getData():
    """Turns the data from the file into a list of lists."""
    dataList = []

    with open("graph.txt", "r") as file:
        fileData = file.read().splitlines()
        for item in fileData:
            data = item.split()
            dataList.append([int(item) for item in data])  # Turns data into a list of integers

    return dataList


def getPoints(data: list):
    """Separates the coordinates from the data we got from the file."""
    numVertices = 0
    coords = []

    for i in data[1::]: # Starts at the second item since we don't need the first number

        if len(i) == 1:
            numVertices = i[0]
            coords.clear()  # Clears the coordinates from the list for the next test case
        else:
            coords.append(i)
            if len(coords) == numVertices:  # If True, it means the coordinates are all in the list
                adjacencyMatrix(coords)


def adjacencyMatrix(coords: list):
    """Makes an adjacency matrix of the coordinates."""
    #print(coords)
    edges = []  # List of edges and their weights
    matrix = [[0 for column in coords] for row in coords]   # Makes matrix of correct size for weights to be added to
    for i, coord in enumerate(coords):  # for index, coordinate in list of coordinates
        for j in range(i+1, len(coords)):
            edges.append(Edge([coords[i], coords[j]], round(math.dist(coords[i], coords[j]))))
    for edge in edges:

        # Puts the weights in the matrix on both ends so if (0,1)-(1,0) has a weight of 4 it puts 4 at those indexes  n
        matrix[coords.index(edge.edge[0])][coords.index(edge.edge[1])] = edge.dist
        matrix[coords.index(edge.edge[1])][coords.index(edge.edge[0])] = edge.dist

    mst(coords, matrix)


def mst(vertices: list, matrix: list):
    """Gets the minimum spanning tree using Prim's algorithm."""
    key = [sys.maxsize] * len(vertices) # List of large number, so we can replace them with the actually weights later
    parent = [None] * len(vertices)  # Array to store constructed MST

    key[0] = 0  # 0 so this vertex is picked first
    mstSet = [False] * len(vertices)    # Keeps track of vertices already in the MST

    parent[0] = -1  # First node is always the root of

    for i in range(len(vertices)):

        u = minKey(vertices, key, mstSet)   # Pick a vertex that's not in mstSet and has min value key

        mstSet[u] = True    # Put vertex in the MST tree

        for v in range(len(vertices)):

            # Key updates if graph[u][v] is smaller than key[v] and vertex mstSet[v] isn't in the mst
            if 0 < matrix[u][v] < key[v] and mstSet[v] == False:
                key[v] = matrix[u][v]
                parent[v] = u

    consoleOut(vertices, matrix, parent)


def minKey(vertices, key, mstSet):
    """Find vertex with min distance value out of the set of vertices not yet included in the MST tree."""
    min = sys.maxsize
    for v in range(len(vertices)):

        if key[v] < min and mstSet[v] == False:
            min = key[v]
            min_index = v

    return min_index


def consoleOut(vertices, matrix, parent):
    """Formats and outputs the information to the console."""
    totalWeight = 0
    global testCases
    for i in range(1, len(vertices)):

        totalWeight += matrix[i][parent[i]]

    print(f"Test case {testCases}: MST weight {totalWeight}\n")
    testCases += 1


def main():
    dataList = getData()
    getPoints(dataList)



if __name__ == "__main__":
    testCases = 1   # We'll count test cases by counting up after outputting the weights to console so start at 1
    main()


