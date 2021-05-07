"""CSC111 Winter Final Project: Graphs and _Vertex class

DESCRIPTION:
===============================

This module contains the Graph class and the _Vertex class that are used alongside the main_display
file. There is also the load_emotions_graph that creates our graph from our csv file and the
edit_file function that edits the emotions.csv file. (see below) Additionally, there is the
recommend_coping_mechanism function that recommends a healthy coping mechanism for an inputted
unhealthy one and the edit_time_csv and read_time_csv that assist in editing the time.csv file to
keep track of the time that the user has engaged in unhealthy coping mechanisms. (see below)

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of instructors and TAs
from CSC111 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited.

This file is Copyright (c) Sophia Abolore, Michelle Chernyi, Emily Chang and Umayrah Chonee.
"""
from __future__ import annotations
import csv
from typing import Any
from typing import Optional
import random
import datetime
import pandas as pd


class _Vertex:
    """A vertex in a emotion app graph, used to represent an emotion, a description, a cause, an
    effect, a coping mechanism or a journal entry.

    Each vertex item is either an emotion, a description of an emotion, causes of an emotion,
    effects of an emotion, coping mechanism for an emotion or a journal entry for a specific emotion
    and coping mechanism. All are represented as strings, but kept as Any.

    Instance Attributes:
        - item: The data stored in this vertex, representing an emotion, a description, a cause, an
                effect, a coping mechanism or a journal entry.
        - kind: The type of this vertex: 'emotion' or 'description' or 'causes' or 'effects' or
                'coping mechanism' or 'journal'.
        - rate: The rating of the vertex: True or False, representing whether the user likes the
                vertex item or not.
        - neighbours: The vertices that are adjacent to this vertex.

    Representation Invariants:
        - self not in self.neighbours
        - all(self in u.neighbours for u in self.neighbours)
        - self.kind in {'emotion', 'description', 'causes', 'effects','coping mechanism', 'journal'}
    """
    item: Any
    kind: str
    rate: bool
    neighbours: set[_Vertex]

    def __init__(self, item: Any, kind: str, rate: bool) -> None:
        """Initialize a new vertex with the given item, kind and rate.

        This vertex is initialized with no neighbours.

        Preconditions:
            - kind in {'emotion', 'description', 'causes', 'effects','coping mechanism', 'journal'}
        """
        self.item = item
        self.kind = kind
        self.rate = rate
        self.neighbours = set()

    def change_rate(self, new_rate: bool) -> None:
        """
        Change the rate of self to the inputted rate (new_rate).
        """
        self.rate = new_rate


class Graph:
    """
    A graph used to represent an emotion app network.

    """
    # Private Instance Attributes:
    #     - _vertices:
    #         A collection of the vertices contained in this graph.
    #         Maps item to _Vertex object.
    _vertices: dict[Any, _Vertex]

    def __init__(self) -> None:
        """Initialize an empty graph (no vertices or edges)."""
        self._vertices = {}

    def add_vertex(self, item: Any, kind: str, rate: Optional[bool] = True) -> None:
        """Add a vertex with the given item and kind to this graph.

        The new vertex is not adjacent to any other vertices.
        Do nothing if the given item is already in this graph.

        Preconditions:
            - kind in {'emotion', 'description', 'causes', 'effects','coping mechanism', 'journal'}
        """
        if item not in self._vertices:
            self._vertices[item] = _Vertex(item, kind, rate)

    def add_edge(self, item1: Any, item2: Any) -> None:
        """Add an edge between the two vertices with the given items in this graph.

        Raise a ValueError if item1 or item2 do not appear as vertices in this graph.

        Preconditions:
            - item1 != item2
        """
        if item1 in self._vertices and item2 in self._vertices:
            v1 = self._vertices[item1]
            v2 = self._vertices[item2]

            v1.neighbours.add(v2)
            v2.neighbours.add(v1)
        else:
            raise ValueError

    def get_neighbour_by_kind(self, item: Any, kind: str) -> list:
        """Return a list of the neighbours of the given item.

        Note that the *items* are returned, not the _Vertex objects themselves.

        Raise a ValueError if item does not appear as a vertex in this graph.
        """
        if item in self._vertices:
            list_so_far = []
            v = self._vertices[item]
            for neighbour in v.neighbours:
                if neighbour.kind == kind:
                    list_so_far.append(neighbour.item)
            return list_so_far
        else:
            raise ValueError

    def get_neighbour_by_kind_rate(self, item: Any, rating: bool, kind: str) -> list:
        """
        Return a list of the neighbours of the given item based on the kind and rating.

        Note that the *items* are returned, not the _Vertex objects themselves.

        Raise a ValueError if item does not appear as a vertex in this graph.
        """
        if item in self._vertices:
            list_so_far = []
            v = self._vertices[item]
            for neighbour in v.neighbours:
                if neighbour.kind == kind and neighbour.rate == rating:
                    list_so_far.append(neighbour.item)
            return list_so_far
        else:
            raise ValueError

    def change_vertex_rate(self, item: Any, new_rate: bool) -> None:
        """
        Change the rate of the _Vertex with the inputted item.

        Raise a ValueError if item does not appear as a vertex in this graph.
        """
        if item in self._vertices:
            vertex = self._vertices[item]
            vertex.change_rate(new_rate)
        else:
            raise ValueError

    def get_all_vertices(self, kind: str = '') -> set:
        """Return a set of all vertex items in this graph.

        If kind != '', only return the items of the given vertex kind.

        Preconditions:
            - kind in {'', 'emotion', 'description', 'causes', 'effects','coping mechanism',
             'journal'}
        """
        if kind != '':
            return {v.item for v in self._vertices.values() if v.kind == kind}
        else:
            return set(self._vertices.keys())


