import inspect
from typing import Optional


def flatten_jagged_list(data):
    for element in data:
        if isinstance(element, list):
            yield from flatten_jagged_list(element)
        else:
            yield element


def write_classes_methods_to_file(classes: list, filename):
    with open(filename, "w") as f:
        for cls in classes:
            f.write(f"Class: {cls.__name__} - Methods:\n")
            for name, method in inspect.getmembers(cls, predicate=inspect.isfunction):
                if method.__qualname__.startswith(cls.__name__):
                    f.write(f"    {name}: {method.__doc__}\n")
            f.write("\n")
