# 2018 Luther Thompson
# This program is public domain. See file COPYING for details.

# TODO:
# Implement features, one at a time, in both nil and Pair.

import pytest

import linkedlist

basicList = linkedlist.new((0, 1, 2))
improperList = linkedlist.Pair(11, 93)


def assertEqual(a, b):
  """Assert that 2 iterables are the same type and have the same elements.

  We should be able to delete this function when we implement equality.
  """
  assert type(a) is type(b)
  for x, y in zip(a, b):
    assert x == y


def test_new():
  """Make a linked list from an iterable."""
  assert tuple(basicList) == (0, 1, 2)


def test_reversed():
  assert tuple(linkedlist.reversed((0, 1, 2))) == (2, 1, 0)


def test_isList():
  """isList returns False for a non-list."""
  assert linkedlist.isList(None) is False


class TestNil:

  def test_isList(self):
    """isList(nil) is True."""
    assert linkedlist.isList(linkedlist.nil) is True

  def test_contains(self):
    """nil does't contain anything."""
    assert not (None in linkedlist.nil)

  def test_iter(self):
    """nil is an empty iterable."""
    for x in linkedlist.nil:
      assert False

  def test_len(self):
    """nil is empty"""
    assert len(linkedlist.nil) == 0

  def test_reversed(self):
    """reversed(nil) is nil"""
    assert reversed(linkedlist.nil) is linkedlist.nil

  def test_getitemIndex(self):
    """Indexing raises IndexError."""
    with pytest.raises(IndexError):
      linkedlist.nil[0]

  def test_getitemSlice(self):
    """A slice returns nil."""
    assert linkedlist.nil[1:3000] is linkedlist.nil


class TestPair:

  def test_isList(self):
    """A Pair is a list."""
    assert linkedlist.isList(basicList) is True

  def test_attributes(self):
    """Has a car and cdr."""
    assert improperList.car == 11
    assert improperList.cdr == 93

  def test_iter(self):
    """We can iterate through a Pair."""
    it = iter(basicList)
    assert next(it) == 0
    assert next(it) == 1
    assert next(it) == 2

  def test_contains(self):
    """'in' operator works."""
    assert 2 in basicList
    assert not (3 in basicList)

  def test_len(self):
    """len() works."""
    assert len(basicList) == 3

  def test_reversed(self):
    """Get a reversed list."""
    assert tuple(reversed(basicList)) == (2, 1, 0)

  def test_getitem(self):
    """Indexing works."""
    assert basicList[1] == 1

  def test_getitemIndexError(self):
    """Out-of-range index raises IndexError."""
    with pytest.raises(IndexError):
      basicList[100]

  def test_getitemNegative(self):
    """Negative index."""
    assert basicList[-3] == 0

  def test_getitemSlice(self):
    """Slicing works."""
    assertEqual(basicList[0:2], linkedlist.new((0, 1)))

  def test_getitemSliceOutOfRange(self):
    """Out of range slice returns nil."""
    assert basicList[10:2365] is linkedlist.nil

  def test_getitemSliceBig(self):
    """An oversize slice returns the same list."""
    assert basicList[-10:20] is basicList

  def test_bool(self):
    """An improper list is truthy."""
    assert improperList

  # TODO: tail with an improper list.
