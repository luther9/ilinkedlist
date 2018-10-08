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

import ilinkedlist

basicList = ilinkedlist.new((1, 2, 3, 4))
improperList = ilinkedlist.Pair(11, 93)


def test_new():
  """Make a linked list from an iterable."""
  assert tuple(basicList) == (1, 2, 3, 4)


def test_reverse():
  assert tuple(ilinkedlist.reverse((0, 1, 2))) == (2, 1, 0)


def test_isList():
  """isList returns False for a non-list."""
  assert ilinkedlist.isList(None) is False


class TestNil:

  def test_isList(self):
    """isList(nil) is True."""
    assert ilinkedlist.isList(ilinkedlist.nil) is True

  def test_contains(self):
    """nil does't contain anything."""
    assert None not in ilinkedlist.nil

  def test_iter(self):
    """nil is an empty iterable."""
    for x in ilinkedlist.nil:
      assert False

  def test_len(self):
    """nil is empty"""
    assert len(ilinkedlist.nil) == 0

  def test_reversed(self):
    """reversed(nil) is nil"""
    assert reversed(ilinkedlist.nil) is ilinkedlist.nil

  def test_getitemIndex(self):
    """Indexing raises IndexError."""
    with pytest.raises(IndexError):
      ilinkedlist.nil[0]

  def test_getitemSlice(self):
    """A slice returns nil."""
    assert ilinkedlist.nil[1:3000] is ilinkedlist.nil

  def test_eq(self):
    """nil is equal only to itself."""
    assert ilinkedlist.nil == ilinkedlist.nil
    assert ilinkedlist.nil != basicList

  def test_lt(self):
    assert not (ilinkedlist.nil < ilinkedlist.nil)
    assert ilinkedlist.nil < basicList

  def test_le(self):
    assert ilinkedlist.nil <= ilinkedlist.nil
    assert ilinkedlist.nil <= basicList

  def test_gt(self):
    assert not (ilinkedlist.nil > ilinkedlist.nil)
    assert not (ilinkedlist.nil > basicList)

  def test_ge(self):
    assert ilinkedlist.nil >= ilinkedlist.nil
    assert not (ilinkedlist.nil >= basicList)

  def test_hash(self):
    """nil is hashable."""
    assert hash(ilinkedlist.nil) == 0


class TestPair:

  def test_isList(self):
    """A Pair is a list."""
    assert ilinkedlist.isList(basicList) is True

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
    assert next(it) == 4
    with pytest.raises(StopIteration):
      next(it)

  def test_contains(self):
    """'in' operator works."""
    assert 2 in basicList
    assert 5 not in basicList

  def test_len(self):
    """len() works."""
    assert len(basicList) == 4

  def test_reversed(self):
    """Get a reversed list."""
    assert tuple(reversed(basicList)) == (4, 3, 2, 1)

  def test_getitem(self):
    """Indexing works."""
    assert basicList[1] == 2

  def test_getitemIndexError(self):
    """Out-of-range index raises IndexError."""
    with pytest.raises(IndexError):
      basicList[100]

  def test_getitemNegative(self):
    """Negative index."""
    assert basicList[-3] == 2

  def test_getitemSlice(self):
    """Slicing works."""
    assert basicList[0:2] == ilinkedlist.new((1, 2))

  def test_getitemSliceOutOfRange(self):
    """Out of range slice returns nil."""
    assert basicList[10:2365] is ilinkedlist.nil

  def test_getitemSliceBig(self):
    """An oversize slice returns the same list."""
    assert basicList[-10:20] is basicList

  def test_bool(self):
    """An improper list is truthy."""
    assert improperList

  def test_tail(self):
    """Get the tail of a list."""
    assert basicList.tail(1) == ilinkedlist.new((2, 3, 4))

  def test_eq(self):
    """Equality."""
    assert basicList == ilinkedlist.new((1, 2, 3, 4))
    assert basicList != ilinkedlist.new((2, 1, 0))

  def test_lt(self):
    assert not (basicList < ilinkedlist.nil)
    assert basicList < ilinkedlist.new((0, 1, 3))

  def test_lt(self):
    assert not (basicList <= ilinkedlist.nil)
    assert basicList <= basicList

  def test_gt(self):
    assert basicList > ilinkedlist.nil
    assert basicList > ilinkedlist.new((0, 1, -1))

  def test_ge(self):
    assert basicList >= ilinkedlist.nil
    assert basicList >= basicList

  def test_hash(self):
    """A Pair hashes its car and cdr."""
    assert hash(improperList) == hash((11, 93))

  def test_add(self):
    """Concatenation."""
    assert (
      basicList + ilinkedlist.new((3, 4, 5))
      == ilinkedlist.new((1, 2, 3, 4, 3, 4, 5))
    )

  def test_member(self):
    assert ilinkedlist.new((-1, 0, 1, 2, 3, 4)).member(1) == basicList

  def test_nodes(self):
    it = basicList.nodes()
    assert next(it) == basicList
    assert next(it) == ilinkedlist.new((2, 3, 4))
    assert next(it) == ilinkedlist.new((3, 4))
    assert next(it) == ilinkedlist.new((4,))
    with pytest.raises(StopIteration):
      next(it)

  def test_count(self):
    assert ilinkedlist.new((0, 0, 1, 1, 1)).count(1) == 3

  def test_radd(self):
    assert (4, 5, 6) + basicList == ilinkedlist.new((4, 5, 6, 1, 2, 3, 4))

  def test_mul(self):
    assert (
      basicList * 3
      == ilinkedlist.new((1, 2, 3, 4, 1, 2, 3, 4, 1, 2, 3, 4))
    )

  def test_rmul(self):
    assert 2 * basicList == ilinkedlist.new((1, 2, 3, 4, 1, 2, 3, 4))

  def test_setItem(self):
    assert basicList.setItem(1, 66) == ilinkedlist.new((1, 66, 3, 4))

  def test_setItemSlice(self):
    assert (
      basicList.setItem(slice(1, 3), (10, 11, 12))
      == ilinkedlist.new((1, 10, 11, 12, 4))
    )

  def test_setItemSliceStep(self):
    assert (
      ilinkedlist.new((1, 2, 3, 4, 5, 6)).setItem(slice(1, 5, 2), (10, 20))
      == ilinkedlist.new((1, 10, 3, 20, 5, 6))
    )

  def test_delItem(self):
    assert basicList.delItem(1) == ilinkedlist.new((1, 3, 4))

  def test_delItemSlice(self):
    assert (
      ilinkedlist.new((1, 20, 30, 2, 3, 4)).delItem(slice(1, 3)) == basicList
    )

  def test_delItemSliceStep(self):
    assert (
      ilinkedlist.new((1, 10, 2, 20, 3, 30, 4)).delItem(slice(1, 6, 2))
      == basicList
    )

  def test_insert(self):
    assert basicList.insert(1, 40) == ilinkedlist.new((1, 40, 2, 3, 4))

  def test_splitAt(self):
    assert (
      basicList.splitAt(2) == (ilinkedlist.new((2, 1)), ilinkedlist.new((3, 4)))
    )

  def test_remove(self):
    assert basicList.remove(3) == ilinkedlist.new((1, 2, 4))
    with pytest.raises(ValueError):
      basicList.remove(10)

  def test_sort(self):
    assert ilinkedlist.new((4, 1, 3, 2)).sort() == basicList
