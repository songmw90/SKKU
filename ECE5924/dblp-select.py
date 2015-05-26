import networkx as nx
from networkx.classes.graph import Graph
from networkx.algorithms import bipartite
import matplotlib.pyplot as plt
import operator

__author__ = "SDN and IoT"


#@func: get_k_highest_degree
#@param G : Data added graph
#@param k : Rank limit
#@desc: read Graph data and sort. print hightest degree limit k
def get_k_highest_degree(G, k):
    degree_dict = G.degree(G.nodes())
    degree_dict = sorted(degree_dict.items(), key=operator.itemgetter(1), reverse = True)
    count = 0
    for author in degree_dict:
        print str(author[0]) + ":" + str(author[1])
        count = count + 1
        if(count == k):
            break

#@func: export_degree_statistic
#@param G : Data added graph
#@desc: read Graph data and export degree to csv file
def export_degree_statistic(G):
    degree_list = list(G.degree(G.nodes()).values())
    max_degree = max(degree_list)
   
    outfile_csv =open("degree_stats.csv",'w')
    for i in range(max_degree + 1):
        outfile_csv.write(str(i) + ',' + str(degree_list.count(i)) + '\n')
    outfile_csv.close()

if __name__ == '__main__':
	B = nx.Graph()

	file = open('parsed_data.txt', 'r')

	authors = set()
	edgelist = []
	i = 0
	parse_limit = 1000000
	#data split to "||"
	#data of first is author and second is title
	#split data and add nodes
	for line in file:

		line = line.replace('\n','')
		tmp_node = line.split("||")
		try:
			B.add_node(tmp_node[0],bipartite=0)
			B.add_node(tmp_node[1],bipartite=1)
			edgelist.append((tmp_node[0],tmp_node[1]))
		except Exception,Err:
			pass
		# we found 2 range exception error in 1000000

		# proccessing element limit 1M
		if i >= parse_limit:
			break
		else:
			i += 1	

	file.close()

	#add edge list
	B.add_edges_from(edgelist)

	authors = set(n for n,d in B.nodes(data=True) if d['bipartite'] == 0)
	G = bipartite.projected_graph(B, authors)

	get_k_highest_degree(G, 10)
	export_degree_statistic(G)

	nx.draw(G)
	plt.figure(num=None, figsize=(20, 20), dpi=80)
	plt.savefig("degree_histogram.png")
	plt.show()
