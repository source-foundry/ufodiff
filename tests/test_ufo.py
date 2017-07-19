#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import pytest

from ufodiff.utilities.ufo import Ufo

# ///////////////////////////////////////////////////////
#
#  Ufo class tests
#
# ///////////////////////////////////////////////////////

ufo_acceptable_files = {
    'metainfo.plist',
    'fontinfo.plist',
    'groups.plist',
    'kerning.plist',
    'features.fea',
    'lib.plist',
    'contents.plist',
    'layercontents.plist',
    'layerinfo.plist'
}

unacceptable_file = "testing.py"


# confirm valid file list in class property
def test_ufodiff_ufo_acceptable_files():
    ufo = Ufo()
    for the_file in ufo.acceptable_files:
        assert the_file in ufo_acceptable_files


# confirm unacceptable file returns false from class property
def test_ufodiff_ufo_unacceptable_file():
    ufo = Ufo()
    assert (unacceptable_file in ufo.acceptable_files) is False


# test ufo.validate_file() with true conditions
def test_ufodiff_ufo_validate_file_true():
    ufo = Ufo()
    for the_file in ufo_acceptable_files:
        assert ufo.validate_file(the_file) is True


# test ufo.validate_file() with false condition
def test_ufodiff_ufo_validate_file_false():
    ufo = Ufo()
    assert ufo.validate_file("testing.py") is False


# test nonglyph file check with true conditions
def test_ufodiff_ufo_nonglyph_true():
    ufo = Ufo()
    for nonglyph_file in ufo_acceptable_files:     # this file set only includes nonglyph files (i.e. not *.glif)
        assert ufo.is_nonglyph_file(nonglyph_file) is True


# test nonglyph file check with false condition
def test_ufodiff_ufo_nonglyph_false():
    ufo = Ufo()
    assert ufo.is_nonglyph_file("A.glif") is False


# test glyph file check with true condition
def test_ufodiff_ufo_glyph_true():
    ufo = Ufo()
    assert ufo.is_glyph_file("A.glif") is True
    assert ufo.is_glyph_file("A__.glif") is True
    assert ufo.is_glyph_file("0012.glif") is True


# test glyph file check with false conditions
def test_ufodiff_ufo_glyph_false():
    ufo = Ufo()
    for nonglyph_file in ufo_acceptable_files:
        assert ufo.is_glyph_file(nonglyph_file) is False


# test detection of metainfo.plist file with true condition
# (location of UFO version definition in the source files)
def test_ufodiff_ufo_version_true():
    ufo = Ufo()
    assert ufo.is_ufo_version_file("metainfo.plist") is True


# test detection of metainfo.plist file with false condition
def test_ufodiff_ufo_version_false():
    ufo = Ufo()
    assert ufo.is_ufo_version_file("fontinfo.plist") is False


# test UFO file filters for diff and diffnc commands
def test_ufodiff_ufo_diff_filters():
    ufo = Ufo()
    filter_test_list = ufo.get_valid_file_filterlist_for_diff()
    # test for each of the nonglyph files
    for acceptable_file in ufo.acceptable_files:
        filter_file = "*" + acceptable_file
        assert filter_file in filter_test_list
    # test for inclusion of glyph files
    assert '*.glif' in filter_test_list


# UFO v3 image directory/file tests

def test_ufodiff_ufo_images_dir_png_file_true():
    ufo = Ufo()
    test_path_1 = os.path.join('source', 'Test-Regular.ufo', 'images', 'cap_a.png')
    assert ufo._is_images_directory_file(test_path_1) is True


def test_ufodiff_ufo_images_dir_png_file_false():
    ufo = Ufo()
    test_path_1 = os.path.join('source', 'anotherdir', 'images', 'cap_a.png')        # not a UFO source directory
    test_path_2 = os.path.join('source', 'Test-Regular.ufo', 'image', 'cap_a.png')   # incorrect images dir path
    test_path_3 = os.path.join('source', 'Test-Regular.ufo', 'images', 'cap_a.jpg')  # jpg file, not png
    assert ufo._is_images_directory_file(test_path_1) is False
    assert ufo._is_images_directory_file(test_path_2) is False
    assert ufo._is_images_directory_file(test_path_3) is False


# UFO v3 data directory/file tests
def test_ufodiff_ufo_data_dir_file_true():
    ufo = Ufo()
    test_path_1 = os.path.join('source', 'Test-Regular.ufo', 'data', 'org.sourcefoundry.coolstuff')
    assert ufo._is_data_directory_file(test_path_1) is True


def test_ufodiff_ufo_data_dir_file_false():
    ufo = Ufo()
    test_path_1 = os.path.join('source', 'Test-Regular.ufo', 'datum', 'org.sourcefoundry.coolstuff')  # bad dir path
    test_path_2 = os.path.join('source', 'Test-Regular', 'data', 'org.sourcefoundry.coolstuff')  # not ufo dir
    assert ufo._is_data_directory_file(test_path_1) is False
    assert ufo._is_data_directory_file(test_path_2) is False