def load_emotion_graph(emotions_file: str, journals_file: str) -> Graph:
    """Return an emotions graph corresponding to the given filepath that corresponds to a dataset.

    The emotions graph stores one vertex for each emotion/ description/ list of causes/
    list of effects/ coping mechanism. (one vertex for each coping mechanism)
    Each vertex stores as its item either emotion/ description/ list of causes/
    list of effects/ coping mechanism. Use the "kind" _Vertex attribute to differentiate
    between the different vertex types.

    Edges represent a connection between an emotion description/ list of causes/
    list of effects/ coping mechanism.

    The graph also contains the previous journal entries (added from the data/journal_entries.csv
    file)

    Preconditions:
        - emotions_file is the path to the emotions.csv file
    """
    emotions_graph = Graph()
    with open(emotions_file, encoding='utf-8') as csv_file:
        reader = csv.reader(csv_file)
        next(reader)

        # adding each row of the csv file
        for row in reader:
            emotions_graph.add_vertex(row[0], 'emotion')
            emotions_graph.add_vertex(row[1], 'description')
            emotions_graph.add_vertex(row[2], 'causes')
            emotions_graph.add_vertex(row[3], 'effects')
            if len(row) == 6 and row[5] != '':
                unhealthy = row[5].split(',')
                _add_unhealthy(unhealthy, emotions_graph, row)
            coping_mechanisms = row[4].split(',')

            # adding coping mechanisms separately
            for mechanism in coping_mechanisms:
                if mechanism not in emotions_graph.get_all_vertices('coping mechanism'):
                    emotions_graph.add_vertex(mechanism, 'coping mechanism')
                emotions_graph.add_edge(row[0], mechanism)
            for i in range(0, 4):
                emotions_graph.add_edge(row[0], row[i])

    # adding past journal entries taken from the data/journal_entries.csv file.
    with open(journals_file, encoding='utf-8') as csv_file:
        reader = csv.reader(csv_file)
        next(reader)

        for row in reader:
            emotions_graph.add_vertex(row[1], 'journal')
            emotions_graph.add_edge(row[0], row[1])

    return emotions_graph


def _add_unhealthy(unhealthy: list, emotions_graph: Graph, row: list) -> None:
    """
    Helper function: add unhealthy coping mechanism to the inputted graph, emotions_graph.
    """
    for mechanism in unhealthy:
        if mechanism not in emotions_graph.get_all_vertices('unhealthy'):
            emotions_graph.add_vertex(mechanism, 'unhealthy')
        emotions_graph.add_edge(row[0], mechanism)


def edit_file(file_name: str, healthy: list, emotion: str) -> None:
    """
    Add the inputted healthy coping mechanism that corresponds to the inputted emotion to the csv
    file with file_name as the path.

    Preconditions:
        - file_name is the path to the emotions.csv file
        - emotion in {'Sadness', 'Fear', 'Vulnerability', 'Exhaustion', 'Envy', 'Jealousy',
         'Anger', 'Stress', 'Anxiousness', 'Procrastination'}
    """
    file = pd.read_csv(file_name)
    index_list = file.index[file['Emotion'] == emotion].tolist()
    index = index_list[0]

    file.at[index, 'Coping Mechanisms'] = ','.join(healthy)

    file.to_csv(file_name, index=False)


def recommend_coping_mechanism(graph: Graph, unhealthy: str) -> str:
    """
    Return a random healthy coping mechanism for the unhealthy coping mechanism that is inputted.
    """
    emotion = graph.get_neighbour_by_kind(unhealthy, 'emotion')
    return random.choice(
        graph.get_neighbour_by_kind_rate(emotion[0], True, 'coping mechanism')).lower()


def edit_time_csv(started: bool, days: int, file_name: str) -> None:
    """
    Edit the file with path file_name: if started is True, edit the file to the current date, else
    does not edit to current date (disabled state)

    Precondition:
        - file_name is the path for the time.csv file.
    """
    file = pd.read_csv(file_name)
    if started is True:
        file.at[0, 'started'] = 'yes'
        file.at[0, 'past time'] = datetime.datetime.now().date()
        file.at[0, 'day'] = days
    else:
        file.at[0, 'started'] = 'no'
        file.at[0, 'past time'] = ''
        file.at[0, 'day'] = 0
    file.to_csv(file_name, index=False)


def read_time_csv(file_name: str) -> dict:
    """
    Return a dictionary where the key 'started' has corresponding item as the first entry in the
    file with path file_name, the key 'day' has corresponding item as the second entry in the file
    with path file_name and the key 'past time' has corresponding item as the third entry in the
    file with path file_name.

    Preconditions:
        - file_name is the path to the time.csv file
    """
    with open(file_name, encoding='utf-8') as csv_file:
        reader = csv.reader(csv_file)
        next(reader)
        time_dict = {}
        for row in reader:
            time_dict['started'] = row[0]
            time_dict['day'] = row[1]
            time_dict['past time'] = row[2]
    return time_dict


if __name__ == '__main__':
    import python_ta.contracts
    python_ta.contracts.check_all_contracts()

    import doctest
    doctest.testmod(verbose=True)

    import python_ta
    python_ta.check_all(config={
        'extra-imports': ['csv', 'typing.Any', 'typing.Optional', 'pandas', 'random', 'datetime'],
        'allowed-io': ['load_emotion_graph', 'read_time_csv'],
        'max-line-length': 100,
        'disable': ['E1136']
    })
