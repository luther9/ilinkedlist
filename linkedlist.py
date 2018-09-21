# 2018 Luther Thompson
# This program is public domain. See file COPYING for details.

"""An immutable linked list library.

A linked list is defined as either nil or a Pair whose cdr is a linked list.
Linked lists are hashable. Note that it is possible to create an improper list
by passing a non-list as the second argument to Pair. This will cause some
methods to raise exceptions.

Linked lists are useful, because they can be built element-by-element, in O(n).
Tuples require O(n^2) due to having to copy the tuple with each new element.
Traditional Python lists require O(n*log(n)), because some new elements will
trigger a memory reallocation (and therefore a copy).
"""

# TODO: Make a _List abstract class, implemented by both nil and Pair.


class _List:
  pass


def isList(x):
  """Return True if x is nil or a Pair, otherwise False."""
  return isinstance(x, _List)
