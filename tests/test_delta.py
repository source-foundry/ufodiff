#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import pytest
import json

from git import Repo

from ufodiff.subcommands.delta import Delta, DeltaFilepathStringDict


# # Mock Diffable class for unit tests - need to assign values in tests
# class MockDiffableObj(object):
#     def __init__(self):
#         self.a_rawpath = ""
#         self.new_file = True
#         self.deleted_file = True
#         self.change_type = "M"
#
#
# def get_mock_newfile():
#     mdo = MockDiffableObj()
#     mdo.a_rawpath = "fontinfo.plist"
#     mdo.new_file = True
#     mdo.deleted_file = False
#     mdo.change_type = "Z"
#     return mdo
#
#
# def get_mock_deleted_file():
#     mdo = MockDiffableObj()
#     mdo.a_rawpath = "features.fea"
#     mdo.new_file = False
#     mdo.deleted_file = True
#     mdo.change_type = "Z"
#     return mdo
#
#
# def get_mock_modified_file_nonglyph():
#     mdo = MockDiffableObj()
#     mdo.a_rawpath = "metainfo.plist"
#     mdo.new_file = False
#     mdo.deleted_file = False
#     mdo.change_type = "M"
#     return mdo
#
#
# def get_mock_modified_file_glyph():
#     mdo = MockDiffableObj()
#     mdo.a_rawpath = "A.glif"
#     mdo.new_file = False
#     mdo.deleted_file = False
#     mdo.change_type = "M"
#     return mdo
#
#
# def get_mock_modified_file_invalidufo():
#     # not valid UFO file
#     mdo = MockDiffableObj()
#     mdo.a_rawpath = "bogus.bogus"
#     mdo.new_file = True
#     mdo.deleted_file = True
#     mdo.change_type = "M"
#     return mdo
#
#
# def get_mock_allchange_file_with_filterpath():
#     mdo = MockDiffableObj()
#     mdo.a_rawpath = os.path.join("source", "Test-Regular.ufo", "metainfo.plist")
#     mdo.new_file = True
#     mdo.deleted_file = True
#     mdo.change_type = "M"
#     return mdo


def get_mock_added_list():
    added_list = []
    added_list.append(os.path.join("source", "Test-Regular.ufo", "metainfo.plist"))
    added_list.append(os.path.join("source", "Test-Italic.ufo", "metainfo.plist"))
    added_list.append('README.md')
    return added_list


def get_mock_deleted_list():
    deleted_list = []
    deleted_list.append(os.path.join("source", "Test-Regular.ufo", "fontinfo.plist"))
    deleted_list.append(os.path.join("source", "Test-Italic.ufo", "fontinfo.plist"))
    deleted_list.append('CHANGELOG.md')
    return deleted_list


def get_mock_modified_list():
    modified_list = []
    modified_list.append(os.path.join("source", "Test-Regular.ufo", "fontinfo.plist"))
    modified_list.append(os.path.join("source", "Test-Italic.ufo", "fontinfo.plist"))
    modified_list.append('CHANGELOG.md')
    return modified_list



# ///////////////////////////////////////////////////////
#
#  Delta class tests
#
# ///////////////////////////////////////////////////////

def test_ufodiff_delta_class_instantiation_commit():
    try:
        deltaobj = Delta('.', [], is_commit_test=True, commit_number='2')
        assert deltaobj.is_commit_test is True
        assert deltaobj.is_branch_test is False
        assert deltaobj.commit_number == "2"
        assert deltaobj.compare_branch_name is None
        assert len(deltaobj.ufo_directory_list) == 0
    except Exception as e:
        pytest.fail(e)


def test_ufodiff_delta_class_instantiation_branch():
    try:
        deltaobj = Delta('.', [], is_branch_test=True, compare_branch_name='test')
        assert deltaobj.is_commit_test is False
        assert deltaobj.is_branch_test is True
        assert deltaobj.compare_branch_name == "test"
        assert deltaobj.commit_number == "0"
        assert len(deltaobj.ufo_directory_list) == 0
    except Exception as e:
        pytest.fail(e)


