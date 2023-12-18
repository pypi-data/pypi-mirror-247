from __future__ import annotations
from typing import Optional


class ListNode:
    def __init__(self, val: int = 0, next: Optional[ListNode] = None):
        """
        This class represents a node in a singly-linked list. It has a value and a pointer to the next node.
        :param val: The value of the node.
        :param next: The next node in the list.
        """
        self.val = val
        self.next = next

    def __str__(self):
        """
        This function returns a string representation of the list.
        :return: A string representation of the list.
        """
        return str(self.val) + " -> " + str(self.next)

    def __copy__(self, deep: bool = False) -> ListNode:
        """
        This function returns a copy of the list, either as a hard copy or a soft copy. (Default is a soft copy.)
        A hard copy means that the two lists are different objects in memory.
        A soft copy means that the two lists are the same object in memory.
        :param deep: If True, returns a hard copy of the list. If False, returns a soft copy of the list.
        :return: A copy of the list.
        """
        if deep:
            return ListNode(self.val, self.next.__copy__(deep)) if self.next else ListNode(self.val, None)
        else:
            return self

    def __len__(self):
        """
        This function returns the length of the list (number of nodes).
        :return: The length of the list.
        """
        return 1 + self.next.__len__() if self.next else 1

    def __getitem__(self, index: int) -> ListNode:
        """
        This function returns the node at the given index.
        :param index: The index of the node to return.
        :return: The node at the given index.
        """
        if index == 0:
            return self
        else:
            return self.next.__getitem__(index-1) if self.next else None

    def equals(self, other: Optional[ListNode], as_obj: bool = False) -> bool:
        """
        This function compares two lists, either as objects or as values. (Default is as objects.)
        As objects means that the two lists are the same object in memory.
        As values means that the two lists have the same values in the same order.
        :param other: The other ListNode to compare to.
        :param as_obj: If True, compares the two lists as objects. If False, compares the two lists as values.
        :return: True if the two lists are equal, False otherwise.
        """
        if (self and not other) or (not self and other):
            return False
        if as_obj:
            h1, h2 = self, other
            while h1 and h2:
                if h1 is not h2:
                    return False
                h1, h2 = h1.next, h2.next
            if h1 or h2:
                return False
            return True
        else:
            h1, h2 = self, other
            while h1 and h2:
                if h1.val != h2.val:
                    return False
                h1, h2 = h1.next, h2.next
            if h1 or h2:
                return False
            return True

    def add_node(self, node: Optional[ListNode]):
        """
        This function adds a node to the end of the list.
        :param node: The node to add to the list.
        """
        tail = self
        while tail.next:
            tail = tail.next
        tail.next = node

    @staticmethod   # Ref: Leetcode 2. Add Two Numbers
    def add_two_numbers(l1: Optional[ListNode], l2: Optional[ListNode]) -> ListNode:
        """
        This function adds two numbers represented by two lists, in reverse order.
        Example: 342 + 465 = 807
        l1 = 2 -> 4 -> 3
        l2 = 5 -> 6 -> 4
        l1 + l2 = 7 -> 0 -> 8
        :param l1: The first list.
        :param l2: The second list.
        :return: The sum of the two lists.
        """
        dummy = ListNode()
        tail, carry = dummy, 0
        while l1 or l2 or carry:
            val = carry
            if l1:
                val, l1 = val + l1.val, l1.next
            if l2:
                val, l2 = val + l2.val, l2.next
            tail.next = ListNode(val % 10)
            tail = tail.next
            carry = val // 10
        return dummy.next

    @staticmethod   # Ref: Leetcode 19. Remove Nth Node From End of List
    def remove_nth_from_end(head: Optional[ListNode], n: int) -> ListNode:
        """
        This function removes the nth node from the end of the list.
        :param head: The head of the list.
        :param n: The nth node from the end of the list.
        :return: The head of the list.
        """
        dummy = ListNode(0, head)
        left, right = dummy, head

        while n > 0:
            right = right.next
            n -= 1

        while right:
            left, right = left.next, right.next

        left.next = left.next.next

        return dummy.next

    @staticmethod   # Ref: Leetcode 19. Remove Nth Node From End of List
    def remove_nth_from_start(head: Optional[ListNode], n: int) -> ListNode:
        """
        This function removes the nth node from the start of the list.
        :param head: The head of the list.
        :param n: The nth node from the end of the list.
        :return: The head of the list.
        """
        dummy = ListNode(0, head)

        tail = dummy

        for _ in range(n-1):
            tail = tail.next

        tail.next = tail.next.next

        return dummy.next

    @staticmethod   # Ref: Leetcode 19. Remove Nth Node From End of List
    def remove_nth_node(head: Optional[ListNode], n: int, from_end: bool = True) -> ListNode:
        """
        This function removes the nth node from the start or end of the list.
        :param head: The head of the list.
        :param n: The nth node from the start or end of the list.
        :param from_end: If True, removes the nth node from the end of the list. If False,
        removes the nth node from the start of the list.
        :return: The head of the list.
        """
        if from_end:
            return ListNode.remove_nth_from_end(head, n)
        else:
            return ListNode.remove_nth_from_start(head, n)

    @staticmethod   # Ref: Leetcode 21. Merge Two Sorted Lists
    def merge_two_sorted_lists(l1: Optional[ListNode], l2: Optional[ListNode]) -> ListNode:
        """
        This function merges two sorted lists.
        :param l1: The first sorted list.
        :param l2: The second sorted list.
        :return: The merged sorted list.
        """
        dummy = ListNode()
        tail = dummy

        while l1 and l2:
            if l1.val < l2.val:
                tail.next = l1
                l1 = l1.next
            else:
                tail.next = l2
                l2 = l2.next
            tail = tail.next

        tail.next = l1 or l2

        return dummy.next

    @staticmethod   # Ref: Leetcode 21. Merge Two Sorted Lists
    def merge_two_sorted_lists_recursive(l1: Optional[ListNode], l2: Optional[ListNode]) -> Optional[ListNode]:
        """
        This function merges two sorted lists recursively.
        :param l1: The first sorted list.
        :param l2: The second sorted list.
        :return: The merged sorted list.
        """
        if not l1 or not l2:
            return l1 or l2
        if l1.val < l2.val:
            l1.next = ListNode.merge_two_sorted_lists_recursive(l1.next, l2)
            return l1
        else:
            l2.next = ListNode.merge_two_sorted_lists_recursive(l1, l2.next)
            return l2

    @staticmethod   # Ref: Leetcode 23. Merge k Sorted Lists
    def merge_k_sorted_lists(lists: list[Optional[ListNode]]) -> Optional[ListNode]:
        """
        This function merges k sorted lists.
        :param lists: The list of sorted lists.
        :return: The merged sorted list.
        """
        if not lists:
            return None
        if len(lists) == 1:
            return lists[0]

        lhead = ListNode.merge_k_sorted_lists(lists[:len(lists)//2])
        rhead = ListNode.merge_k_sorted_lists(lists[len(lists)//2:])

        return ListNode.merge_two_sorted_lists_recursive(lhead, rhead)

    @staticmethod   # Ref: Leetcode 206. Reverse Linked List
    def reverse_list(head: Optional[ListNode]) -> ListNode:
        """
        This function reverses a linked list.
        :param head: The head of the list.
        :return: The head of the reversed list.
        """
        prev, tail = None, head
        while tail:
            frwd = tail.next
            tail.next = prev
            prev = tail
            tail = frwd
        return prev

    @staticmethod   # Ref: Leetcode 92. Reverse Linked List II
    def reverse_list_within(head: Optional[ListNode], left: int, right: int) -> Optional[ListNode]:
        """
        This function reverses a linked list within the given range.
        :param head: The head of the list.
        :param left: The left index of the range.
        :param right: The right index of the range.
        :return: The head of the list.
        """
        dummy = ListNode(0, head)
        left_tail = dummy

        for _ in range(left-1):
            left_tail = left_tail.next

        prev, tail = None, left_tail.next

        for _ in range(right-left+1):
            frwd = tail.next
            tail.next = prev
            prev = tail
            tail = frwd

        left_tail.next.next = tail
        left_tail.next = prev

        return dummy.next

    @staticmethod   # Ref: Leetcode 25. Reverse Nodes in k-Group
    def reverse_list_in_k_group(head: Optional[ListNode], k: int) -> Optional[ListNode]:
        """
        This function reverses a linked list in k groups.
        :param head: The head of the list.
        :param k: The number of groups.
        :return: The head of the list.
        """
        # Edge cases:
        if k == 1 or not head or not head.next:
            return head

        dummy = ListNode(0, head)

        # Depth inference:
        dpth = 0
        tail = head
        while tail:
            tail = tail.next
            dpth += 1

        # Reverse within segments:
        lh = dummy
        prev, tail = None, head
        for _ in range(dpth // k):
            prev = None
            for __ in range(k):
                frwd = tail.next
                tail.next = prev
                prev = tail
                tail = frwd
            # lh.next.next = tail
            # lh.next = prev
            # lh = lh.next
            lh.next.next, lh.next, lh = tail, prev, lh.next
        return dummy.next

    @staticmethod   # Ref: Leetcode 24. Swap Nodes in Pairs
    def swap_pairs(head: Optional[ListNode]) -> Optional[ListNode]:
        """
        This function swaps nodes in pairs.
        :param head: The head of the list.
        :return: The head of the list.
        """
        if not head or not head.next:
            return head
        tail = head
        prev = dummy = ListNode(0, head)
        while tail and tail.next:
            prev.next = tail.next
            tail.next = tail.next.next
            prev.next.next = tail

            prev = tail
            tail = tail.next
        return dummy.next
    