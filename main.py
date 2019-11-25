import csv
import random
from graph_generator import GraphGenerator
import argparse
import sys
from task.graph_library.graph_parser import Parser
from task.graph_library.graph_algo import BaseGraphAlgorithms
from task.graph_library.tester import Tester

NUMBER_OF_TESTS = 100
NODE_COUNT = 1
STEP = 5


def get_args():
    argument_parser = argparse.ArgumentParser(
        description='This program is module that can find paths in graph '
                    'with four different algorithms. To use the help input '
                    '--help')
    argument_parser.add_argument('-a', '--algorithm', type=str,
                                 help='name of testing algorithm')
    argument_parser.add_argument('--start', type=int,
                                 help='start node for algo')
    argument_parser.add_argument('--end', type=int,
                                 help='end node for algo')
    argument_parser.add_argument('-i', '--input', default=None,
                                 help='name of input file')
    argument_parser.add_argument('-o', '--output', default=None,
                                 help='name of output file')
    argument_parser.add_argument('-t', '--testing', action='store_true')
    return argument_parser.parse_args()


def pretty_input(input_name):
    if input_name is not None:
        with open(input_name) as f:
            graph = Parser.read(f)
    else:
        graph = Parser.read(sys.stdin)
    return graph


def pretty_output(out, algorithm, graph, start, end):
    for class_algo in BaseGraphAlgorithms.__subclasses__():
        if algorithm == class_algo.__name__:
            data = class_algo.find_path(graph, start, end)
            with (open(out) if out else sys.stdout) as f:
                print(data, file=f)


def get_test_result(filename, full_graph=False, chain_graph=False):
    columns = ['Count of nodes', 'BFS average time', 'BFS delta time',
               'BFS memory', 'DFS average time', 'DFS delta time',
               'DFS memory', 'Dijkstra average time', 'Dijkstra delta time',
               'Dijkstra memory', 'Ford-Bellman average time',
               'Ford-Bellman delta time', 'Ford-Bellman memory',
               'A_Star average time', 'A_Star delta time', 'A_Star memory']
    with open(filename, 'w', newline='') as file:
        writer = csv.DictWriter(file, dialect=csv.excel_tab(),
                                fieldnames=columns)
        writer.writeheader()
        tester = Tester()
        for i in range(NUMBER_OF_TESTS):
            if not chain_graph:
                start_node = random.randint(0, NODE_COUNT + STEP * i - 1)
                finish_node = random.randint(0, NODE_COUNT + STEP * i - 1)
            else:
                start_node = 0
                finish_node = NODE_COUNT + STEP * i - 1
            base_graph_generator = GraphGenerator(
                NODE_COUNT + STEP * i, False, False, full_graph, chain_graph)
            graph = base_graph_generator.generate_graph()
            weighted_ordered_graph_generator = GraphGenerator(
                NODE_COUNT + STEP * i, True, True, full_graph, chain_graph)
            weighted_graph = weighted_ordered_graph_generator.generate_graph()
            negative_weighted_graph_generator = GraphGenerator(
                NODE_COUNT + STEP * i, True, True, full_graph, chain_graph,
                negative_weighted=True)
            negative_weighted_graph = (
                negative_weighted_graph_generator.generate_graph())
            planar_graph_generator = GraphGenerator(
                NODE_COUNT + STEP * i, True, True, chain_graph=chain_graph,
                planar=True)
            planar_graph = planar_graph_generator.generate_graph()
            result_line = tester.get_test_line(
                NODE_COUNT + STEP * i, start_node, finish_node, graph,
                weighted_graph, planar_graph, negative_weighted_graph)
            writer.writerow(result_line)


def main():
    args = get_args()
    if args.testing:
        get_test_result('random_100.xls')
        get_test_result('full_graph_100.xls', full_graph=True)
        get_test_result('chain_graph_100.xls', chain_graph=True)
    else:
        graph = pretty_input(args.input)
        pretty_output(
            args.out, args.algorithm.capitalize(), graph, args.start, args.end)


if __name__ == "__main__":
    main()