def test_ufodiff_delta_class_instantiation_commit_with_ufo_filter():
    try:
        deltaobj = Delta('.', ['Font-Regular.ufo'], is_commit_test=True, commit_number='2')
        assert deltaobj.is_commit_test is True
        assert deltaobj.is_branch_test is False
        assert deltaobj.commit_number == "2"
        assert deltaobj.compare_branch_name is None
        assert len(deltaobj.ufo_directory_list) == 1
        assert deltaobj.ufo_directory_list[0] == "Font-Regular.ufo"
    except Exception as e:
        pytest.fail(e)


def test_ufodiff_delta_class_instantiation_branch_with_ufo_filter():
    try:
        deltaobj = Delta('.', ['Font-Regular.ufo'], is_branch_test=True, compare_branch_name='test')
        assert deltaobj.is_commit_test is False
        assert deltaobj.is_branch_test is True
        assert deltaobj.compare_branch_name == "test"
        assert deltaobj.commit_number == "0"
        assert len(deltaobj.ufo_directory_list) == 1
        assert deltaobj.ufo_directory_list[0] == "Font-Regular.ufo"
    except Exception as e:
        pytest.fail(e)


def test_ufodiff_delta_add_commit_sha1_method():
    deltaobj = Delta('.', ['Font-Regular.ufo'], is_commit_test=True, commit_number='1')
    # clear sha1 list because defined on instantiation
    deltaobj.commit_sha1_list = []
    assert len(deltaobj.commit_sha1_list) == 0
    deltaobj._add_commit_sha1_to_lists()
    assert len(deltaobj.commit_sha1_list) == 1


