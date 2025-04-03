# searchExample.py - Search Examples
# AIFCA Python code Version 0.9.15 Documentation at https://aipython.org
# Download the zip file and read aipython.pdf for documentation

# Artificial Intelligence: Foundations of Computational Agents https://artint.info
# Copyright 2017-2024 David L. Poole and Alan K. Mackworth
# This work is licensed under a Creative Commons
# Attribution-NonCommercial-ShareAlike 4.0 International License.
# See: https://creativecommons.org/licenses/by-nc-sa/4.0/deed.en

from library.searchProblem import Arc, Search_problem_from_explicit_graph, Search_problem

problem1 = Search_problem_from_explicit_graph('Problem 1',
    {'A','B','C','D','G'},
    [Arc('A','B',3), Arc('A','C',1), Arc('B','D',1), Arc('B','G',3),
         Arc('C','B',1), Arc('C','D',3), Arc('D','G',1)],
    start = 'A',
    goals = {'G'},
    positions={'A': (0, 1), 'B': (0.5, 0.5), 'C': (0,0.5),
                   'D': (0.5,0), 'G': (1,0)})

problem2 = Search_problem_from_explicit_graph('Problem 2',
    {'A','B','C','D','E','G','H','J'},
    [Arc('A','B',1), Arc('B','C',3), Arc('B','D',1), Arc('D','E',3),
        Arc('D','G',1), Arc('A','H',3), Arc('H','J',1)],
    start = 'A',
    goals = {'G'},
    positions={'A':(0, 1), 'B':(0, 3/4), 'C':(0,0), 'D':(1/4,3/4),
                   'E':(1/4,0), 'G':(2/4,3/4), 'H':(3/4,1), 'J':(3/4,3/4)})

problem3 = Search_problem_from_explicit_graph('Problem 3',
    {'a','b','c','d','e','g','h','j'},
    [],
    start = 'g',
    goals = {'k','g'})

simp_delivery_graph = Search_problem_from_explicit_graph("Acyclic Delivery Graph",
    {'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'J'},
    [    Arc('A', 'B', 2),
         Arc('A', 'C', 3),
         Arc('A', 'D', 4),
         Arc('B', 'E', 2),
         Arc('B', 'F', 3),
         Arc('C', 'J', 7),
         Arc('D', 'H', 4),
         Arc('F', 'D', 2),
         Arc('H', 'G', 3),
         Arc('J', 'G', 4)],
   start = 'A',
   goals = {'G'},
   hmap = {
        'A': 7,
        'B': 5,
        'C': 9,
        'D': 6,
        'E': 3,
        'F': 5,
        'G': 0,
        'H': 3,
        'J': 4,
    },
    positions = {
        'A': (0.4,0.1),
        'B': (0.4,0.4),
        'C': (0.1,0.1),
        'D': (0.7,0.1),
        'E': (0.6,0.7),
        'F': (0.7,0.4),
        'G': (0.7,0.9),
        'H': (0.9,0.6),
        'J': (0.3,0.9)
        }
    )
cyclic_simp_delivery_graph = Search_problem_from_explicit_graph("Cyclic Delivery Graph",
    {'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'J'},
    [    Arc('A', 'B', 2),
         Arc('A', 'C', 3),
         Arc('A', 'D', 4),
         Arc('B', 'E', 2),
         Arc('B', 'F', 3),
         Arc('C', 'A', 3),
         Arc('C', 'J', 6),
         Arc('D', 'A', 4),
         Arc('D', 'H', 4),
         Arc('F', 'B', 3),
         Arc('F', 'D', 2),
         Arc('G', 'H', 3),
         Arc('G', 'J', 4),
         Arc('H', 'D', 4),
         Arc('H', 'G', 3),
         Arc('J', 'C', 6),
         Arc('J', 'G', 4)],
   start = 'A',
   goals = {'G'},
   hmap = {
        'A': 7,
        'B': 5,
        'C': 9,
        'D': 6,
        'E': 3,
        'F': 5,
        'G': 0,
        'H': 3,
        'J': 4,
    },
    positions = {
        'A': (0.4,0.1),
        'B': (0.4,0.4),
        'C': (0.1,0.1),
        'D': (0.7,0.1),
        'E': (0.6,0.7),
        'F': (0.7,0.4),
        'G': (0.7,0.9),
        'H': (0.9,0.6),
        'J': (0.3,0.9)
        })

tree_graph = Search_problem_from_explicit_graph("Tree Graph",
    {'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O',
         'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'AA', 'BB', 'CC',
         'DD', 'EE', 'FF', 'GG', 'HH', 'II', 'JJ', 'KK'},
    [    Arc('A', 'B', 1),
         Arc('A', 'C', 1),
         Arc('B', 'D', 1),
         Arc('B', 'E', 1),
         Arc('C', 'F', 1),
         Arc('C', 'G', 1),
         Arc('D', 'H', 1),
         Arc('D', 'I', 1),
         Arc('E', 'J', 1),
         Arc('E', 'K', 1),
         Arc('F', 'L', 1),
         Arc('G', 'M', 1),
         Arc('G', 'N', 1),
         Arc('H', 'O', 1),
         Arc('H', 'P', 1),
         Arc('J', 'Q', 1),
         Arc('J', 'R', 1),
         Arc('L', 'S', 1),
         Arc('L', 'T', 1),
         Arc('N', 'U', 1),
         Arc('N', 'V', 1),
         Arc('O', 'W', 1),
         Arc('P', 'X', 1),
         Arc('P', 'Y', 1),
         Arc('R', 'Z', 1),
         Arc('R', 'AA', 1),
         Arc('T', 'BB', 1),
         Arc('T', 'CC', 1),
         Arc('V', 'DD', 1),
         Arc('V', 'EE', 1),
         Arc('W', 'FF', 1),
         Arc('X', 'GG', 1),
         Arc('Y', 'HH', 1),
         Arc('AA', 'II', 1),
         Arc('CC', 'JJ', 1),
         Arc('CC', 'KK', 1)
    ],
   start = 'A',
   goals = {'K', 'M', 'T', 'X', 'Z', 'HH'},
    positions = {
        'A': (0.5,0.95),
        'B': (0.3,0.8),
        'C': (0.7,0.8),
        'D': (0.2,0.65),
        'E': (0.4,0.65),
        'F': (0.6,0.65),
        'G': (0.8,0.65),
        'H': (0.2,0.5),
        'I': (0.3,0.5),
        'J': (0.4,0.5),
        'K': (0.5,0.5),
        'L': (0.6,0.5),
        'M': (0.7,0.5),
        'N': (0.8,0.5),
        'O': (0.1,0.35),
        'P': (0.2,0.35),
        'Q': (0.3,0.35),
        'R': (0.4,0.35),
        'S': (0.5,0.35),
        'T': (0.6,0.35),
        'U': (0.7,0.35),
        'V': (0.8,0.35),
        'W': (0.1,0.2),
        'X': (0.2,0.2),
        'Y': (0.3,0.2),
        'Z': (0.4,0.2),
        'AA': (0.5,0.2),
        'BB': (0.6,0.2),
        'CC': (0.7,0.2),
        'DD': (0.8,0.2),
        'EE': (0.9,0.2),
        'FF': (0.1,0.05),
        'GG': (0.2,0.05),
        'HH': (0.3,0.05),
        'II': (0.5,0.05),
        'JJ': (0.7,0.05),
        'KK': (0.8,0.05)      
        }
    )

# tree_graph.show(show_costs = False)
