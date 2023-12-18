![alt text](https://user-images.githubusercontent.com/74055973/284341411-914d7bf0-dbb2-4c4b-8db4-9c9372b51091.png)

# LLlib - A Linked List Library for Python

[LLlib](https://pypi.org/project/LLlib/) is a simple Python library for creating [List Nodes]() / [Linked Lists]()
and performing dense operations (reverse in k-groups, swap in even length groups), design subsidiary structures (LRU/LFU caches, text editors, etc) and build derived classes based projects.

© Copyright 2023, All rights reserved to Hans Haller, MSc Graduate Student in Computer Science at Cranfield University, United Kingdom.

Author GitHub: https://github.com/Hnshlr

Python Package Index (PyPI): https://pypi.org/project/LLlib/

## Context

Linked lists are a fundamental data structure in computer science. They are used to store data in a linear fashion, and are often used to implement other data structures such as stacks, queues, and trees. Linked lists are also used to implement file systems, hash tables, and adjacency lists.

The objective of this package/library (tbd later) is to provide a simple and easy to use interface for creating linked lists and performing simple or complex operations on them. The library is written in Python, and is designed to be used with Python 3.9 or higher.

The core finality of these classes is for anyone to create their own class derived from the `LinkedList` class, and implement their architectures based on the methods provided by the library.

## Installation

The [LLlib](https://pypi.org/project/LLlib/) library is available on [PyPI](https://pypi.org/) (Python Package Index, the official third-party software repository for Python), and can be installed using `pip`:

```shell
$ pip install LLlib
```

## Documentation

The documentation for the [LLlib](https://pypi.org/project/LLlib/) library is currently under development. The documentation will be available on [Read the Docs](https://readthedocs.org/), and will be accessible through the [LLlib](https://pypi.org/project/LLlib/) PyPI page.


## Usage

### Import the Package

````shell
$ python
````
````python
>>> from LLlib import *
````

### List Nodes

The [LLlib](https://pypi.org/project/LLlib/) library provides a `ListNode` class for creating list nodes. The `ListNode` class is a simple class that stores a value and a pointer to the next node in the list. The `ListNode` class can be used to create a linked list by chaining together multiple `ListNode` objects.

````python
>>> from LLlib import ListNode
>>> head = ListNode(1, ListNode(2, ListNode(3, ListNode(4, ListNode(5)))))
>>> str(head)
'1 -> 2 -> 3 -> 4 -> 5 -> None'
>>> ListNode.reverse_list_in_k_group(head, k=2)
>>> str(head)
'2 -> 1 -> 4 -> 3 -> 5 -> None'
````

Ultimately, one may create a class derived from the `ListNode` class, and implement their own methods and attributes.

As an example, to create a Spotify-like music player, one may create a `Song` class derived from the `ListNode` class, and implement their own methods and attributes related to the project at hand.

This class will allow the user to utilize `ListNode` methods and attributes to manipulate the data more efficiently (e.g. reversing the playlist, shuffling the songs, etc).

### Linked Lists

[LLlib](https://pypi.org/project/LLlib/) also provides a `LinkedList` class for creating linked lists. The `LinkedList` class is a simple class that stores a pointer to the head of the list. The `LinkedList` class can be used to create a complete linked lists (of `ListNode` objects) by chaining together multiple `ListNode` objects, using data structures such as lists, tuples, sets, dictionaries, etc.

````python
>>> from LLlib import LinkedList
>>> list = [1, 2, 3, 4, 5]
>>> head = LinkedList(list)
>>> str(head)
'1 -> 2 -> 3 -> 4 -> 5 -> None'
>>> jagged = [[1, 2, 3], [4, 5, [6, 7]], [8, 9, 10, 11]]
>>> head = LinkedList(jagged)
>>> str(head)
'1 -> 2 -> 3 -> 4 -> 5 -> 6 -> 7 -> 8 -> 9 -> 10 -> 11 -> None'
````

For more examples, see the [EXAMPLES.md](doc/EXAMPLES.md) markdown file.

## Acknowledgements

The [LLlib](https://pypi.org/project/LLlib/) library was developed by Hans Haller, MSc Graduate Student in Computer Science at Cranfield University, United Kingdom. Most of the code used is truly unique, and was developed by the author. 

Most of the functions' concepts and ideas were inspired by Leetcode and HackerRank problems. All solutions were developed by the author, and in no way were copied from other sources.

## License

This project is licensed under the [MIT License](LICENSE).

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Library.

‎

Copyright (c) 2023-2024, All rights reserved to Hans Haller.