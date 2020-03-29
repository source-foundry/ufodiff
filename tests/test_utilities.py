#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os.path
import pytest

from ufodiff.utilities import dir_exists, file_exists

# ///////////////////////////////////////////////////////
#
# Utility function tests (utilities.__init__.py)
#
# ///////////////////////////////////////////////////////

valid_directory_test_path = os.path.join("tests", "testfiles")
valid_file_test_path = os.path.join("tests", "testfiles", "testfile.txt")

invalid_directory_test_path = os.path.join("tests", "bogusdir")
invalid_file_test_path = os.path.join("tests", "testfiles", "totallybogus_file.txt")


def test_ufodiff_utilities_dir_exists_true():
    assert dir_exists(valid_directory_test_path) is True


def test_ufodiff_utilities_file_exists_true():
    assert file_exists(valid_file_test_path) is True


def test_ufodiff_utilities_dir_exists_false():
    assert dir_exists(invalid_directory_test_path) is False


def test_ufodiff_utilities_file_exists_false():
    assert file_exists(invalid_file_test_path) is False
