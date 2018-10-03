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

# TODO:
# Implement features, one at a time, in both nil and Pair.

import pytest

import linkedlist

basicList = linkedlist.new((1, 2, 3))
improperList = linkedlist.Pair(11, 93)


def test_new():
  """Make a linked list from an iterable."""
  assert tuple(basicList) == (1, 2, 3)


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

  def test_eq(self):
    """nil is equal only to itself."""
    assert linkedlist.nil == linkedlist.nil
    assert linkedlist.nil != basicList

  def test_lt(self):
    assert not (linkedlist.nil < linkedlist.nil)
    assert linkedlist.nil < basicList

  def test_le(self):
    assert linkedlist.nil <= linkedlist.nil
    assert linkedlist.nil <= basicList

  def test_gt(self):
    assert not (linkedlist.nil > linkedlist.nil)
    assert not (linkedlist.nil > basicList)

  def test_ge(self):
    assert linkedlist.nil >= linkedlist.nil
    assert not (linkedlist.nil >= basicList)

  def test_hash(self):
    """nil is hashable."""
    assert hash(linkedlist.nil) == 0


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
    assert next(it) == 1
    assert next(it) == 2
    assert next(it) == 3
    with pytest.raises(StopIteration):
      next(it)

  def test_contains(self):
    """'in' operator works."""
    assert 2 in basicList
    assert not (4 in basicList)

  def test_len(self):
    """len() works."""
    assert len(basicList) == 3

  def test_reversed(self):
    """Get a reversed list."""
    assert tuple(reversed(basicList)) == (3, 2, 1)

  def test_getitem(self):
    """Indexing works."""
    assert basicList[1] == 2

  def test_getitemIndexError(self):
    """Out-of-range index raises IndexError."""
    with pytest.raises(IndexError):
      basicList[100]

  def test_getitemNegative(self):
    """Negative index."""
    assert basicList[-3] == 1

  def test_getitemSlice(self):
    """Slicing works."""
    assert basicList[0:2] == linkedlist.new((1, 2))

  def test_getitemSliceOutOfRange(self):
    """Out of range slice returns nil."""
    assert basicList[10:2365] is linkedlist.nil

  def test_getitemSliceBig(self):
    """An oversize slice returns the same list."""
    assert basicList[-10:20] is basicList

  def test_bool(self):
    """An improper list is truthy."""
    assert improperList

  def test_tail(self):
    """Get the tail of a list."""
    assert basicList.tail(1) == linkedlist.new((2, 3))

  def test_eq(self):
    """Equality."""
    assert basicList == linkedlist.new((1, 2, 3))
    assert basicList != linkedlist.new((2, 1, 0))

  def test_lt(self):
    assert not (basicList < linkedlist.nil)
    assert basicList < linkedlist.new((0, 1, 3))

  def test_lt(self):
    assert not (basicList <= linkedlist.nil)
    assert basicList <= basicList

  def test_gt(self):
    assert basicList > linkedlist.nil
    assert basicList > linkedlist.new((0, 1, -1))

  def test_ge(self):
    assert basicList >= linkedlist.nil
    assert basicList >= basicList

  def test_hash(self):
    """A Pair hashes its car and cdr."""
    assert hash(improperList) == hash((11, 93))

  def test_add(self):
    """Concatenation."""
    assert (
      basicList + linkedlist.new((3, 4, 5))
      == linkedlist.new((1, 2, 3, 3, 4, 5))
    )

  def test_member(self):
    assert linkedlist.new((-1, 0, 1, 2, 3)).member(1) == basicList

  def test_nodes(self):
    it = basicList.nodes()
    assert next(it) == basicList
    assert next(it) == linkedlist.new((2, 3))
    assert next(it) == linkedlist.new((3,))
    with pytest.raises(StopIteration):
      next(it)

  #def test_count(self):
