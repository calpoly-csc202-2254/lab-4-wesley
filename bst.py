import sys
import unittest
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
    def _lookup(node: BinTree, value: Any, comes_before: Callable[[Any, Any], bool]) -> bool:
        if node is None:
            return False
        if (not comes_before(value, node.element)) and (not comes_before(node.element, value)):
            return True
        if comes_before(value, node.element):
            return _lookup(node.left, value, comes_before)
        else:
            return _lookup(node.right, value, comes_before)
    return _lookup(bst.tree, value, bst.comes_before)

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
            # Node with two children: replace with min from right subtree
            min_larger = help_find_min(node.right)
            return Node(min_larger, node.left, help_delete(node.right, min_larger, comes_before))
        elif comes_before(value, node.element):
            return Node(node.element, help_delete(node.left, value, comes_before), node.right)
        else:
            return Node(node.element, node.left, help_delete(node.right, value, comes_before))
    new_tree = help_delete(bst.tree, value, bst.comes_before)
    return BinarySearchTree(bst.comes_before, new_tree)

        





