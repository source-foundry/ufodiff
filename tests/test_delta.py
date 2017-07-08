#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import pytest
import json

from git import Repo

from ufodiff.subcommands.delta import Delta, DeltaFilepathDict, get_delta_string

# ///////////////////////////////////////////////////////
#
#  Delta class tests
#
# ///////////////////////////////////////////////////////


# Mock Diffable class for unit tests - need to assign values in tests
class MockDiffableObj(object):
    def __init__(self):
        self.a_rawpath = ""
        self.new_file = True
        self.deleted_file = True
        self.change_type = "M"


def test_ufodiff_delta_class_instantiation():
    try:
        Delta('.', [], '2')
    except Exception as e:
        pytest.fail(e)


def test_ufodiff_delta_class_sha1_list_build_method():
    delta_test = Delta('.', [], '2')
    repo = Repo('.')
    git = repo.git

    # have to empty the list before testing this as unit test because it is filled on instatiation of class
    delta_test.commit_sha1_list = []
    assert len(delta_test.commit_sha1_list) == 0
    # confirm the commit history request number
    assert delta_test.commit_number == '2'
    # execute test method to fill SHA1 list
    delta_test._add_commit_sha1_to_lists(git)
    # appropriate number of commit entries after test
    assert len(delta_test.commit_sha1_list) == 2


def test_ufodiff_delta_class_validate_ufo_method():
    # Mock Diffable Obj 1
    mdo1 = MockDiffableObj()
    mdo1.a_rawpath = "fontinfo.plist"
    mdo1.new_file = True
    mdo1.deleted_file = False
    mdo1.change_type = "Z"

    mdo2 = MockDiffableObj()
    mdo2.a_rawpath = "metainfo.plist"
    mdo2.new_file = False
    mdo2.deleted_file = False
    mdo2.change_type = "M"

    mdo3 = MockDiffableObj()
    mdo3.a_rawpath = "features.fea"
    mdo3.new_file = False
    mdo3.deleted_file = True
    mdo3.change_type = "Z"

    mdo4 = MockDiffableObj()
    mdo4.a_rawpath = "A.glif"
    mdo4.new_file = False
    mdo4.deleted_file = False
    mdo4.change_type = "M"

    # should not load into lists
    mdo5 = MockDiffableObj()
    mdo5.a_rawpath = "bogus.bogus"
    mdo5.new_file = True
    mdo5.deleted_file = True
    mdo5.change_type = "M"

    delta_test = Delta('.', [], '2')

    #empty the existing lists built on instantiation
    delta_test.added_ufo_diffobj_list = []
    delta_test.modified_ufo_diffobj_list = []
    delta_test.deleted_ufo_diffobj_list = []

    assert len(delta_test.added_ufo_diffobj_list) == 0
    assert len(delta_test.modified_ufo_diffobj_list) == 0
    assert len(delta_test.deleted_ufo_diffobj_list) == 0

    # execute method
    for diff_file in [mdo1, mdo2, mdo3, mdo4, mdo5]:
        delta_test._validate_ufo_and_load_lists(diff_file)

    assert 'fontinfo.plist' == delta_test.added_ufo_diffobj_list[0].a_rawpath
    assert len(delta_test.added_ufo_diffobj_list) == 1
    assert 'metainfo.plist' == delta_test.modified_ufo_diffobj_list[0].a_rawpath
    assert 'A.glif' == delta_test.modified_ufo_diffobj_list[1].a_rawpath
    assert len(delta_test.modified_ufo_diffobj_list) == 2
    assert 'features.fea' == delta_test.deleted_ufo_diffobj_list[0].a_rawpath
    assert len(delta_test.deleted_ufo_diffobj_list) == 1
    assert ('bogus.bogus' == delta_test.added_ufo_diffobj_list[0].a_rawpath) is False
    assert ('bogus.bogus' == delta_test.deleted_ufo_diffobj_list[0].a_rawpath) is False
    assert ('bogus.bogus' == delta_test.modified_ufo_diffobj_list[0].a_rawpath) is False
    assert ('bogus.bogus' == delta_test.modified_ufo_diffobj_list[1].a_rawpath) is False


def test_ufodiff_delta_get_all_ufo_fp_dict_method():
    delta_test = Delta('.', [], '2')
    fp_dict = delta_test.get_all_ufo_delta_fp_dict()
    assert type(fp_dict) is DeltaFilepathDict
    assert 'added' in fp_dict.delta_dict.keys()
    assert 'deleted' in fp_dict.delta_dict.keys()
    assert 'modified' in fp_dict.delta_dict.keys()
    assert 'commits' in fp_dict.delta_dict.keys()

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
