#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import pytest
import json

from ufodiff.subcommands.delta import Delta, DeltaFilepathDict, get_delta_string

# ///////////////////////////////////////////////////////
#
#  Delta class tests
#
# ///////////////////////////////////////////////////////

# Testing Delta object with mocked values
testing_delta = Delta('.', [], '2')
testing_delta.commit_number = 2


def test_ufodiff_delta_class_instantiation():
    try:
        Delta('.', [], '2')
    except Exception as e:
        pytest.fail(e)


# ///////////////////////////////////////////////////////
#
#  get_delta_string function tests
#
# ///////////////////////////////////////////////////////


class MockDeltaDictObj(object):
    def __init__(self):
        self.delta_dict = {
            'commits': ['ff418e4d', '73fee88'],
            'added': ['Test-Regular.ufo/fontinfo.plist', 'Test-Regular.ufo/metainfo.plist'],
            'deleted': ['Test-Regular.ufo/features.fea'],
            'modified': ['Test-Regular.ufo/glyphs/A.glif', 'Test-Regular.ufo/glyphs/B.glif']
        }


def test_ufodiff_getdeltastring_text():
    mddo = MockDeltaDictObj()
    test_string = get_delta_string(mddo, write_format='text')
    assert 'ff418e4d' in test_string
    assert '73fee88' in test_string
    assert 'Test-Regular.ufo/fontinfo.plist' in test_string
    assert 'Test-Regular.ufo/metainfo.plist' in test_string
    assert 'Test-Regular.ufo/glyphs/A.glif' in test_string
    assert 'Test-Regular.ufo/glyphs/B.glif' in test_string


def test_ufodiff_getdeltastring_json():
    mddo = MockDeltaDictObj()
    test_string = get_delta_string(mddo, write_format='json')
    returned_json_obj = json.loads(test_string)
    assert returned_json_obj['commits'] == ['ff418e4d', '73fee88']
    assert len(returned_json_obj['commits']) == 2
    assert returned_json_obj['added'] == ['Test-Regular.ufo/fontinfo.plist', 'Test-Regular.ufo/metainfo.plist']
    assert len(returned_json_obj['added']) == 2
    assert returned_json_obj['deleted'] == ['Test-Regular.ufo/features.fea']
    assert len(returned_json_obj['deleted']) == 1
    assert returned_json_obj['modified'] == ['Test-Regular.ufo/glyphs/A.glif', 'Test-Regular.ufo/glyphs/B.glif']
    assert len(returned_json_obj['modified']) == 2


def test_ufodiff_getdeltastring_md():
    mddo = MockDeltaDictObj()
    test_string = get_delta_string(mddo, write_format='markdown')
    assert 'ff418e4d' in test_string
    assert '73fee88' in test_string
    assert 'Test-Regular.ufo/fontinfo.plist' in test_string
    assert 'Test-Regular.ufo/metainfo.plist' in test_string
    assert 'Test-Regular.ufo/glyphs/A.glif' in test_string
    assert 'Test-Regular.ufo/glyphs/B.glif' in test_string
