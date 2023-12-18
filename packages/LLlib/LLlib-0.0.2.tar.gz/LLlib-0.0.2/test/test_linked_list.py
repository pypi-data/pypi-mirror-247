import unittest
import numpy as np
from LLlib import LinkedList


class TestLinkedList(unittest.TestCase):
    def setUp(self):
        self.list = [1, 2, 3, 4, 5]
        self.jagged = [[1, 2, 3], [4, 5, [6, 7]], [8, 9, 10, 11]]
        self.nparray = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        self.dict = {0: 1, 1: 2, 2: 3, 3: 4, 4: 5}

    def test_init(self):
        self.assertEqual(str(LinkedList(self.list)), "1 -> 2 -> 3 -> 4 -> 5 -> None")
        self.assertEqual(str(LinkedList(self.jagged)), "1 -> 2 -> 3 -> 4 -> 5 -> 6 -> 7 -> 8 -> 9 -> 10 -> 11 -> None")
        self.assertEqual(str(LinkedList(self.nparray)), "1 -> 2 -> 3 -> 4 -> 5 -> 6 -> 7 -> 8 -> 9 -> None")
        self.assertEqual(str(LinkedList(self.dict)), "1 -> 2 -> 3 -> 4 -> 5 -> None")


if __name__ == "__main__":
    unittest.main()
