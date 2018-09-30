# Copyright 2018 Luther Thompson

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License (GPL3) as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# You have the following additional permission: You may convey the program in
# object code form under the terms of sections 4 and 5 of GPL3 without being
# bound by section 6 of GPL3.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""An immutable linked list library.

A linked list is defined as either nil or a Pair whose cdr is a linked list.
Linked lists are hashable. Note that it is possible to create an improper list
by passing a non-list as the second argument to Pair.

Linked lists are useful, because they can be built element-by-element in O(n).
Tuples require O(n^2) due to having to copy the tuple with each new element.
Traditional Python lists require O(n*log(n)), because some new elements will
trigger a memory reallocation (and therefore a copy).
"""

import abc
import collections
import itertools
import operator

__all__ = 'nil', 'Pair', 'new', 'reversed', 'isList'


class _List(
    collections.abc.Collection, collections.abc.Hashable,
    collections.abc.Reversible,
):
  """The abstract base class for nil and Pair."""
  # TODO:
  # Implement Sequence methods. We can't inherit from Sequence, because its
  # concrete methods are inefficient for linked lists.
  # count
  # index
  # Implement the equivalents of list methods.
  __slots__ = ()

  @abc.abstractmethod
  def __eq__(self, other):
    pass

  @abc.abstractmethod
  def __lt__(self, other):
    pass

  @abc.abstractmethod
  def __le__(self, other):
    pass

  @abc.abstractmethod
  def __gt__(self, other):
    pass

  @abc.abstractmethod
  def __ge__(self, other):
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
    cdr). Equivalent to self[i:].
    """
    while i > 0 and _isPair(self):
      self = self.cdr
      i -= 1
    return self

  def __getitem__(self, key):
    """Get the key-th element of the list."""
    size = len(self)
    if isinstance(key, int):
      i = key + (size if key < 0 else 0)
      error = IndexError(f'Index out of range: {key}')
      if i < 0:
        raise error
      for x in self:
        if not i:
          return x
        i -= 1
      raise error
    if isinstance(key, slice):
      s = key.indices(size)
      return (
        self.tail(s[0])
        if s[1] >= size and s[2] == 1
        else new(itertools.islice(self, key.start, key.stop, key.step))
      )
    raise TypeError('Index must be int or slice, got {key}')

  def appendReverse(self, head):
    """Append the elements of head, in reverse order, to the beginning of self.

    Return the resulting list. Faster than concatenation.
    """
    for x in head:
      self = Pair(x, self)
    return self

  def __add__(self, other):
    return other.appendReverse(reversed(self))


def isList(x):
  """Return True if x is nil or a Pair, otherwise False."""
  return isinstance(x, _List)


class _NilType(_List):
  """The singleton class for nil."""
  __slots__ = ()

  def __len__(self):
    return 0

  def __eq__(self, other):
    return _isNil(other)

  def __lt__(self, other):
    return (
      False if _isNil(other)
      else True if _isPair(other)
      else NotImplemented
    )

  def __le__(self, other):
    return True if isList(other) else NotImplemented

  def __gt__(self, other):
    return False if isList(other) else NotImplemented

  def __ge__(self, other):
    return (
      True if _isNil(other)
      else False if _isPair(other)
      else NotImplemented
    )

  def __hash__(self):
    return 0


def _isNil(x):
  return x is nil


def _comparePairs(a, b, f):
  return f(a.car, b.car) if a.car != b.car else f(a.cdr, b.cdr)


class Pair(_List):
  """The linked list node."""
  __slots__ = 'car', 'cdr', '_len'

  def __init__(self, car, cdr):
    self.car = car
    self.cdr = cdr
    self._len = (len(cdr) if _isPair(cdr) else 0) + 1

  def __len__(self):
    """Return the length of the list."""
    return self._len

  def __eq__(self, other):
    return (
      False
      if not _isPair(other) or self.car != other.car
      else self.cdr == other.cdr
    )

  def __lt__(self, other):
    return (
      False if not _isPair(other) else _comparePairs(self, other, operator.lt)
    )

  def __le__(self, other):
    return (
      False if not _isPair(other) else _comparePairs(self, other, operator.le)
    )

  def __gt__(self, other):
    return (
      True if not _isPair(other) else _comparePairs(self, other, operator.gt)
    )

  def __ge__(self, other):
    return (
      True if not _isPair(other) else _comparePairs(self, other, operator.ge)
    )

  def __hash__(self):
    return hash((self.car, self.cdr))


def _isPair(x):
  return isinstance(x, Pair)


def reversed(iterable):
  """Reverse iterable and turn it into a linked list.

  This function is faster than new if you don't want to preserve order.
  """
  return nil.appendReverse(iterable)


def new(iterable):
  """Build a linked list from iterable."""
  return reversed(reversed(iterable))


# The empty linked list.
nil = _NilType()
