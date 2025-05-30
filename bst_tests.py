import sys
import unittest
from typing import *
from dataclasses import dataclass
sys.setrecursionlimit(10**6)

from bst import *

def numeric_comes_before(a, b):
    return a < b

def alphabetic_comes_before(a, b):
    return a < b

def euclidean_comes_before(a, b):
    def dist_from_zero(p):
        return (p[0] ** 2 + p[1] ** 2) ** 0.5
    return dist_from_zero(a) < dist_from_zero(b)

class BSTTests(unittest.TestCase):
    def test_example_fun(self):
        self.assertEqual(example_fun(34), True)
        self.assertEqual(example_fun(1423), False)

    def test_numeric_ordering(self):
        bst = BinarySearchTree(numeric_comes_before, None)
        bst = insert(bst, 5)
        bst = insert(bst, 3)
        bst = insert(bst, 7)
        self.assertEqual(lookup(bst, 5), True)
        self.assertEqual(lookup(bst, 10), False)
        bst2 = delete(bst, 3)
        self.assertEqual(lookup(bst2, 3), False)

    def test_alphabetic_ordering(self):
        bst = BinarySearchTree(alphabetic_comes_before, None)
        bst = insert(bst, "cat")
        bst = insert(bst, "apple")
        bst = insert(bst, "dog")
        self.assertEqual(lookup(bst, "cat"), True)
        self.assertEqual(lookup(bst, "banana"), False)
        bst2 = delete(bst, "cat")
        self.assertEqual(lookup(bst2, "cat"), False)

    def test_euclidean_distance_ordering(self):
        bst = BinarySearchTree(euclidean_comes_before, None)
        bst = insert(bst, (3, 4))   # distance 5
        bst = insert(bst, (1, 1))   # distance sqrt(2)
        bst = insert(bst, (0, 0))   # distance 0
        self.assertEqual(lookup(bst, (3, 4)), True)
        self.assertEqual(lookup(bst, (2, 2)), False)
        bst2 = delete(bst, (3, 4))
        self.assertEqual(lookup(bst2, (3, 4)), False)

if __name__ == '__main__':
    unittest.main()