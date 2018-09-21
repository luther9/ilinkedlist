# 2018 Luther Thompson
# This program is public domain. See file COPYING for details.

#TODO: Implement features one at a time, in both nil and Pair.

import linkedlist


def test_isList():
  """isList returns False for a non-list."""
  assert linkedlist.isList(None) is False


class TestNil:

  def test_isList(self):
    """isList(nil) is True."""
    assert linkedlist.isList(linkedlist.nil) is True


class TestPair:

  def test_isList(self):
    """A Pair is a list."""
    assert linkedlist.isList(linkedlist.Pair(None, linkedlist.nil)) is True
