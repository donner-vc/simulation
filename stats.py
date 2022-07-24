import constants as cons
import pandas as pd
import networkx as nx

# whole network
# Number of nodes 20508
# Number of edges 83427
# Total capacity 3286.94005544

# largest connected component
# Number of nodes 20178
# Number of edges 83253
# Total capacity 3283.96899504

# Dict containing occurrence of number of channels owned by entity. key -> number of channels owned, value -> occurrence
# For example 1: 9019 means there are 9019 entities with 1 channel
# {1: 9019, 2: 2673, 3: 1574, 4: 1094, 5: 751, 6: 574, 7: 442, 8: 351, 9: 331, 10: 265, 11: 214, 12: 182, 13: 189, 14: 146, 15: 117, 16: 122, 17: 113, 18: 88, 19: 81, 20: 73, 21: 78, 22: 85, 23: 67, 24: 61, 25: 62, 26: 60, 27: 50, 28: 39, 29: 29, 30: 32, 31: 33, 32: 36, 33: 35, 34: 22, 35: 29, 36: 26, 37: 31, 38: 19, 39: 21, 40: 22, 41: 11, 42: 16, 43: 17, 44: 18, 45: 18, 46: 12, 47: 15, 48: 9, 49: 16, 50: 10, 51: 9, 52: 18, 53: 13, 54: 10, 55: 17, 56: 7, 57: 11, 58: 7, 59: 12, 60: 11, 61: 10, 62: 9, 63: 5, 64: 6, 65: 8, 66: 9, 67: 8, 68: 8, 69: 6, 70: 6, 71: 9, 72: 8, 73: 5, 74: 2, 75: 6, 76: 6, 77: 5, 78: 5, 79: 5, 80: 3, 81: 5, 82: 2, 83: 3, 84: 3, 85: 2, 86: 4, 87: 3, 88: 3, 89: 6, 90: 4, 91: 2, 92: 7, 93: 4, 94: 2, 95: 2, 96: 5, 97: 6, 98: 3, 99: 3, 100: 5, 101: 3, 102: 3, 103: 1, 104: 3, 105: 2, 106: 2, 107: 2, 108: 1, 109: 1, 110: 3, 112: 1, 113: 3, 114: 2, 115: 1, 116: 2, 117: 1, 118: 1, 121: 1, 122: 2, 123: 1, 124: 2, 125: 1, 126: 1, 127: 3, 129: 2, 130: 3, 131: 1, 133: 2, 134: 3, 136: 3, 137: 1, 139: 1, 143: 2, 144: 3, 145: 2, 148: 1, 150: 1, 151: 1, 152: 1, 154: 1, 155: 2, 157: 2, 158: 1, 159: 3, 160: 1, 161: 2, 164: 1, 168: 1, 172: 1, 174: 2, 175: 2, 176: 1, 178: 2, 179: 1, 180: 1, 181: 1, 182: 1, 192: 1, 193: 1, 194: 1, 197: 1, 198: 2, 201: 1, 202: 1, 206: 1, 207: 1, 209: 2, 214: 1, 215: 1, 216: 2, 217: 1, 218: 1, 221: 1, 222: 1, 224: 1, 225: 2, 226: 1, 231: 2, 235: 3, 241: 1, 250: 2, 251: 1, 254: 2, 256: 1, 259: 1, 260: 1, 263: 1, 264: 1, 265: 1, 266: 1, 268: 1, 269: 1, 270: 1, 272: 2, 275: 1, 276: 1, 281: 1, 283: 1, 285: 1, 295: 1, 296: 1, 300: 1, 301: 1, 309: 1, 317: 1, 320: 1, 325: 1, 332: 1, 337: 1, 345: 1, 350: 1, 351: 1, 352: 1, 353: 1, 354: 1, 356: 1, 358: 1, 389: 1, 409: 1, 410: 2, 412: 1, 449: 1, 472: 1, 481: 1, 487: 1, 488: 1, 496: 1, 498: 1, 503: 1, 505: 1, 513: 1, 518: 1, 544: 1, 566: 1, 577: 1, 578: 1, 614: 1, 637: 1, 640: 1, 738: 1, 752: 1, 787: 1, 809: 1, 837: 1, 849: 1, 879: 1, 1005: 1, 1119: 1, 1179: 1, 1209: 1, 1274: 1, 1584: 1, 2011: 1, 2086: 1, 2379: 1, 3211: 1}

# These are the aliases with most channels: 
# ACINQ: 3211
# WalletOfSatoshi.com: 2379
# 1ML.com node ALPHA: 2086
# CoinGate: 2011
# OpenNode.com: 1584

channels = pd.read_csv(cons.CHANNELS_CSV)  # This csv comes from a snapshot from https://ln.fiatjaf.com/ from July 6, 2022

graph = nx.from_pandas_edgelist(channels, cons.NODE_A, cons.NODE_B, [cons.SATOSHIS, cons.BASE_FEE, cons.RELATIVE_FEE, cons.ALIAS_A, cons.ALIAS_B])
cc = sorted(nx.connected_components(graph), key=len, reverse=True)
graph = graph.subgraph(cc[0])

#print(nx.average_shortest_path_length(graph))

print(f'Number of nodes {len(graph.nodes)}')
print(f'Number of edges {len(graph.edges)}')

total = 0
for u,v,a in graph.edges(data=True):
    total += a[cons.SATOSHIS]

print(f'Total capacity {total/cons.SATOSHIS_IN_BTC}')