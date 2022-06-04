import pandas as pd
import networkx as nx
from matplotlib import pyplot as plt
import imageio

df = pd.read_excel('english_length_units.xlsx')

G = nx.DiGraph()

for k, row in df.iterrows():
    G.add_edge(row.unit_B, row.unit_A, label=row.A_to_B)


def clean_name(n):
    n_clean = n.split(' ')
    n_clean = [fst.upper() + ''.join(rest) for fst, *rest in n_clean]
    return '\n'.join(n_clean)


x = { n: clean_name(n) for n in G.nodes}
nx.set_node_attributes(G, x, 'label')


G2 = nx.nx_agraph.to_agraph(G)
G2.layout(prog='dot', args="-Nshape=box -Efontsize=10 -Nfontname=sans -Efontname=sans -Ecolor=#646464 -Nstyle=rounded -Ncolor=#949494")
G2.draw()
G2.draw('english_length_units_viz.png')
G2.draw('english_length_units_viz.svg')

im = imageio.imread('english_length_units_viz.png')
plt.imshow(im)
plt.show()

print('Done')



