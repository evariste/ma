import os, sys, argparse, itertools
import pandas as pd
import networkx as nx
from fractions import Fraction

def main():

    args = usage()

    unit_from = args.unit_from
    unit_to = args.unit_to
    print_table = args.print_table


    unit_from = unit_from.lower()
    unit_to = unit_to.lower()

    df = pd.read_excel('english_length_units.xlsx')

    G = nx.DiGraph()

    for k, row in df.iterrows():
        node_A = row.unit_A
        node_B = row.unit_B
        mult = row.A_to_B

        G.add_edge(node_B, node_A, multiplier=Fraction(mult, 1))
        G.add_edge(node_A, node_B, multiplier=Fraction(1, mult))

    assert unit_to in G.nodes
    assert unit_from in G.nodes

    mult = get_multiplier(G, unit_to, unit_from)

    msg = f'To convert {unit_from} to {unit_to} multiply by {mult.numerator}'
    if mult.denominator > 1:
        msg += f'/{mult.denominator}'

    print(msg)

    if print_table:
        print_latex_table(G)


    return 0


def print_latex_table(G):

    node_list = sorted(G.nodes)
    n_nodes = len(node_list)

    print('\\begin{tabular}{', end='')
    print('|' + '|'.join((1+n_nodes) * ['c']) + '|}')

    columns = [' '] + [f'\\rotatebox{{90}}{{{n}}}' for n in node_list]
    print('\\hline')
    print(' & '.join(columns) + ' \\\\')
    print('\\hline')

    for j in range(n_nodes):
        if j % 5 == 0:
            print('\\hline')

        unit_from = node_list[j]

        print(f'{unit_from}', end='')

        for k in range(n_nodes):
            unit_to = node_list[k]

            mult = get_multiplier(G, unit_to, unit_from)

            print(f' & {mult} ', end='')

        print(' \\\\')
    print('\\hline')
    print('\\end{tabular}')






def get_multiplier(G, unit_to, unit_from):
    p = nx.dijkstra_path(G, unit_to, unit_from)

    mult = 1

    curr_node = p[0]
    for next_node in p[1:]:
        mult *= G.edges[(curr_node, next_node)]['multiplier']
        curr_node = next_node
    return mult

def usage():

    desc = 'Convert a length given in one unit to another (All are UK imperial length units).'
    parser = argparse.ArgumentParser(description=desc)

    parser.add_argument('unit_from', type=str, help='From unit')
    parser.add_argument('unit_to', type=str, help='To unit')

    parser.add_argument('-print_table', action='store_true', help='Print a table for all conversions.')
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    sys.exit(main())

