#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import pytest

from ufodiff.subcommands.diff import Diff


# ///////////////////////////////////////////////////////
#
#  Diff class tests
#
# ///////////////////////////////////////////////////////

def test_diff_class_instantiation():
    diff = Diff('.')
    assert diff.is_color_diff is False
    assert diff.gitrepo_path == "."


def test_diff_class_instantation():
    diff = Diff(".", color_diff=True)
    assert diff.is_color_diff is True
    assert diff.gitrepo_path == "."