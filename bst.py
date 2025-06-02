import sys
import time
import random
from typing import *
from dataclasses import dataclass
sys.setrecursionlimit(10**6)

def example_fun(x : int) -> bool:
    return x < 142

BinTree: TypeAlias = Union["Node", None]

@dataclass(frozen=True)
class Node:
    element: Any
    left: BinTree
    right: BinTree

@dataclass(frozen=True)
class BinarySearchTree:
    comes_before: Callable[[Any, Any], bool]
    tree: BinTree

def is_empty(bst: BinarySearchTree) -> bool:
    return bst.tree is None

def insert(bst: BinarySearchTree, value: Any) -> BinarySearchTree:
    def helper_insert(node: BinTree, value: Any, comes_before: Callable[[Any, Any], bool]) -> BinTree:
        if node is None:
            return Node(value, None, None)
        if comes_before(value, node.element):
            return Node(node.element, helper_insert(node.left, value, comes_before), node.right)
        else:
            return Node(node.element, node.left, helper_insert(node.right, value, comes_before))
    new_tree = helper_insert(bst.tree, value, bst.comes_before)
    return BinarySearchTree(bst.comes_before, new_tree)

def lookup(bst: BinarySearchTree, value: Any) -> bool:
    def help_lookup(node: BinTree, value: Any, comes_before: Callable[[Any, Any], bool]) -> bool:
        if node is None:
            return False
        if (not comes_before(value, node.element)) and (not comes_before(node.element, value)):
            return True
        if comes_before(value, node.element):
            return help_lookup(node.left, value, comes_before)
        else:
            return help_lookup(node.right, value, comes_before)
    return help_lookup(bst.tree, value, bst.comes_before)

def delete(bst: BinarySearchTree, value: Any) -> BinarySearchTree:
    def help_find_min(node: Node) -> Any:
        current = node
        while current.left is not None:
            current = current.left
        return current.element

    def help_delete(node: BinTree, value: Any, comes_before: Callable[[Any, Any], bool]) -> BinTree:
        if node is None:
            return None
        if (not comes_before(value, node.element)) and (not comes_before(node.element, value)):
            # Node to delete found
            if node.left is None:
                return node.right
            if node.right is None:
                return node.left
            min_larger = help_find_min(node.right)
            return Node(min_larger, node.left, help_delete(node.right, min_larger, comes_before))
        elif comes_before(value, node.element):
            return Node(node.element, help_delete(node.left, value, comes_before), node.right)
        else:
            return Node(node.element, node.left, help_delete(node.right, value, comes_before))
    new_tree = help_delete(bst.tree, value, bst.comes_before)
    return BinarySearchTree(bst.comes_before, new_tree)


# Binary Search Tree Performance Testing

def float_less(x: float, y: float) -> bool:
    return x < y

def build_bst(size: int) -> BinarySearchTree:
    bst = BinarySearchTree(float_less, None)
    for num in range(size):
        value = random.random()
        bst = insert(bst, value)
    return bst

def test_performance():
    sizes = [100000,200000,300000,400000,500000,600000,700000,800000,900000,1000000]

    for size in sizes:
        print(f"\nBuilding BST with {size} elements...")
        start_insert = time.time()
        bst = build_bst(size)
        end_insert = time.time()
        print(f"Insertion time: {end_insert - start_insert:.3f} seconds")

        print(f"Testing search performance with 100 random misses...")
        search_values = [random.random() for _ in range(100)]
        start_search = time.time()
        for val in search_values:
            lookup(bst, val)
        end_search = time.time()
        print(f"Time =  {end_search - start_search:.3f} seconds")

if __name__ == "__main__":
    test_performance()

