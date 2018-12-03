from abc import abstractmethod
from functools import total_ordering


@total_ordering
class Shape(object):

    @abstractmethod
    def area(self):
        pass

    def __eq__(self, other):
        if not isinstance(other, Shape):
            raise TypeError('Not Shape')
        return self.area() == other.area()

    def __lt__(self, other):
        if not isinstance(other, Shape):
            raise TypeError('Not Shape')
        return self.area() < other.area()


class Cicle(Shape):

    def __init__(self, r):
        self.r = r

    def area(self):
        return 3.14 * self.r * self.r


class Rec(Shape):

    def __init__(self, h, w):
        self.h = h
        self.w = w

    def area(self):
        return self.w * self.h


def isPrime(k):
    if k % 2 == 0:
        return False
    return True


class PrimeNum(object):
    def __init__(self, start, end):
        self.start = start
        self.end = end

    def __iter__(self):
        for e in range(self.start, self.end):
            if isPrime(e):
                yield e


class Stu(object):

    def __init__(self, name, age):
        self._name = name
        self._age = age

    @property
    def name(self):
        return self._name + '哈哈'

    @name.setter
    def name(self, name):
        self._name = name

    @property
    def age(self):
        return self._age


if __name__ == '__main__':
    c = Cicle(2)
    r = Rec(2, 3)
    print(c < r)
    print(r <= c)