# def test_ufodiff_delta_get_all_ufo_fp_dict_method():
#     delta_test = Delta('.', [], '2')
#     fp_dict = delta_test.get_all_ufo_delta_fp_dict()
#     assert type(fp_dict) is DeltaFilepathDict
#     assert 'added' in fp_dict.delta_dict.keys()
#     assert 'deleted' in fp_dict.delta_dict.keys()
#     assert 'modified' in fp_dict.delta_dict.keys()
#     assert 'commits' in fp_dict.delta_dict.keys()
#
#
# # ///////////////////////////////////////////////////////
# #
# #  DeltaFilepathDict class tests
# #
# # ///////////////////////////////////////////////////////
#
# def test_ufodiff_dfpd_instantiation_empty_fp_list():   # user did not specify UFO source filter so list arg empty
#     dfpd = DeltaFilepathDict([])
#     assert len(dfpd.ufo_directory_list) == 0
#
#
# def test_ufodiff_dfpd_instantiation_nonempty_fp_list():  # user did specify UFO source filter so list arg not empty
#     filepath_list = ['Font-Regular.ufo', 'Font-Italic.ufo']
#     dfpd = DeltaFilepathDict(filepath_list)
#     assert len(dfpd.ufo_directory_list) == 2
#     assert 'Font-Regular.ufo' in dfpd.ufo_directory_list
#     assert 'Font-Italic.ufo' in dfpd.ufo_directory_list
#
#
# def test_ufodiff_dfpd_add_added_fp_method():
#     dfpd = DeltaFilepathDict([])
#     dfpd2 = DeltaFilepathDict(['Test-Regular.ufo'])
#     dfpd3 = DeltaFilepathDict(['Test-Regular.ufo'])
#     added_list = [get_mock_newfile()]
#     added_filterpath_list = [get_mock_allchange_file_with_filterpath()]
#
#     # this one tests when no user requested source filter applied
#     dfpd.add_added_filepaths(added_list)
#     # this one tests when file path is not on source filter filepath, should remain empty
#     dfpd2.add_added_filepaths(added_list)
#     # this one tests when file path is on source filter path, should include in the dictionary
#     dfpd3.add_added_filepaths(added_filterpath_list)
#
#     assert len(dfpd.delta_dict['added']) == 1
#     assert dfpd.delta_dict['added'][0] == "fontinfo.plist"
#
#     assert len(dfpd2.delta_dict['added']) == 0
#
#     assert len(dfpd3.delta_dict['added']) == 1
#     assert dfpd3.delta_dict['added'][0] == os.path.join("source", "Test-Regular.ufo", "metainfo.plist")
#
#
# def test_ufodiff_dfpd_add_deleted_fp_method():
#     dfpd = DeltaFilepathDict([])
#     dfpd2 = DeltaFilepathDict(['Test-Regular.ufo'])
#     dfpd3 = DeltaFilepathDict(['Test-Regular.ufo'])
#     deleted_list = [get_mock_deleted_file()]
#     deleted_filterpath_list = [get_mock_allchange_file_with_filterpath()]
#
#     # this one tests when no user requested source filter applied
#     dfpd.add_deleted_filepaths(deleted_list)
#     # this one tests when not on source filter filepath, should be empty
#     dfpd2.add_deleted_filepaths(deleted_list)
#     # this one tests when file path is on source filter path, should include in the dictionary
#     dfpd3.add_deleted_filepaths(deleted_filterpath_list)
#
#     assert len(dfpd.delta_dict['deleted']) == 1
#     assert dfpd.delta_dict['deleted'][0] == "features.fea"
#
#     assert len(dfpd2.delta_dict['deleted']) == 0
#
#     assert len(dfpd3.delta_dict['deleted']) == 1
#     assert dfpd3.delta_dict['deleted'][0] == os.path.join("source", "Test-Regular.ufo", "metainfo.plist")
#
#
# def test_ufodiff_dfpd_add_modified_fp_method():
#     dfpd = DeltaFilepathDict([])
#     dfpd2 = DeltaFilepathDict(['Test-Regular.ufo'])
#     dfpd3 = DeltaFilepathDict(['Test-Regular.ufo'])
#     mod_list = []
#     mod_list.append(get_mock_modified_file_nonglyph())
#     mod_list.append(get_mock_modified_file_glyph())
#
#     mod_filterpaths_list = []
#     mod_filterpaths_list.append(get_mock_allchange_file_with_filterpath())  # load with the same file path for testing
#     mod_filterpaths_list.append(get_mock_allchange_file_with_filterpath())  # iteration of file paths
#
#     # this one tests when no user requested source filter applied
#     dfpd.add_modified_filepaths(mod_list)
#     # this one tests when not on source filter filepath, should be empty
#     dfpd2.add_modified_filepaths(mod_list)
#     # this one tests when file path is on source filter path, should include in the dictionary
#     dfpd3.add_modified_filepaths(mod_filterpaths_list)
#
#     assert len(dfpd.delta_dict['modified']) == 2
#     assert dfpd.delta_dict['modified'][0] == "metainfo.plist"
#     assert dfpd.delta_dict['modified'][1] == "A.glif"
#
#     assert len(dfpd2.delta_dict['modified']) == 0
#
#     assert len(dfpd3.delta_dict['modified']) == 2
#     assert dfpd3.delta_dict['modified'][0] == os.path.join("source", "Test-Regular.ufo", "metainfo.plist")
#     assert dfpd3.delta_dict['modified'][1] == os.path.join("source", "Test-Regular.ufo", "metainfo.plist")
#
#
# def test_ufodiff_dfpd_add_commit_sha1_method():
#     sha1_list = ['1a3e2f', '2c2eff']
#     dfpd = DeltaFilepathDict([])
#     dfpd.add_commit_sha1(sha1_list)
#
#     assert len(dfpd.delta_dict['commits']) == 2
#     for sha1 in sha1_list:
#         assert (sha1 in dfpd.delta_dict['commits']) is True
#
#
# # ///////////////////////////////////////////////////////
# #
# #  get_delta_string function tests
# #
# # ///////////////////////////////////////////////////////
#
#
# class MockDeltaDictObj(object):
#     def __init__(self):
#         self.delta_dict = {
#             'commits': ['ff418e4d', '73fee88'],
#             'added': ['Test-Regular.ufo/fontinfo.plist', 'Test-Regular.ufo/metainfo.plist'],
#             'deleted': ['Test-Regular.ufo/features.fea'],
#             'modified': ['Test-Regular.ufo/glyphs/A.glif', 'Test-Regular.ufo/glyphs/B.glif']
#         }
#
#
# class MockDeltaDictObj_MissingAdded(object):
#     def __init__(self):
#         self.delta_dict = {
#             'commits': ['ff418e4d', '73fee88'],
#             'added': [],
#             'deleted': ['Test-Regular.ufo/features.fea'],
#             'modified': ['Test-Regular.ufo/glyphs/A.glif', 'Test-Regular.ufo/glyphs/B.glif']
#         }
#
#
# class MockDeltaDictObj_MissingDeleted(object):
#     def __init__(self):
#         self.delta_dict = {
#             'commits': ['ff418e4d', '73fee88'],
#             'added': ['Test-Regular.ufo/fontinfo.plist', 'Test-Regular.ufo/metainfo.plist'],
#             'deleted': [],
#             'modified': ['Test-Regular.ufo/glyphs/A.glif', 'Test-Regular.ufo/glyphs/B.glif']
#         }
#
#
# class MockDeltaDictObj_MissingModified(object):
#     def __init__(self):
#         self.delta_dict = {
#             'commits': ['ff418e4d', '73fee88'],
#             'added': ['Test-Regular.ufo/fontinfo.plist', 'Test-Regular.ufo/metainfo.plist'],
#             'deleted': ['Test-Regular.ufo/features.fea'],
#             'modified': []
#         }
#
#
# def test_ufodiff_getdeltastring_text():
#     mddo = MockDeltaDictObj()
#     test_string = get_delta_string(mddo, write_format='text')
#     assert 'ff418e4d' in test_string
#     assert '73fee88' in test_string
#     assert 'Test-Regular.ufo/fontinfo.plist' in test_string
#     assert 'Test-Regular.ufo/metainfo.plist' in test_string
#     assert 'Test-Regular.ufo/glyphs/A.glif' in test_string
#     assert 'Test-Regular.ufo/glyphs/B.glif' in test_string
#
#
# def test_ufodiff_getdeltastring_json():
#     mddo = MockDeltaDictObj()
#     test_string = get_delta_string(mddo, write_format='json')
#     returned_json_obj = json.loads(test_string)
#     assert returned_json_obj['commits'] == ['ff418e4d', '73fee88']
#     assert len(returned_json_obj['commits']) == 2
#     assert returned_json_obj['added'] == ['Test-Regular.ufo/fontinfo.plist', 'Test-Regular.ufo/metainfo.plist']
#     assert len(returned_json_obj['added']) == 2
#     assert returned_json_obj['deleted'] == ['Test-Regular.ufo/features.fea']
#     assert len(returned_json_obj['deleted']) == 1
#     assert returned_json_obj['modified'] == ['Test-Regular.ufo/glyphs/A.glif', 'Test-Regular.ufo/glyphs/B.glif']
#     assert len(returned_json_obj['modified']) == 2
#
#
# def test_ufodiff_getdeltastring_md():
#     mddo = MockDeltaDictObj()
#     test_string = get_delta_string(mddo, write_format='markdown')
#     assert 'ff418e4d' in test_string
#     assert '73fee88' in test_string
#     assert 'Test-Regular.ufo/fontinfo.plist' in test_string
#     assert 'Test-Regular.ufo/metainfo.plist' in test_string
#     assert 'Test-Regular.ufo/glyphs/A.glif' in test_string
#     assert 'Test-Regular.ufo/glyphs/B.glif' in test_string
#     assert 'Test-Regular.ufo/features.fea' in test_string
#
#
# def test_ufodiff_getdeltastring_md_missing_added():
#     mddo = MockDeltaDictObj_MissingAdded()
#     test_string = get_delta_string(mddo, write_format='markdown')
#     assert 'ff418e4d' in test_string
#     assert '73fee88' in test_string
#     assert 'Test-Regular.ufo/glyphs/A.glif' in test_string
#     assert 'Test-Regular.ufo/glyphs/B.glif' in test_string
#     assert 'None' in test_string
#
#
# def test_ufodiff_getdeltastring_md_missing_deleted():
#     mddo = MockDeltaDictObj_MissingDeleted()
#     test_string = get_delta_string(mddo, write_format='markdown')
#     assert 'ff418e4d' in test_string
#     assert '73fee88' in test_string
#     assert 'Test-Regular.ufo/fontinfo.plist' in test_string
#     assert 'Test-Regular.ufo/metainfo.plist' in test_string
#     assert 'Test-Regular.ufo/glyphs/A.glif' in test_string
#     assert 'Test-Regular.ufo/glyphs/B.glif' in test_string
#     assert 'None' in test_string
#
#
# def test_ufodiff_getdeltastring_md_missing_modified():
#     mddo = MockDeltaDictObj_MissingModified()
#     test_string = get_delta_string(mddo, write_format='markdown')
#     assert 'ff418e4d' in test_string
#     assert '73fee88' in test_string
#     assert 'Test-Regular.ufo/fontinfo.plist' in test_string
#     assert 'Test-Regular.ufo/metainfo.plist' in test_string
#     assert 'Test-Regular.ufo/features.fea' in test_string
#     assert 'None' in test_string
