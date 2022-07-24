import constants as cons
import pandas as pd
import networkx as nx
from typing import List

# whole network
# Number of nodes 20508
# Number of edges 83427
# Total capacity 3286.94005544

# largest connected component
# Number of nodes 20178
# Number of edges 83253
# Total capacity 3283.96899504

def main():

    channels = pd.read_csv(cons.CHANNELS_CSV)  # This csv comes from a snapshot from https://ln.fiatjaf.com/ from July 6, 2022

    graph = nx.from_pandas_edgelist(channels, cons.NODE_A, cons.NODE_B, [cons.SATOSHIS, cons.BASE_FEE, cons.RELATIVE_FEE, cons.NODE_A, cons.NODE_B, cons.ALIAS_A, cons.ALIAS_B])
    cc = sorted(nx.connected_components(graph), key=len, reverse=True)
    graph = graph.subgraph(cc[0])

    alias_list = channels['aliasA'].to_list()
    alias_list = alias_list + channels['aliasB'].to_list()

    G = nx.Graph(graph)
    
    num_edges_beginning = len(G.edges) # 83253

    alias_sample = []
    # Select all nodes with at least 2 edges, get their alias
    for node in G.nodes:
        aliasA = list(channels.loc[channels['nodeA'] == node]['aliasA'].to_dict().values())
        aliasB = list(channels.loc[channels['nodeB'] == node]['aliasB'].to_dict().values())
        if len(aliasA) + len(aliasB) < 2:
            continue
        if len(aliasA)>0:
            alias_sample.append(aliasA[0])
        else:
            alias_sample.append(aliasB[0])
    alias_sample = list(set(alias_sample))
    

    #print(alias_sample)
    print('alias,channels_closed')

    ########### How many edges can be closed?
    total_closed = 0
    for alias in alias_sample:
        if str(alias) == 'nan': # Some nodes don't have an alias, we disregard them
            continue
        alias_nodes = nodes_of_alias_in_graph(alias, channels, G)
        # This is if the alias has one node
        if len(alias_nodes) == 1:
            startnode = list(alias_nodes)[0]
            paths_left = True
            while True:
                num_edges = len(G.edges)
                # print(len(G.edges))
                try:
                    paths = nx.cycle_basis(G, root=startnode)
                except KeyError:
                        pass # cana happen if node in disconnected component, which we pruned
                if len(paths) < 1:
                    break
                paths.sort(key=len, reverse=True)
                i=0
                longest_path = paths[0]
                while longest_path[len(longest_path)-1] != startnode:
                    i+=1
                    if (i > len(paths)-1):
                        paths_left = False
                        break
                    longest_path = paths[i]
                if not paths_left:
                    break
                G.remove_edges_from(path_to_edgelist(longest_path, startnode))
        # This is if the alias has multiple nodes
        elif len(alias_nodes) > 1:
            paths_left = True
            while True:
                num_edges = len(G.edges)
                paths = []
                for startnode in alias_nodes:
                    try:
                        paths = paths + nx.cycle_basis(G, root=startnode)
                    except KeyError:
                        pass # can happen if node in disconnected component, which we pruned
                # In this heuristic, we consider paths to the same node
                # for pair in itertools.combinations(alias_nodes, r=2):
                #     try:
                #         path = next(nx.all_simple_paths(G, source=pair[0], target=pair[1]))
                #         paths.append(path)
                #     except StopIteration:
                #         pass
                if len(paths) < 1:
                    break
                paths.sort(key=len, reverse=True)
                i=0
                longest_path = paths[0]
                while longest_path[len(longest_path)-1] != startnode:
                    i+=1
                    if (i > len(paths)-1):
                        paths_left = False
                        break
                    longest_path = paths[i]
                if not paths_left:
                    break
                G.remove_edges_from(path_to_edgelist(longest_path, startnode))
        else:
            raise ValueError('alias cannot have fewer than 1 node')
        #print(f'For alias {alias} there are {num_edges_beginning}-{num_edges}={num_edges_beginning-num_edges} edges closed')
        print(f'{str(alias).replace(",",";")},{num_edges_beginning-num_edges}')
        total_closed += num_edges_beginning-num_edges
        G = nx.Graph(graph)
    #print(f'Average edges closed: {total_closed/len(alias_sample)}')


def path_to_edgelist(path: List[int], startnode):
    if len(path) < 1:
        return []
    edgelist = []
    edgelist.append((startnode, path[0]))
    assert path[len(path)-1] == startnode
    for i in range(1,len(path)):
        edgelist.append((path[i-1],path[i]))
    return edgelist
        
def nodes_of_alias_in_graph(alias: str, channels: pd.DataFrame, G: nx.graph):
    node_list = channels.loc[(channels['aliasA'] == alias)]['nodeA'].to_list()
    node_list = node_list + channels.loc[(channels['aliasB'] == alias)]['nodeB'].to_list()
    node_set = set(node_list)
    return_list = []
    for node in node_set:
        if node in G.nodes:
            return_list.append(node)
    return return_list

if __name__ == "__main__":
    main()
