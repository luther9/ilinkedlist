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

__all__ = 'nil', 'Pair', 'isList'


class _List(collections.abc.Collection, collections.abc.Reversible):
  """The abstract base class for nil and Pair."""
  # TODO:
  # Implement Sequence methods. We can't inherit from Sequence, because it's
  # inefficient for linked lists.
  __slots__ = ()

  def __contains__(self, item):
    for x in self:
      if x == item:
        return True
    return False

  def __reversed__(self):
    new = nil
    for x in self:
      new = Pair(x, new)
    return new


def isList(x):
  """Return True if x is nil or a Pair, otherwise False."""
  return isinstance(x, _List)


class _NilType(_List):
  """The singleton class for nil."""
  __slots__ = ()

  def __iter__(self):
    return self

  def __next__(self):
    raise StopIteration

  def __len__(self):
    return 0


class Pair(_List):
  """The linked list node.

  If this class is used to form an improper list, some of its methods will throw
  exceptions."""
  __slots__ = 'car', 'cdr', '_len'

  def __init__(self, car, cdr):
    self.car = car
    self.cdr = cdr
    try:
      self._len = len(cdr) + 1
    except (ValueError, TypeError):
      self._len = None

  def __iter__(self):
    while self:
      yield self.car
      self = self.cdr

  def __len__(self):
    if self._len is None:
      raise ValueError('Attempt to get length of an improper list.')
    return self._len


# The empty linked list.
nil = _NilType()
