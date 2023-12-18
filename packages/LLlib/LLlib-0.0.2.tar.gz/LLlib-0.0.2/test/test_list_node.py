import unittest
from LLlib import ListNode


class TestListNode(unittest.TestCase):
    def setUp(self):
        self.head = ListNode(1, ListNode(2, ListNode(3, ListNode(4, ListNode(5)))))     # 1 -> 2 -> 3 -> 4 -> 5 -> None
        self.unique = ListNode(1)                                                       # 1 -> None
        self.zero = ListNode()                                                          # 0 -> None
        self.two = ListNode(1, ListNode(2))                                             # 1 -> 2 -> None
        self.sorted_one = ListNode(1, ListNode(2, ListNode(4)))                         # 1 -> 2 -> 4 -> None
        self.sorted_two = ListNode(1, ListNode(3, ListNode(4)))                         # 1 -> 3 -> 4 -> None

    def test_init(self):
        self.assertEqual(self.head.val, 1)
        self.assertIsNone(self.zero.next)

    def test_str(self):
        self.assertEqual(str(self.head), "1 -> 2 -> 3 -> 4 -> 5 -> None")
        self.assertEqual(str(self.unique), "1 -> None")
        self.assertEqual(str(self.zero), "0 -> None")

    def test_copy(self):
        self.assertTrue(self.head.__copy__(deep=False).equals(self.head, as_obj=True))
        self.assertTrue(self.head.__copy__(deep=True).equals(self.head, as_obj=False))
        tmp = self.head.__copy__(deep=True)
        tmp_soft_copy = tmp.__copy__(deep=False)
        tmp_soft_copy.val = 33
        self.assertTrue(tmp_soft_copy.equals(tmp, as_obj=True))
        self.assertTrue(tmp_soft_copy.equals(tmp, as_obj=False))
        self.assertFalse(tmp_soft_copy.equals(self.head, as_obj=True))
        self.assertFalse(tmp_soft_copy.equals(self.head, as_obj=False))

    def test_len(self):
        self.assertEqual(self.head.__len__(), 5)
        self.assertEqual(self.unique.__len__(), 1)
        self.assertEqual(len(self.zero), 1)
        self.assertEqual(len(self.two), 2)

    def test_getitem(self):
        self.assertEqual(self.head.__getitem__(0).val, 1)
        self.assertEqual(self.head.__getitem__(2).val, 3)
        self.assertTrue(self.head.__getitem__(5) is None)
        self.assertTrue(self.head.__getitem__(-1) is None)

    def test_equals(self):
        self.assertTrue(self.head.equals(self.head.__copy__(deep=False), as_obj=True))
        self.assertTrue(self.head.equals(self.head.__copy__(deep=True), as_obj=False))

        self.assertFalse(self.head.equals(ListNode(1), as_obj=True))
        self.assertFalse(self.head.equals(ListNode(1), as_obj=False))

        self.assertFalse(self.head.equals(None, as_obj=True))
        self.assertFalse(self.head.equals(None, as_obj=False))
        self.assertFalse(self.head.equals(self.unique, as_obj=True))
        self.assertFalse(self.head.equals(self.unique, as_obj=False))

    def test_add_two_numbers(self):
        self.assertTrue(ListNode.add_two_numbers(
            ListNode(2, ListNode(4, ListNode(3))),
            ListNode(5, ListNode(6, ListNode(4))))
                        .equals(ListNode(7, ListNode(0, ListNode(8)))))

        self.assertTrue(ListNode.add_two_numbers(
            ListNode(0), ListNode(0))
                        .equals(ListNode(0)))

        self.assertTrue(ListNode.add_two_numbers(
            ListNode(9, ListNode(9, ListNode(9, ListNode(9, ListNode(9, ListNode(9, ListNode(9))))))),
            ListNode(9, ListNode(9, ListNode(9, ListNode(9)))))
                        .equals(ListNode(8, ListNode(9, ListNode(9, ListNode(9, ListNode(0, ListNode(0, ListNode(0, ListNode(1))))))))))

    def test_remove_nth_from_end(self):
        self.assertTrue(ListNode.remove_nth_from_end(self.head.__copy__(deep=True), 2).equals(ListNode(1, ListNode(2, ListNode(3, ListNode(5))))))
        self.assertTrue(ListNode.remove_nth_from_end(self.unique.__copy__(True), 1) is None)
        self.assertTrue(ListNode.remove_nth_from_end(self.two.__copy__(True), 1).equals(ListNode(1)))
        self.assertTrue(ListNode.remove_nth_from_end(self.two.__copy__(True), 2).equals(ListNode(2)))

    def test_remove_nth_from_start(self):
        self.assertTrue(ListNode.remove_nth_from_start(self.head.__copy__(deep=True), 2).equals(ListNode(1, ListNode(3, ListNode(4, ListNode(5))))))
        self.assertTrue(ListNode.remove_nth_from_start(self.unique.__copy__(deep=True), 1) is None)
        self.assertTrue(ListNode.remove_nth_from_start(self.two.__copy__(deep=True), 1).equals(ListNode(2)))
        self.assertTrue(ListNode.remove_nth_from_start(self.two.__copy__(deep=True), 2).equals(ListNode(1)))

    def test_merge_two_sorted_lists(self):
        self.assertTrue(ListNode.merge_two_sorted_lists(self.sorted_one, self.sorted_two)
                        .equals(ListNode(1, ListNode(1, ListNode(2, ListNode(3, ListNode(4, ListNode(4))))))))

        self.assertTrue(ListNode.merge_two_sorted_lists(self.zero.__copy__(deep=True), self.zero.__copy__(deep=True))
                        .equals(ListNode(0, ListNode(0, None))))

    def test_merge_two_sorted_lists_recursive(self):
        self.assertTrue(ListNode.merge_two_sorted_lists_recursive(self.sorted_one, self.sorted_two)
                        .equals(ListNode(1, ListNode(1, ListNode(2, ListNode(3, ListNode(4, ListNode(4))))))))

        self.assertTrue(ListNode.merge_two_sorted_lists_recursive(self.zero.__copy__(deep=True), self.zero.__copy__(deep=True))
                        .equals(ListNode(0, ListNode(0, None))))

    def test_merge_k_sorted_lists(self):
        lists = [
            ListNode(1, ListNode(4, ListNode(5))),
            ListNode(1, ListNode(3, ListNode(4))),
            ListNode(2, ListNode(6))
        ]
        self.assertTrue(ListNode.merge_k_sorted_lists(lists)
                        .equals(ListNode(1, ListNode(1, ListNode(2, ListNode(3, ListNode(4, ListNode(4, ListNode(5, ListNode(6))))))))))
        self.assertTrue(ListNode.merge_k_sorted_lists([ListNode()]).equals(ListNode()))
        self.assertTrue(ListNode.merge_k_sorted_lists([]) is None)

    def test_reverse_list(self):
        self.assertTrue(ListNode.reverse_list(self.head.__copy__(deep=True))
                        .equals(ListNode(5, ListNode(4, ListNode(3, ListNode(2, ListNode(1, None)))))))

        self.assertTrue(ListNode.reverse_list(self.unique.__copy__(deep=True)).equals(ListNode(1, None)))
        self.assertTrue(ListNode.reverse_list(self.two.__copy__(deep=True)).equals(ListNode(2, ListNode(1, None))))
        self.assertTrue(ListNode.reverse_list(self.zero.__copy__(deep=True)).equals(ListNode()))

    def test_reverse_list_within(self):
        self.assertTrue(ListNode.reverse_list_within(self.head.__copy__(deep=True), left=2, right=4)
                        .equals(ListNode(1, ListNode(4, ListNode(3, ListNode(2, ListNode(5)))))))
        self.assertTrue(ListNode.reverse_list_within(self.head.__copy__(deep=True), left=1, right=5)
                        .equals(ListNode(5, ListNode(4, ListNode(3, ListNode(2, ListNode(1)))))))
        self.assertTrue(ListNode.reverse_list_within(self.unique.__copy__(deep=True), left=1, right=1)
                        .equals(ListNode(1, None)))

    def test_reverse_list_in_k_group(self):
        self.assertTrue(ListNode.reverse_list_in_k_group(self.head.__copy__(deep=True), k=2)
                        .equals(ListNode(2, ListNode(1, ListNode(4, ListNode(3, ListNode(5)))))))
        self.assertTrue(ListNode.reverse_list_in_k_group(self.head.__copy__(deep=True), k=3)
                        .equals(ListNode(3, ListNode(2, ListNode(1, ListNode(4, ListNode(5)))))))
        self.assertTrue(ListNode.reverse_list_in_k_group(self.head.__copy__(deep=True), k=1)
                        .equals(ListNode(1, ListNode(2, ListNode(3, ListNode(4, ListNode(5)))))))
        self.assertTrue(ListNode.reverse_list_in_k_group(self.unique.__copy__(deep=True), k=1)
                        .equals(ListNode(1, None)))
        self.assertTrue(ListNode.reverse_list_in_k_group(self.zero.__copy__(deep=True), k=1)
                        .equals(ListNode(0, None)))
        self.assertTrue(ListNode.reverse_list_in_k_group(self.two.__copy__(deep=True), k=2)
                        .equals(ListNode(2, ListNode(1, None))))

    def test_swap_pairs(self):
        self.assertTrue(ListNode.swap_pairs(self.head.__copy__(deep=True))
                        .equals(ListNode(2, ListNode(1, ListNode(4, ListNode(3, ListNode(5)))))))
        self.assertTrue(ListNode.swap_pairs(self.unique.__copy__(deep=True)).equals(ListNode(1, None)))
        self.assertTrue(ListNode.swap_pairs(self.zero.__copy__(deep=True)).equals(ListNode(0, None)))
        self.assertTrue(ListNode.swap_pairs(self.two.__copy__(deep=True)).equals(ListNode(2, ListNode(1, None))))


if __name__ == "__main__":
    unittest.main()
