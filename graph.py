'''
    graphs.py
    Hannah Scooler, 12 October 2022

    A very simple unweighted Graph datatype. Each node consists entirely
    of a string (the node's name), and is stored as a key in a dictionary
    (self.adjacencies). The value associated with a node in this dictionary
    is a set of the names of the node's neighbors.

    Not much error handling, so if it crashes on you, feel free to add some
    exception handling of your own.

    Currently, this class supports:

        directed & undirected graphs
        printing to a simple adjacency list representation
            (more or less human-readable)
        export to the DOT graph description language
            https://en.wikipedia.org/wiki/DOT_(graph_description_language)
            draw the exports here: https://dreampuf.github.io/GraphvizOnline/
        import from a highly simplified version of DOT

    The super simple DOT subset that we're using looks like this:

        graph NameOfGraph {
            a -- b;
            b -- c;
            a -- c;
        }

    for a complete undirected graph. For the directed equivalent, the --'s would
    be ->'s, and the word "graph" would be replaced by "digraph". DOT has *many*
    more features, but that's all this Graph class supports.
'''

import re

class Graph:
    def __init__(self, dotfile=None, directed=False, name='G'):
        ''' Load from the specified dotfile, or initialize to the empty
            graph otherwise. The dotfile specification of whether this
            Graph object is directed overrides the directed parameter. '''
        self.directed = directed
        self.name = name
        self.adjacencies = {}
        if dotfile is not None:
            self._load_from_dotfile(dotfile)

    def _load_from_dotfile(self, dotfile):
        ''' Loads this Graph object from the specified dotfile. Assumes
            that this object has been initialized to empty before this method
            is called. '''
        with open(dotfile) as f:
            for line in f:
                if 'digraph' in line:
                    match = re.search(r'^\s*digraph\s+(\S+)\s*{', line)
                    if match:
                        self.name = match.group(1)
                        self.directed = True
                elif 'graph' in line:
                    match = re.search(r'^\s*graph\s+(\S+)\s*{', line)
                    if match:
                        self.name = match.group(1)
                        self.directed = False
                elif ('--' in line and not self.directed) or ('->' in line and self.directed):
                    match = re.search(r'^\s*(\S+)\s*-[->]\s*(\S+)\s*;', line)
                    if match:
                        u = match.group(1)
                        v = match.group(2)
                        self.add_node(u)
                        self.add_node(v)
                        self.add_edge(u, v)

    def __str__(self):
        s = f'[Graph {self.name}, directed: {self.directed}]\n'
        for node in sorted(self.adjacencies):
            s += f'{node}: ' + ', '.join(sorted(self.adjacencies[node])) + '\n'
        return s

    def to_dot(self):
        if self.directed:
            dot = 'digraph'
            arrow = '->' 
        else:
            dot = 'graph'
            arrow = '--' 
        dot += f' {self.name} {{\n'

        for node in sorted(self.adjacencies):
            if len(self.adjacencies[node]) == 0:
                dot += f'  {node};\n'
            else:
                for neighbor in self.adjacencies[node]:
                    if self.directed or node < neighbor:
                        dot += f'  {node} {arrow} {neighbor};\n'

        dot += '}\n'
        return dot

    def has_edge(self, u, v):
        return u in self.adjacencies and v in self.adjacencies[u]

    def add_node(self, node):
        if node not in self.adjacencies:
            self.adjacencies[node] = set()

    def add_nodes(self, nodes):
        for node in nodes:
            self.add_node(node)

    def add_edge(self, u, v):
        if u in self.adjacencies and v in self.adjacencies:
            self.adjacencies[u].add(v)
            if not self.directed:
                self.adjacencies[v].add(u)
        else:
            print(f'Trying to add edge ({u},{v}) between unrecognized nodes')

    def add_edges(self, edges):
        for u, v in edges:
            self.add_edge(u, v)

    def bfs_tree(self, start_node):
        ''' Returns a Graph with the same node set as this Graph instance,
            and with a subset of this Graph's edge set corresponding to
            the edges in a breadth-first search starting at start_node.

            Returns an empty Graph if this Graph is directed or if
            start_node is not in this Graph. '''
        return Graph(name='EmptyBFSTree')

    def dfs_tree(self, start_node):
        ''' Returns a Graph with the same node set as this Graph instance,
            and with a subset of this Graph's edge set corresponding to
            the edges in a depth-first search starting at start_node.

            Returns an empty Graph if this Graph is directed or if
            start_node is not in this Graph. '''
        return Graph(name='EmptyDFSTree')

    def topological_sort(self):
        ''' Returns a topologically sorted list of the nodes of this Graph.
            
            Returns an empty list if this Graph is not a DAG.
        '''
        return []

# Very simple-minded testing of Graph operations
def test_report(message, g):
    print(f'===== {message} =====')
    print(g)
    print('DOT format')
    print(g.to_dot())

def test_manual_construction():
    # Build a graph from scratch
    g = Graph(directed=True)
    g.add_nodes(['a', 'b', 'c', 'd'])
    g.add_edges([('a','b'), ('a','d'), ('c','b')])
    test_report('Graph initialized manually', g)

def test_from_dotfile(dotfile):
    g = Graph(dotfile=dotfile)
    test_report(f'Graph loaded from {dotfile}', g)

def test_traversals(dotfile, start_node):
    g = Graph(dotfile=dotfile)
    test_report(f'Graph loaded from {dotfile}', g)
    test_report(f'BFS tree from {start_node} for {g.name}', g.bfs_tree(start_node))
    test_report(f'DFS tree from {start_node} for {g.name}', g.dfs_tree(start_node))

def test_topological_sort(dotfile):
    g = Graph(dotfile=dotfile)
    test_report(f'Graph loaded from {dotfile}', g)
    print(f'Topological sort: {g.topological_sort()}')

if __name__ == '__main__':
    test_manual_construction()
    test_from_dotfile('undirected.dot')
    test_from_dotfile('directed.dot')
    test_traversals('undirected.dot', 'A')
    test_topological_sort('directed.dot')
