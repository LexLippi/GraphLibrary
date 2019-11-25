from task.graph_library.graph_factory import GraphFactory
import re


REGEX_NUMBERS = re.compile(r'[\d|\*]+')
REGEX_TITLE = re.compile(r'\b\w+\b')
REGEX_ADJACENCY_LIST = re.compile(r'[\s|:]+')


class Parser:
    @staticmethod
    def _graph_adjacency_matrix_read(node_count, matrix, line):
        """
        Функция принимает строки матрицы смежности графа и переводит строковое
        представление матрицы в матрицу смежности.
        """
        numbers = list(map(lambda value: None if value == '*' else int(value),
                           REGEX_NUMBERS.findall(line)))
        matrix.append(numbers)
        return max(node_count, len(numbers), len(matrix))

    @staticmethod
    def _graph_adjacency_list_read(node_count, matrix, line):
        """
        Функция принимает строки списка смежности графа и переводит строковое
        представление списка в матрицу смежности.
        """
        node, *numbers = list(map(int, REGEX_ADJACENCY_LIST.split(line)))
        while len(matrix) <= node:
            matrix.append([None for _ in range(node_count)])
        for i in range(0, len(numbers), 2):
            while len(matrix[node - 1]) <= numbers[i] - 1:
                matrix[node - 1].append(None)
            matrix[node - 1][numbers[i] - 1] = numbers[i + 1]
        return max(node_count, int(len(numbers) / 2), node)

    @staticmethod
    def _graph_edge_list_read(node_count, matrix, line):
        """
        Функция принимает строки списка смежности графа и переводит строковое
        представление списка в матрицу смежности.
        """
        first_node, second_node, weight = tuple(
            map(int, REGEX_NUMBERS.findall(line)))
        while len(matrix) <= first_node:
            matrix.append([None for _ in range(node_count)])
        while len(matrix[first_node - 1]) <= second_node - 1:
            matrix[first_node - 1].append(None)
        matrix[first_node - 1][second_node - 1] = weight
        return max(node_count, first_node, second_node)

    @staticmethod
    def read(file):
        """
        Функция считывает входной файл и возвращает граф.
        """
        title = frozenset(map(lambda value: value.casefold(),
                              REGEX_TITLE.findall(file[0])))
        file = file[1:]
        node_count = 0
        matrix = []
        if 'adjmat' in title:
            for line in file:
                node_count = Parser._graph_adjacency_matrix_read(node_count,
                                                                 matrix, line)
        elif 'adjlist' in title:
            for line in file:
                node_count = Parser._graph_adjacency_list_read(node_count,
                                                               matrix, line)
        elif 'edlist' in title:
            for line in file:
                node_count = Parser._graph_edge_list_read(node_count,
                                                          matrix, line)
        else:
            return None
        for line in matrix:
            line.extend([None] * (node_count - len(line)))
        weighted = 'w' in title
        ordered = 'o' in title
        return GraphFactory.create_graph(node_count, matrix, weighted, ordered)
