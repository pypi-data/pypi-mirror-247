from LLlib import ListNode
from LLlib.utils import flatten_jagged_list
import numpy as np


class LinkedList(ListNode):
    def __init__(self, data=None, flatten_order="C"):
        """
        This class allows to create complete linked lists (head nodes) from lists, numpy arrays, or dictionaries.
        :param data: The data to create the linked list from.
        :param flatten_order: The order to flatten the data if it is a numpy array (default is "C").
        """
        super().__init__()
        if isinstance(data, list) or isinstance(data, np.ndarray):
            self._from_list_or_array(data, flatten_order)
        elif isinstance(data, dict):
            self._from_dict(data)

    def _from_list_or_array(self, data: list or np.ndarray, flatten_order):
        """
        This function creates a linked list from a list or numpy array, and handles jagged lists or multidimensional
        numpy arrays.
        :param data: The data to create the linked list from (either a list or numpy array).
        :param flatten_order: The order to flatten the data if it is a numpy array.
        """
        if isinstance(data, np.ndarray):
            data = data.flatten(flatten_order)
        else:
            data = list(flatten_jagged_list(data))
        self.val, tail = data[0], self
        for el in data[1:]:
            tail.next = ListNode(el)
            tail = tail.next

    def _from_dict(self, data: dict):
        """
        This function creates a linked list from a dictionary. If the keys are integers, the linked list will be sorted
        by the keys. Otherwise, the linked list will be created in the order of the keys.
        :param data: The data to create the linked list from (a dictionary).
        """
        keys = sorted(data.keys())
        self.val, tail = data[keys[0]], self
        for el in keys[1:]:
            tail.next = ListNode(data[el])
            tail = tail.next
