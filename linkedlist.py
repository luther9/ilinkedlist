# 2018 Luther Thompson
# This program is public domain. See file COPYING for details.

"""An immutable linked list library.

A linked list is defined as either nil or a Pair whose cdr is a linked list.
Linked lists are hashable. Note that it is possible to create an improper list
by passing a non-list as the second argument to Pair. This will cause some Pair
methods to raise exceptions.

Linked lists are useful, because they can be built element-by-element in O(n).
Tuples require O(n^2) due to having to copy the tuple with each new element.
Traditional Python lists require O(n*log(n)), because some new elements will
trigger a memory reallocation (and therefore a copy).
"""

import abc
import collections
import itertools

__all__ = 'nil', 'Pair', 'new', 'reversed', 'isList'


class _List(collections.abc.Collection, collections.abc.Reversible):
  """The abstract base class for nil and Pair."""
  # TODO:
  # Implement Sequence methods. We can't inherit from Sequence, because its
  # concrete methods are inefficient for linked lists.
  # count
  # index
  # Implement the equivalents of list methods.
  __slots__ = ()

  @abc.abstractmethod
  def isProper(self):
    pass

  def __iter__(self):
    while _isPair(self):
      yield self.car
      self = self.cdr

  def __contains__(self, item):
    for x in self:
      if x == item:
        return True
    return False

  def __reversed__(self):
    return reversed(self)

  def tail(self, i):
    """Return the list starting after the first i nodes.

    If i is greater than the length of the list, return nil (actually the last
    cdr).
    """
    while i > 0 and _isPair(self):
      self = self.cdr
      i -= 1
    return self

  def __getitem__(self, key):
    """Get the key-th element of the list.

    Negative indexes are only supported for proper lists.
    """
    proper = self.isProper()
    if proper:
      size = len(self)
    if isinstance(key, int):
      i = key + (size if proper and key < 0 else 0)
      error = IndexError(f'Index out of range: {key}')
      if i < 0:
        raise error
      for x in self:
        if not i:
          return x
        i -= 1
      raise error
    if isinstance(key, slice):
      if proper:
        s = key.indices(size)
        if s[1] >= size and s[2] == 1:
          return self.tail(s[0])
      return new(itertools.islice(self, key.start, key.stop, key.step))
    raise TypeError('Index must be int or slice, got {key}')


def isList(x):
  """Return True if x is nil or a Pair, otherwise False."""
  return isinstance(x, _List)


class _NilType(_List):
  """The singleton class for nil."""
  __slots__ = ()

  def __len__(self):
    return 0

  def isProper(self):
    return True


class Pair(_List):
  """The linked list node."""
  __slots__ = 'car', 'cdr', '_len'

  def __init__(self, car, cdr):
    self.car = car
    self.cdr = cdr
    self._len = len(cdr) + 1 if isList(cdr) and cdr.isProper() else None

  def __len__(self):
    """Return the length of the list.

    If the list is improper, raise ValueError.
    """
    if self.isProper():
      return self._len
    raise ValueError('Attempt to get length of an improper list')

  def __bool__(self):
    """Don't crash when converting an improper list to bool."""
    return True

  def isProper(self):
    return self._len is not None


def _isPair(x):
  return isinstance(x, Pair)


def reversed(iterable):
  """Reverse iterable and turn it into a linked list.

  This function is faster than new if you don't want to preserve order.
  """
  new = nil
  for x in iterable:
    new = Pair(x, new)
  return new


def new(iterable):
  """Build a linked list from iterable."""
  return reversed(reversed(iterable))


# The empty linked list.
nil = _NilType()
