from typing import Type


class Ship:
    def __init__(self, size, id):
        self._id = id
        self._size = size
        self._letter_start = None
        self._number_start = None
        self._placed = False
        self._sink = False

    def place(self, letter, number, side):
        self._placed = True
        self._letter_start = letter
        self._number_start = number
        self._side = side

    def get_letter(self):
        return self._letter_start

    def get_side(self):
        return self._side

    def get_number(self):
        return self._number_start

    def get_id(self):
        return self._id

    def get_size(self):
        return self._size

    def set_sink(self):
        self._sink = True

    def is_sink(self):
        return self._sink

    def is_placed(self):
        return self._placed
