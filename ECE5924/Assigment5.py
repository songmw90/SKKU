import networkx as nx
from networkx.classes.graph import Graph
from math import radians, cos, sin, asin, sqrt
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
    
    #@func: get the dictionary of nodes in graph
    #       this dictionary helps us drawing the graph with absolutely coordinate 
    #@return a dictionary
    #@desc: we create the dictionary of all node in graph
    #       with key is the node and value is coordinate of node
    def get_node_dict(self):
        pos = {}
        for node in self.nodes():
            pos[node] = (self.node[node]["Longitude"], self.node[node]["Latitude"])
        return pos
#@func: calculate haversine distance between 2 points
#@param lon1, lat1, lon2, lat2: longitude and latitude of 2 points, respectively
#@return haversine distance
#@desc: Calculate the great circle distance between two points 
#       on the earth (specified in decimal degrees)
def haversine(lon1, lat1, lon2, lat2):
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6371 # Radius of earth in kilometers. Use 3956 for miles
    return c * r
#@func: caculate and set attributes for edges
#@param G: the graph G
#@desc: Calculate and set haversine distance, capacity, flow (= 0) for each edge in G
def set_edge_attributes(G):
    max_dist = 0;
    for edge in G.edges():
        u = G.node[edge[0]]
        v = G.node[edge[1]]
        edge_attr = G.get_edge_data(edge[0], edge[1])
        dist = haversine(u["Longitude"], u["Latitude"], v["Longitude"], v["Latitude"])
        if(dist > max_dist):
            max_dist = dist
        edge_attr["distance"] = dist
        if dist >= 0 and dist < 1000:
            edge_attr["capacity"] = 100
        elif dist >= 1000 and dist < 2000:
            edge_attr["capacity"] = 200
        else:
            edge_attr["capacity"] = 300
        edge_attr["flow"] = 0
        G.remove_edge(edge[0], edge[1])
        G.add_edge(edge[0], edge[1], edge_attr)
#@func: draw MST with solid line, remaining edges with dotted line
#       we also print the total distance of this MST
#@param G: the graph G
#@desc: we get the graph which is created by MST, then draw it with solid style
#       then we calculate the total distance of all edges in MST and hide all these edges in G
#       finally we draw G with dotted style
def draw_MST_Graph(G):
    total_distance = 0
    MST_G = nx.minimum_spanning_tree(G)
    MST_G.__class__ = NewGraph
    
    pos = MST_G.get_node_dict()
    nx.draw_networkx(MST_G, pos, False)
    
    MST_edges = nx.minimum_spanning_edges(G)
    for edge in MST_edges:
        edge_attr = G.get_edge_data(edge[0], edge[1])
        total_distance += edge_attr["distance"]
        G.hide_edge(edge[0], edge[1])
    print(total_distance)
    pos = G.get_node_dict()
    nx.draw_networkx(G, pos, False, style="dotted")
    G.show_all_edges()
    plt.show()
#@func: process all demands from demand list, write the demand and shortest path to csv file
#@param list_demands: the demand list
#@param G: the graph G
#@desc: for each demand we will process that demand by calling function execute_demand
#       if there is a shortest path between source and target, we write this demand and shortest
#       path into csv file, if not then we print the number of processed demand and close csv file
def process_List_Demands(list_demands, G):
    count = 0
    outfile_csv =open("output.csv",'w')
    outfile_csv.write("Order, Source, Target, Bandwidth, Shortest path \n")
    for demand in list_demands:
        if len(demand) != 4:
            print "Wrong data!!!"
            break
        else:
            source = int(demand[1])
            target = int(demand[2])
            bandwidth = float(demand[3])
            shortest_path = execute_demand_version2(G, source, target, bandwidth)
            if len(shortest_path) != 0:
                str_shortest_path = '-'.join(map(str, shortest_path))
                str_shortest_path.replace('\n', "")
                outfile_csv.write(demand[0] + ", " + demand[1] + ", " + demand[2] + ", " + str(bandwidth) + ", " + str_shortest_path + '\n')
                count = count + 1
            else:
                outfile_csv.close()
                print count
                break
#@func: process a demand
#@param G: the graph G
#@param source: source node
#@param target: target node
#@param bandwidth: the bandwidth of demand
#@return shortest path
#@desc: if there is a path between source and target, we find the shortest path
#       if this path is valid (all edges has remaining capacity greater or equal bandwidth)
#       then for each edge in this shortest path, we update their flow
#       otherwise we return an empty list
def execute_demand(G, source, target, bandwidth):
    shortest_path = []
    if(nx.has_path(G, source, target)):
        shortest_path = nx.shortest_path(G, source, target, "distance")
        if(check_is_valid_shortest_path(G, shortest_path, bandwidth) == True):
            for i in range(len(shortest_path)-1):
                edge_attr = G.get_edge_data(shortest_path[i], shortest_path[i+1])
                edge_attr["flow"] = edge_attr["flow"] + bandwidth
                G.remove_edge(shortest_path[i], shortest_path[i+1])
                G.add_edge(shortest_path[i], shortest_path[i+1], edge_attr)
            return shortest_path
        else:
            shortest_path = []
    return shortest_path
