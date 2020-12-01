import sys
import random
import heapq


class Graph(object):
    def __init__(self, digraph=False):
        self.digraph = digraph
        self.nodes_dict = {}
        self.edges_dict = {}

    def add_node(self, node):

        if node not in self.nodes_dict:  # node not yet in graph
            # add it to node dictionary and attach an empty set of adjacent nodes
            self.nodes_dict[node] = set()

    def add_edge(self, from_node, to_node, weight):
        # add an edge with given weight
        self.edges_dict[(from_node, to_node)] = weight
        # add connection reference to nodes
        self.nodes_dict[from_node].add(to_node)

        if not self.digraph:  # if not digraph
            # add edge connecting node in other direction
            self.edges_dict[(to_node, from_node)] = weight
            # add connection reference to other node
            self.nodes_dict[to_node].add(from_node)

    def remove_edge(self, from_node, to_node):
        # delete edge from dictionary of edges
        del self.edges_dict[(from_node, to_node)]
        # remove connection reference from node
        self.nodes_dict[from_node].remove(to_node)

        if not self.digraph:  # if not a digraph
            # delete edge in other direction
            del self.edges_dict[(to_node, from_node)]
            # remove connection reference from other node
            self.nodes_dict[to_node].remove(from_node)

    def remove_node(self, del_node):
        for node in self.nodes_dict:  # for each node
            # if node to be deleted is connected
            if del_node in self.nodes_dict[node]:
                self.remove_edge(node, del_node)  # delete connecting edge

        # for each node that can be reached from deleted node
        for adj in self.nodes_dict[del_node]:
            self.remove_edge(del_node, adj)  # remove connecting edge

        del self.nodes_dict[del_node]  # delete the node

    def print_adj_list(self):
        print('Digraph ' if self.digraph else 'Graph ',
              end='')  # print if graph or digraph
        print('Adjacency List:')
        for node, adj_set in self.nodes_dict.items():  # for each node in dictionary
            print(str(node) + '--> ', end='')
            for adj_node in adj_set:
                # print each adjacent node and associated weights
                print('['+str(adj_node) + ':' +
                      str(self.edges_dict[node, adj_node])+']', end=' ')
            print('')

    def is_connected(self):
        if len(self.nodes_dict) < 1:
            return False
        visited = []
        if not self.digraph:  # if graph
            # randomly select node
            rand = random.choice(list(self.nodes_dict.keys()))
            return self.check_connections(rand, visited)  # check connections
        # if digraph
        connected = []
        for node in self.nodes_dict.keys():  # for every node
            visited.clear()  # clear visited
            if not self.check_connections(node, visited):  # check connections
                return False
        return True  # return true only if strongly connected

    def check_connections(self, node, visited):
        visited.append(node)  # add given node to list of visited
        if len(visited) == len(self.nodes_dict):  # if visited contains all nodes in graph
            return True  # return true
        for adj in self.nodes_dict[node]:  # for each node
            if adj not in visited:  # if node is in visited
                # check connections of that node recursively
                if self.check_connections(adj, visited):
                    return True  # return true if all nodes in graph were visited
        return False  # if nodes were not all able to be visited return false
