import networkx as nx
from networkx.classes.graph import Graph
import matplotlib.pyplot as plt
class NewGraph(Graph):
    hidden_nodes = {}
    hidden_edges = {}
    def __init__(self):
        Graph.__init__(self)
    
    #@func: hide a node
    #@param u: the node will be hidden
    #@desc: we move all edges connect to u into hidden_edges
    #       then we remove these edges from graph
    #       finally we move that node to hidden_nodes and remove it from graph
    def hide_node(self, u):
        for v in self.neighbors(u):
            hidden_edge = (u, v)
            edge_attr = self.get_edge_data(u, v)
            self.hidden_edges[hidden_edge] = edge_attr
            self.remove_edge(u, v)
        self.hidden_nodes[u] = self.node[u]
        self.remove_node(u)
        
    #@func: show a node
    #@param u: the node will be restored
    #@desc: we search in hidden_nodes
    #       if there is a node equal to u, we pop that node
    #       then we add this node to graph   
    def show_node(self, u):
        for v in self.hidden_nodes:
            if v == u:
                attr_u = self.hidden_nodes.pop(v)
                self.add_node(u, attr_u)
    
    #@func: show all node
    #@desc: for each node in hidden_nodes
    #       we get attribute of that node and add this node to graph  
    def show_all_nodes(self):
        for v in self.hidden_nodes:
            attr_v = self.hidden_nodes[v]
            self.add_node(v, attr_v)
        self.hidden_nodes.clear()
    
    #@func: hide an edge
    #@param u, v: the nodes that create the hidden edge
    #@desc: we get attribute of the edge
    #       then we add this edge to hidden_edge
    #       finally we remove edge from graph
    def hide_edge(self, u, v):
        hidden_edge = (u, v)
        edge_attr = self.get_edge_data(u, v)
        self.hidden_edges[hidden_edge] = edge_attr
        self.remove_edge(u, v)
    
    #@func: show an edge
    #@param u, v: the nodes of the restored edge
    #@desc: if the node of this edge is hidden, we will show this node
    #       after that we get the attribute of the edge and remove it from hidden_edges
    #       then we add this edge to graph   
    def show_edge(self, u, v):
        if self.has_node(u) == False:
            self.show_node(u)
        if self.has_node(v) == False:
            self.show_node(v)
        edge_attr = self.hidden_edges.pop((u, v))
        self.add_edge(u, v, edge_attr)
    
    #@func: show all edges
    #@desc: for each edge in hidden_edges
    #       if the node of this edge is hidden, we will show this node
    #       we get attribute of that edge and add this edge to graph  
    def show_all_edges(self):
        for edge in self.hidden_edges:
            if self.has_node(edge[0]) == False:
                self.show_node(edge[0])
            if self.has_node(edge[1]) == False:
                self.show_node(edge[1])
            edge_attr = self.hidden_edges[edge]
            self.add_edges_from([edge], edge_attr)
        self.hidden_edges.clear()
    
    #@func: hide all edges that cross the line parallel with coordinate axis
    #@param coor_type: the type of parallel axis (longitude or latitude)
    #@param value: the constant value of the line
    #@desc: we search edges which cross the line
    #       then we hide these edge   
    def hide_cross_edge(self, coor_type, value):
        for edge in self.edges():
            u = self.node[edge[0]]
            v = self.node[edge[1]]
            if (u[coor_type] <= value and v[coor_type] >= value) or (u[coor_type] >= value and v[coor_type] <= value):
                self.hide_edge(edge[0], edge[1])
    
    #@func: get the dictionary of nodes in graph
    #       this dictionary helps us drawing the graph with absolutely coordinate 
    #@return a dictionary
    #@desc: we create the dictionary of all node in graph
    #       with key is the node and value is coordinate of node
    def get_node_dict(self):
        pos = {}
        for node in self.nodes():
            pos[node] = (self.node[node]["longitude"], self.node[node]["latitude"])
        return pos

#@func: get the mean degree of graph 
#@param G: the graph
#@desc: we get total degree of all node then divide to number of nodes
def get_mean_degree_graph(G):
    total_degree = 0
    for degree in  G.degree(G.nodes()).values():
        total_degree += degree
    return total_degree/float(len(G.nodes()))

if __name__ == '__main__':
    G = nx.read_gexf("SN001.gexf")
    G.__class__ = NewGraph
    
    print("Number of edges in full graph: " + str(len(G.edges())))
    
    #draw the total graph
    pos = G.get_node_dict()
    nx.draw_networkx(G, pos, False)
    plt.show()
    
    #hide edges cross x = 150
    G.hide_cross_edge("longitude", 150)
    print("Number of edges in graph after hiding egdes which cross x=150: " + str(len(G.edges())))
    
    #get mean degree of all subgraph after hiding egdes which cross x=150
    graphs = list(nx.connected_component_subgraphs(G, True))
    for subgraph in graphs:
        print("Mean degree of subgraph: " + str(get_mean_degree_graph(subgraph)))
    
    #draw graph after hiding egdes which cross x=150
    pos = G.get_node_dict()
    nx.draw_networkx(G, pos, False)
    plt.show()
    
    #draw subgraph after hiding egdes which cross x=150
    for subgraph in graphs:
        pos = subgraph.get_node_dict()
        nx.draw_networkx(subgraph, pos, False)
        plt.show()

    #restore all hidden nodes and hidden edges
    G.show_all_nodes()
    G.show_all_edges()
    
    print("Number of edges after restoring all nodes and edges: " + str(len(G.edges())))
    
    #hide edges cross y = 150
    G.hide_cross_edge("latitude", 150)
    print("Number of edges after hiding egdes which cross y=150: " + str(len(G.edges())))
    
    #get mean degree of all subgraph after hiding egdes which cross y=150
    graphs = list(nx.connected_component_subgraphs(G, True))
    for subgraph in graphs:
        print("Mean degree of subgraph: " + str(get_mean_degree_graph(subgraph)))
    
    #draw graph after hiding egdes which cross y=150
    pos = G.get_node_dict()
    nx.draw_networkx(G, pos, False)
    plt.show()
    
    #draw subgraph after hiding egdes which cross y=150
    for subgraph in graphs:
        pos = subgraph.get_node_dict()
        nx.draw_networkx(subgraph, pos, False)
        plt.show()
    