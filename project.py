import re
import csv
import sys

class Graph:
    def __init__(self, gdict=None):
        if gdict is None:
            gdict = {}
        self.gdict = gdict

    #calls find edges which returns all edges in graph
    def edges(self):
        return self.findedges()

    #Adds edge if not already in Graph
    def addEdge(self, edge):
        if edge[0] in self.gdict:
            self.gdict[edge[0]].append(edge[1])
        else:
            self.gdict[edge[0]] = [edge[1]]

    #adds the vertex if not already in the graph
    def addVertex(self, vrtx):
        if vrtx not in self.gdict:
            self.gdict[vrtx] = []

    #returns all the edges in the graph
    def findedges(self):
        edgename = []
        for vrtx in self.gdict:
            for nxtvrtx in self.gdict[vrtx]:
                if {nxtvrtx, vrtx} not in edgename:
                    edgename.append({vrtx, nxtvrtx})
        return edgename
    #finds if there is a relation between 2 people, if there is print the shrotest one
    #if there isn't hen print there isn't any relation between 2 people
    def findShortestPath(self, source, destination):
        return self.BFS(source,destination);

    #helper function that finds the shortest path between 2 people
    def BFS(self, source, destination):
        visited = {};
        destLength = {};
        queue = []
        if source not in self.gdict:
            return -1;

        visited[source] = True;
        destLength[source] = 0;
        queue.append(source);

        while queue:
            source = queue.pop(0);

            for i in self.gdict[source]:
                if i not in visited:
                    destLength[i] = destLength[source] + 1;
                    queue.append(i)
                    visited[i] = True
                if (i == destination):
                    return destLength[source] + 1;

        return -1;


with open('movie_metadata.csv', encoding="utf-8") as csv_file:
    arguments = [];
    for i in range(1,len(sys.argv)):
        arguments.append(int(sys.argv[i]))
    graph = Graph()
    csv_reader = csv.reader(csv_file, delimiter=',')
    print("default movie_metadata.csv args are 10, 6, 14")
    for row in csv_reader:
        #row[6] = actor 2, row[10] = actor 1, row[14] = actor 3
        for relations in arguments:
            if (row[relations] is not None):
                graph.addVertex(row[relations].lower())
            for relationEdge in arguments:
                if(row[relations] != row[relationEdge] and row[relationEdge] is not None and row[relations] is not None):
                    edge = [row[relations].lower(), row[relationEdge].lower()]
                    graph.addEdge(edge)

    
    graph_erdos = Graph();
    graph.addVertex("erdos, paul")
    erdos_text = open("Erdos1.txt", "r")
    next_line = True;
    dependency = "";
    for line in erdos_text:
        line_split = re.split('\W+', line.strip().replace("*", ""))
        if line.strip() == '':
            next_line = True
        elif next_line:
            name = line_split[0] + ', '
            name += line_split[1] + ' '
            if line_split[2].isdigit() is False:
                name += line_split[2]
            name = name.strip().lower()
            edge = ["erdos, paul", name]
            edge2 = [name, "erdos, paul"];
            graph_erdos.addEdge(edge)
            graph_erdos.addEdge(edge2)
            dependency = name
            next_line = False
        else:
            if len(line_split) == 1:
                name = line_split[0];
            else:
                name = line_split[0] + ', '
                name += line_split[1] + ' '
            if len(line_split) >= 3:
                name += line_split[2];
            name = name.strip().lower();
            edge = [dependency, name]
            edge2 = [name, dependency]
            graph_erdos.addVertex(name)
            graph_erdos.addEdge(edge)
            graph_erdos.addEdge(edge2)
            




    first_person = input("first person: ").lower()
    second_person = input("seocnd person: ").lower()
    actor_dest = graph.findShortestPath(first_person, second_person);
    if (actor_dest == -1):
        print("Atleast one of these people are not actors, or they were not the top 3 stars of any given movie")
    else:
        print("They have ", end = " "); print(actor_dest, end = " "); print("relations");
    erdos_number = graph_erdos.findShortestPath(first_person, second_person);
    if (erdos_number == -1):
        print("These 2 people have no papers together");
    else:
        print("They have ", end = " "); print(erdos_number, end = " "); print("relation papers");