#@func: check if a path is valid
#@param G: the graph G
#@param shortest_path: the shortest_path will be checked
#@param bandwidth: the bandwidth of demand
#@return True if this path is valid, otherwise return False
#@desc: we will check if all edge in this path has remaining capacity greater or equal bandwidth 
#       if yes then return True, else return False
def check_is_valid_shortest_path(G, shortest_path, bandwidth):
    for i in range(len(shortest_path)-1):
        edge_attr = G.get_edge_data(shortest_path[i], shortest_path[i+1])
        if edge_attr["capacity"] - edge_attr["flow"] < bandwidth:
            return False
    return True

#@func: process a demand
#@param G: the graph G
#@param source: source node
#@param target: target node
#@param bandwidth: the bandwidth of demand
#@return shortest path
#@desc: first we hide all edges which have the remaining capacity less than bandwidth
#       if there is a path between source and target, we find the shortest path
#       for each edge in this shortest path, we update their flow
#       then we show all hidden edges and return the shortest path 
def execute_demand_version2(G, source, target, bandwidth):
    shortest_path = []
    for edge in G.edges():
        edge_attr = G.get_edge_data(edge[0], edge[1])
        if edge_attr["capacity"] - edge_attr["flow"] < bandwidth:
            G.hide_edge(edge[0], edge[1])
    if(nx.has_path(G, source, target)):
        shortest_path = nx.shortest_path(G, source, target, "distance")
        for i in range(len(shortest_path)-1):
            edge_attr = G.get_edge_data(shortest_path[i], shortest_path[i+1])
            edge_attr["flow"] = edge_attr["flow"] + bandwidth
            G.remove_edge(shortest_path[i], shortest_path[i+1])
            G.add_edge(shortest_path[i], shortest_path[i+1], edge_attr)
    G.show_all_edges()
    return shortest_path
#@func: calculate the mean, variance, minimum and maximum flow in G
#@param G: the graph G
#@return a list contain the mean, variance, minimum and maximum flow 
def mean_variance_min_max_of_flow(G):
    min_flow, max_flow, total_flow, mean, variance = 300, 0, 0, 0, 0
    for edge in G.edges():
        edge_attr = G.get_edge_data(edge[0], edge[1])
        if  edge_attr["flow"] < min_flow:
            min_flow = edge_attr["flow"]
        if edge_attr["flow"] > max_flow:
            max_flow = edge_attr["flow"]
        total_flow += edge_attr["flow"]
    mean = total_flow/float(len(G.edges()))
    
    total_square_diff = 0
    for edge in G.edges():
        total_square_diff += (mean - edge_attr["flow"])**2
    variance = total_square_diff/float(len(G.edges()))

    return [mean, variance, min_flow, max_flow]
#@func: calculate the percentage of capacity used
#@param G: the graph G
#@return the percentage of capacity used
def percentage_of_capacity_used(G):
    total_capacity, total_flow = 0, 0
    for edge in G.edges():
        edge_attr = G.get_edge_data(edge[0], edge[1])
        total_capacity += edge_attr["capacity"]
        total_flow += edge_attr["flow"]
    return round(100 * total_flow/float(total_capacity), 2)
#@func: get links which have not been used
#@param G: the graph G
#@return the list of edge
def link_never_been_used(G):
    list_link = []
    for edge in G.edges():
        edge_attr = G.get_edge_data(edge[0], edge[1])
        if edge_attr["flow"] == 0:
            list_link.append(edge)
    return list_link
#@func: get links which carry no less than x% of capacity (more than x%)
#@param G: the graph G
#@param percent: the percent will be calculate
#@return the list of edges
def link_carry_no_less_than_x_percent_of_capacity(G, percent):
    list_link = []
    for edge in G.edges():
        edge_attr = G.get_edge_data(edge[0], edge[1])
        if round(100 * edge_attr["flow"]/ edge_attr["capacity"], 2) >= percent:
            list_link.append(edge)
    return list_link
#@func: draw the graph with flow information
#@param G: the graph G
def draw_Graph_With_Flow(G):
    pos = G.get_node_dict()    
    nx.draw(G,pos)
    edge_labels=dict([((u,v,),d['flow'])
             for u,v,d in G.edges(data=True)])
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

    plt.show()
#@func: read AttDemands file
#@param filename: the file name
#@return the list of demands
def read_AttDemands_File(filename):
    list_demands = []
    infile = open(filename, 'r')
    for line in infile:
        list_vals = str(line).split(", ")
        if len(list_vals) == 4:
            list_demands.append(list_vals)
        else:
            break
    infile.close()
    print(len(list_demands))
    return list_demands

if __name__ == '__main__':
    G = nx.read_gml("AttMpls.gml")
    G.__class__ = NewGraph
    
    set_edge_attributes(G)
    draw_MST_Graph(G)
    
    list_demands = read_AttDemands_File("AttDemands.csv")
    process_List_Demands(list_demands, G)
    draw_Graph_With_Flow(G)
    
    m_v_m_m_vals = mean_variance_min_max_of_flow(G)
    print(m_v_m_m_vals)
    
    capcity_used = percentage_of_capacity_used(G)
    print(capcity_used)
    
    never_used_links = link_never_been_used(G)
    print(never_used_links)
    
    over_70_percent_capacity_links = link_carry_no_less_than_x_percent_of_capacity(G, 70)
    print(over_70_percent_capacity_links)
