# 2018 Luther Thompson
# This program is public domain. See file COPYING for details.

# TODO:
# Implement features one at a time, in both nil and Pair.

import pytest

import linkedlist

basicList = linkedlist.new((0, 1, 2))
improperList = linkedlist.Pair(11, 93)


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

  def test_badLen(self):
    """len() raises an exception for an improper list."""
    with pytest.raises(ValueError):
      len(linkedlist.Pair(None, None))

  def test_reversed(self):
    """Get a reversed list."""
    assert tuple(reversed(basicList)) == (2, 1, 0)
