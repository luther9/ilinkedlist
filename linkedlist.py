# 2018 Luther Thompson
# This program is public domain. See file COPYING for details.

"""An immutable linked list library.

A linked list is defined as either nil or a Pair whose cdr is a linked list.
Linked lists are hashable. Note that it is possible to create an improper list
by passing a non-list as the second argument to Pair. This will cause some Pair
methods to raise exceptions.

Linked lists are useful, because they can be built element-by-element, in O(n).
Tuples require O(n^2) due to having to copy the tuple with each new element.
Traditional Python lists require O(n*log(n)), because some new elements will
trigger a memory reallocation (and therefore a copy).
"""

import collections

__all__ = 'nil', 'Pair', 'new', 'reversed', 'isList'


class _List(collections.abc.Collection, collections.abc.Reversible):
  """The abstract base class for nil and Pair."""
  # TODO:
  # Implement Sequence methods. We can't inherit from Sequence, because its
  # concrete methods are inefficient for linked lists.
  __slots__ = ()

  def __iter__(self):
    while self:
      yield self.car
      self = self.cdr

  def __contains__(self, item):
    for x in self:
      if x == item:
        return True
    return False

  def __reversed__(self):
    return reversed(self)


def isList(x):
  """Return True if x is nil or a Pair, otherwise False."""
  return isinstance(x, _List)


class _NilType(_List):
  """The singleton class for nil."""
  __slots__ = ()

  def __len__(self):
    return 0


class Pair(_List):
  """The linked list node.

  If this class is used to form an improper list, some of its methods will raise
  exceptions."""
  __slots__ = 'car', 'cdr', '_len'

  def __init__(self, car, cdr):
    self.car = car
    self.cdr = cdr
    try:
      self._len = len(cdr) + 1 if isList(cdr) else None
    except ValueError:
      self._len = None

  def __len__(self):
    """Return the length of the list.

    If the list is improper, raise ValueError.
    """
    if self._len is None:
      raise ValueError('Attempt to get length of an improper list.')
    return self._len


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
