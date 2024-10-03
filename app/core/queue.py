# -*- coding: utf-8 -*-

class DictQueue:
    """Class for managing data in a queue."""

    def __init__(self):
        """DictQueue constructor object for receiving data from the queue."""
        self.data = dict()

    def add(self, key: str | int, value: any) -> None:
        """Method adds data to the queue."""
        if key not in self.data.keys():
            self.data[key] = value

    def get(self, key: str | int = None) -> dict:
        """Method for receiving data from a queue."""
        if key is None:
            return self.data
        else:
            if key not in self.data.keys():
                raise KeyError(
                    f"'{key}' not found."
                )
            return self.data[key]

    def update(self, key: str | int, value: any) -> None:
        """Method updates data in the queue."""
        if key not in self.data.keys():
            raise KeyError(
                f"'{key}' not found."
            )
        self.data[key] = value

    def delete(self, key: str | int) -> None:
        """Method deleted data in the queue."""
        if key not in self.data:
            raise KeyError(
                f"'{key}' not found."
            )
        self.data.pop(key, None)

    def size(self) -> int:
        """Method returns the queue size."""
        return len(self.data.keys())
