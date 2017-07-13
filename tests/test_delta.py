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

def make_testing_branch():
    repo = Repo('.')
    gitobj = repo.git
    # create 'test' branch if it doesn't exist so that it can be used for tests in this module
    git_branch_string = gitobj.branch()
    git_branch_list = git_branch_string.split("\n")
    clean_branch_list = []
    for branch in git_branch_list:
        branch = branch.replace('*', '')
        branch = branch.replace(' ', '')
        clean_branch_list.append(branch)
    if 'testing_branch' in clean_branch_list:
        pass
    else:
        gitobj.branch('testing_branch')


def delete_testing_branch():
    repo = Repo('.')
    gitobj = repo.git
    # create 'test' branch if it doesn't exist so that it can be used for tests in this module
    git_branch_string = gitobj.branch()
    git_branch_list = git_branch_string.split("\n")
    clean_branch_list = []
    for branch in git_branch_list:
        branch = branch.replace('*', '')
        branch = branch.replace(' ', '')
        clean_branch_list.append(branch)
    if 'testing_branch' in clean_branch_list:
        gitobj.branch('-d', 'testing_branch')


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
    modified_list.append(os.path.join("source", "Test-Regular.ufo", "features.fea"))
    modified_list.append(os.path.join("source", "Test-Italic.ufo", "features.fea"))
    modified_list.append('CONTRIBUTING.md')
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
    make_testing_branch()

    try:
        deltaobj = Delta('.', [], is_branch_test=True, compare_branch_name='testing_branch')
        assert deltaobj.is_commit_test is False
        assert deltaobj.is_branch_test is True
        assert deltaobj.compare_branch_name == "testing_branch"
        assert deltaobj.commit_number == "0"
        assert len(deltaobj.ufo_directory_list) == 0
    except Exception as e:
        delete_testing_branch()
        pytest.fail(e)

    delete_testing_branch()


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
    make_testing_branch()

    try:
        deltaobj = Delta('.', ['Font-Regular.ufo'], is_branch_test=True, compare_branch_name='testing_branch')
        assert deltaobj.is_commit_test is False
        assert deltaobj.is_branch_test is True
        assert deltaobj.compare_branch_name == "testing_branch"
        assert deltaobj.commit_number == "0"
        assert len(deltaobj.ufo_directory_list) == 1
        assert deltaobj.ufo_directory_list[0] == "Font-Regular.ufo"
    except Exception as e:
        delete_testing_branch()
        pytest.fail(e)

    delete_testing_branch()


def test_ufodiff_delta_add_commit_sha1_method():
    deltaobj = Delta('.', ['Font-Regular.ufo'], is_commit_test=True, commit_number='1')
    # clear sha1 list because defined on instantiation
    deltaobj.commit_sha1_list = []
    assert len(deltaobj.commit_sha1_list) == 0
    deltaobj._add_commit_sha1_to_lists()
    assert len(deltaobj.commit_sha1_list) == 1


def test_ufodiff_delta_validate_ufo_load_dict_method_commit_correct_lists_dicts():
    deltaobj = Delta('.', [], is_commit_test=True, commit_number='1')
    # clear lists that were created on instantiation of the object for testing
    deltaobj.added_ufo_file_list = []
    deltaobj.deleted_ufo_file_list = []
    deltaobj.modified_ufo_file_list = []

    added_testfile_list = get_mock_added_list()
    deleted_testfile_list = get_mock_deleted_list()
    modified_testfile_list = get_mock_modified_list()

    # execute the method to be tested
    deltaobj._validate_ufo_and_load_dict_from_filepath_strings(added_testfile_list, deleted_testfile_list, modified_testfile_list)

    # confirm UFO validations worked
    # added
    assert os.path.join("source", "Test-Regular.ufo", "metainfo.plist") in deltaobj.added_ufo_file_list
    assert os.path.join("source", "Test-Italic.ufo", "metainfo.plist") in deltaobj.added_ufo_file_list
    assert ('README.md' in deltaobj.added_ufo_file_list) is False

    # deleted
    assert os.path.join("source", "Test-Regular.ufo", "fontinfo.plist") in deltaobj.deleted_ufo_file_list
    assert os.path.join("source", "Test-Italic.ufo", "fontinfo.plist") in deltaobj.deleted_ufo_file_list
    assert ('CHANGELOG.md' in deltaobj.deleted_ufo_file_list) is False

    # modified
    assert os.path.join("source", "Test-Regular.ufo", "features.fea") in deltaobj.modified_ufo_file_list
    assert os.path.join("source", "Test-Italic.ufo", "features.fea") in deltaobj.modified_ufo_file_list
    assert ('CONTRIBUTING.md' in deltaobj.modified_ufo_file_list) is False

    # confirm dict keys hold correct file paths
    # added
    assert os.path.join("source", "Test-Regular.ufo", "metainfo.plist") in deltaobj.delta_fp_string_dict.delta_dict['added']
    assert os.path.join("source", "Test-Italic.ufo", "metainfo.plist") in deltaobj.delta_fp_string_dict.delta_dict['added']
    assert ('README.md' in deltaobj.delta_fp_string_dict.delta_dict['added']) is False

    # deleted
    assert os.path.join("source", "Test-Regular.ufo", "fontinfo.plist") in deltaobj.delta_fp_string_dict.delta_dict['deleted']
    assert os.path.join("source", "Test-Italic.ufo", "fontinfo.plist") in deltaobj.delta_fp_string_dict.delta_dict['deleted']
    assert ('CHANGELOG.md' in deltaobj.delta_fp_string_dict.delta_dict['deleted']) is False

    # modified
    assert os.path.join("source", "Test-Regular.ufo", "features.fea") in deltaobj.delta_fp_string_dict.delta_dict['modified']
    assert os.path.join("source", "Test-Italic.ufo", "features.fea") in deltaobj.delta_fp_string_dict.delta_dict['modified']
    assert ('CONTRIBUTING.md' in deltaobj.delta_fp_string_dict.delta_dict['modified']) is False


def test_ufodiff_delta_validate_ufo_load_dict_method_commit_correct_dict_keys():
    deltaobj = Delta('.', [], is_commit_test=True, commit_number='1')
    # clear lists that were created on instantiation of the object for testing
    deltaobj.added_ufo_file_list = []
    deltaobj.deleted_ufo_file_list = []
    deltaobj.modified_ufo_file_list = []

    added_testfile_list = get_mock_added_list()
    deleted_testfile_list = get_mock_deleted_list()
    modified_testfile_list = get_mock_modified_list()

    # execute the method to be tested
    deltaobj._validate_ufo_and_load_dict_from_filepath_strings(added_testfile_list, deleted_testfile_list,
                                                               modified_testfile_list)

    # confirm delta dictionary class object property properly defined with filepaths
    delta_dict = deltaobj.delta_fp_string_dict.delta_dict

    assert 'added' in delta_dict.keys()
    assert 'deleted' in delta_dict.keys()
    assert 'modified' in delta_dict.keys()
    assert 'commits' in delta_dict.keys()
    assert ('branches' in delta_dict.keys()) is False


def test_ufodiff_delta_validate_ufo_load_dict_method_branch_correct_lists_dicts():
    make_testing_branch()

    deltaobj = Delta('.', [], is_branch_test=True, compare_branch_name='testing_branch')
    # clear lists that were created on instantiation of the object for testing
    deltaobj.added_ufo_file_list = []
    deltaobj.deleted_ufo_file_list = []
    deltaobj.modified_ufo_file_list = []

    added_testfile_list = get_mock_added_list()
    deleted_testfile_list = get_mock_deleted_list()
    modified_testfile_list = get_mock_modified_list()

    # execute the method to be tested
    deltaobj._validate_ufo_and_load_dict_from_filepath_strings(added_testfile_list, deleted_testfile_list, modified_testfile_list)

    # confirm UFO validations worked
    # added
    assert os.path.join("source", "Test-Regular.ufo", "metainfo.plist") in deltaobj.added_ufo_file_list
    assert os.path.join("source", "Test-Italic.ufo", "metainfo.plist") in deltaobj.added_ufo_file_list
    assert ('README.md' in deltaobj.added_ufo_file_list) is False

    # deleted
    assert os.path.join("source", "Test-Regular.ufo", "fontinfo.plist") in deltaobj.deleted_ufo_file_list
    assert os.path.join("source", "Test-Italic.ufo", "fontinfo.plist") in deltaobj.deleted_ufo_file_list
    assert ('CHANGELOG.md' in deltaobj.deleted_ufo_file_list) is False

    # modified
    assert os.path.join("source", "Test-Regular.ufo", "features.fea") in deltaobj.modified_ufo_file_list
    assert os.path.join("source", "Test-Italic.ufo", "features.fea") in deltaobj.modified_ufo_file_list
    assert ('CONTRIBUTING.md' in deltaobj.modified_ufo_file_list) is False

    # confirm dict keys hold correct file paths
    # added
    assert os.path.join("source", "Test-Regular.ufo", "metainfo.plist") in deltaobj.delta_fp_string_dict.delta_dict['added']
    assert os.path.join("source", "Test-Italic.ufo", "metainfo.plist") in deltaobj.delta_fp_string_dict.delta_dict['added']
    assert ('README.md' in deltaobj.delta_fp_string_dict.delta_dict['added']) is False

    # deleted
    assert os.path.join("source", "Test-Regular.ufo", "fontinfo.plist") in deltaobj.delta_fp_string_dict.delta_dict['deleted']
    assert os.path.join("source", "Test-Italic.ufo", "fontinfo.plist") in deltaobj.delta_fp_string_dict.delta_dict['deleted']
    assert ('CHANGELOG.md' in deltaobj.delta_fp_string_dict.delta_dict['deleted']) is False

    # modified
    assert os.path.join("source", "Test-Regular.ufo", "features.fea") in deltaobj.delta_fp_string_dict.delta_dict['modified']
    assert os.path.join("source", "Test-Italic.ufo", "features.fea") in deltaobj.delta_fp_string_dict.delta_dict['modified']
    assert ('CONTRIBUTING.md' in deltaobj.delta_fp_string_dict.delta_dict['modified']) is False

    delete_testing_branch()


def test_ufodiff_delta_validate_ufo_load_dict_method_branch_correct_dict_keys():
    make_testing_branch()

    deltaobj = Delta('.', [], is_branch_test=True, compare_branch_name='testing_branch')
    # clear lists that were created on instantiation of the object for testing
    deltaobj.added_ufo_file_list = []
    deltaobj.deleted_ufo_file_list = []
    deltaobj.modified_ufo_file_list = []

    added_testfile_list = get_mock_added_list()
    deleted_testfile_list = get_mock_deleted_list()
    modified_testfile_list = get_mock_modified_list()

    # execute the method to be tested
    deltaobj._validate_ufo_and_load_dict_from_filepath_strings(added_testfile_list, deleted_testfile_list,
                                                               modified_testfile_list)

    # confirm delta dictionary class object property properly defined with filepaths
    delta_dict = deltaobj.delta_fp_string_dict.delta_dict

    assert 'added' in delta_dict.keys()
    assert 'deleted' in delta_dict.keys()
    assert 'modified' in delta_dict.keys()
    assert 'branches' in delta_dict.keys()
    assert ('commits' in delta_dict.keys()) is False

    delete_testing_branch()


def test_ufodiff_delta_get_delta_text_string_method_commit():
    deltaobj = Delta('.', [], is_commit_test=True, commit_number='1')

    added_testfile_list = get_mock_added_list()
    deleted_testfile_list = get_mock_deleted_list()
    modified_testfile_list = get_mock_modified_list()

    # execute the method to be tested
    deltaobj._validate_ufo_and_load_dict_from_filepath_strings(added_testfile_list, deleted_testfile_list,
                                                               modified_testfile_list)

    response_string = deltaobj.get_stdout_string(write_format='text')
    # assert len(response_string) > 0
    assert "Commit history SHA1 for this analysis:" in response_string


def test_ufodiff_delta_get_delta_text_string_method_branch():
    make_testing_branch()

    deltaobj = Delta('.', [], is_branch_test=True, compare_branch_name='testing_branch')

    added_testfile_list = get_mock_added_list()
    deleted_testfile_list = get_mock_deleted_list()
    modified_testfile_list = get_mock_modified_list()

    # execute the method to be tested
    deltaobj._validate_ufo_and_load_dict_from_filepath_strings(added_testfile_list, deleted_testfile_list,
                                                               modified_testfile_list)

    response_string = deltaobj.get_stdout_string(write_format='text')
    # assert len(response_string) > 0
    assert "Branches under analysis:" in response_string

    delete_testing_branch()


def test_ufodiff_delta_get_delta_json_string_method_commit():
    deltaobj = Delta('.', [], is_commit_test=True, commit_number='1')

    added_testfile_list = get_mock_added_list()
    deleted_testfile_list = get_mock_deleted_list()
    modified_testfile_list = get_mock_modified_list()

    # execute the method to be tested
    deltaobj._validate_ufo_and_load_dict_from_filepath_strings(added_testfile_list, deleted_testfile_list,
                                                               modified_testfile_list)

    response_string = deltaobj.get_stdout_string(write_format='json')

    json_obj = json.loads(response_string)
    assert len(response_string) > 0
    assert len(json_obj['commits']) > 0

    # added
    assert os.path.join("source", "Test-Regular.ufo", "metainfo.plist") in json_obj['added']
    assert os.path.join("source", "Test-Italic.ufo", "metainfo.plist") in json_obj['added']
    assert ('README.md' in json_obj['added']) is False

    # deleted
    assert os.path.join("source", "Test-Regular.ufo", "fontinfo.plist") in json_obj['deleted']
    assert os.path.join("source", "Test-Italic.ufo", "fontinfo.plist") in json_obj['deleted']
    assert ('CHANGELOG.md' in json_obj['deleted']) is False

    # modified
    assert os.path.join("source", "Test-Regular.ufo", "features.fea") in json_obj['modified']
    assert os.path.join("source", "Test-Italic.ufo", "features.fea") in json_obj['modified']
    assert ('CONTRIBUTING.md' in json_obj['modified']) is False


def test_ufodiff_delta_get_delta_json_string_method_branch():
    make_testing_branch()

    deltaobj = Delta('.', [], is_branch_test=True, compare_branch_name='testing_branch')

    added_testfile_list = get_mock_added_list()
    deleted_testfile_list = get_mock_deleted_list()
    modified_testfile_list = get_mock_modified_list()

    # execute the method to be tested
    deltaobj._validate_ufo_and_load_dict_from_filepath_strings(added_testfile_list, deleted_testfile_list,
                                                               modified_testfile_list)

    response_string = deltaobj.get_stdout_string(write_format='json')

    json_obj = json.loads(response_string)
    assert len(response_string) > 0
    assert len(json_obj['branches']) > 0

    # added
    assert os.path.join("source", "Test-Regular.ufo", "metainfo.plist") in json_obj['added']
    assert os.path.join("source", "Test-Italic.ufo", "metainfo.plist") in json_obj['added']
    assert ('README.md' in json_obj['added']) is False

    # deleted
    assert os.path.join("source", "Test-Regular.ufo", "fontinfo.plist") in json_obj['deleted']
    assert os.path.join("source", "Test-Italic.ufo", "fontinfo.plist") in json_obj['deleted']
    assert ('CHANGELOG.md' in json_obj['deleted']) is False

    # modified
    assert os.path.join("source", "Test-Regular.ufo", "features.fea") in json_obj['modified']
    assert os.path.join("source", "Test-Italic.ufo", "features.fea") in json_obj['modified']
    assert ('CONTRIBUTING.md' in json_obj['modified']) is False

    delete_testing_branch()


def test_ufodiff_delta_get_delta_markdown_string_method_commit():
    deltaobj = Delta('.', [], is_commit_test=True, commit_number='1')

    added_testfile_list = get_mock_added_list()
    deleted_testfile_list = get_mock_deleted_list()
    modified_testfile_list = get_mock_modified_list()

    # execute the method to be tested
    deltaobj._validate_ufo_and_load_dict_from_filepath_strings(added_testfile_list, deleted_testfile_list,
                                                               modified_testfile_list)

    response_string = deltaobj.get_stdout_string(write_format='markdown')

    assert len(response_string) > 0

    # added
    assert os.path.join("source", "Test-Regular.ufo", "metainfo.plist") in response_string
    assert os.path.join("source", "Test-Italic.ufo", "metainfo.plist") in response_string
    assert ('README.md' in response_string) is False

    # deleted
    assert os.path.join("source", "Test-Regular.ufo", "fontinfo.plist") in response_string
    assert os.path.join("source", "Test-Italic.ufo", "fontinfo.plist") in response_string
    assert ('CHANGELOG.md' in response_string) is False

    # modified
    assert os.path.join("source", "Test-Regular.ufo", "features.fea") in response_string
    assert os.path.join("source", "Test-Italic.ufo", "features.fea") in response_string
    assert ('CONTRIBUTING.md' in response_string) is False


def test_ufodiff_delta_get_delta_markdown_string_method_branch():
    make_testing_branch()

    deltaobj = Delta('.', [], is_branch_test=True, compare_branch_name='testing_branch')

    added_testfile_list = get_mock_added_list()
    deleted_testfile_list = get_mock_deleted_list()
    modified_testfile_list = get_mock_modified_list()

    # execute the method to be tested
    deltaobj._validate_ufo_and_load_dict_from_filepath_strings(added_testfile_list, deleted_testfile_list,
                                                               modified_testfile_list)

    response_string = deltaobj.get_stdout_string(write_format='markdown')

    assert len(response_string) > 0

    # added
    assert os.path.join("source", "Test-Regular.ufo", "metainfo.plist") in response_string
    assert os.path.join("source", "Test-Italic.ufo", "metainfo.plist") in response_string
    assert ('README.md' in response_string) is False

    # deleted
    assert os.path.join("source", "Test-Regular.ufo", "fontinfo.plist") in response_string
    assert os.path.join("source", "Test-Italic.ufo", "fontinfo.plist") in response_string
    assert ('CHANGELOG.md' in response_string) is False

    # modified
    assert os.path.join("source", "Test-Regular.ufo", "features.fea") in response_string
    assert os.path.join("source", "Test-Italic.ufo", "features.fea") in response_string
    assert ('CONTRIBUTING.md' in response_string) is False

    delete_testing_branch()


# ///////////////////////////////////////////////////////
#
#  DeltaFilepathStringDict class tests
#
# ///////////////////////////////////////////////////////

def test_ufodiff_dfpd_instantiation_empty_fp_list():   # user did not specify UFO source filter so list arg empty
    dfpd = DeltaFilepathStringDict([])
    assert len(dfpd.ufo_directory_list) == 0


def test_ufodiff_dfpd_instantiation_nonempty_fp_list():  # user did specify UFO source filter so list arg not empty
    filepath_list = ['Font-Regular.ufo', 'Font-Italic.ufo']
    dfpd = DeltaFilepathStringDict(filepath_list)
    assert len(dfpd.ufo_directory_list) == 2
    assert 'Font-Regular.ufo' in dfpd.ufo_directory_list
    assert 'Font-Italic.ufo' in dfpd.ufo_directory_list


def test_ufodiff_dfpd_add_added_fp_method():
    dfpd = DeltaFilepathStringDict([])
    dfpd2 = DeltaFilepathStringDict(['Test-Regular.ufo'])
    dfpd3 = DeltaFilepathStringDict(['Test-Regular.ufo'])
    added_list = [os.path.join('source', 'NotPath-Regular.ufo', 'fontinfo.plist')]
    added_filterpath_list = [os.path.join('source', 'Test-Regular.ufo', 'metainfo.plist')]

    # this one tests when no user requested source filter applied
    dfpd.add_added_filepaths(added_list)
    # this one tests when file path is not on source filter filepath, should remain empty
    dfpd2.add_added_filepaths(added_list)
    # this one tests when file path is on source filter path, should include in the dictionary
    dfpd3.add_added_filepaths(added_filterpath_list)

    assert len(dfpd.delta_dict['added']) == 1
    assert dfpd.delta_dict['added'][0] == os.path.join('source', 'NotPath-Regular.ufo', 'fontinfo.plist')

    assert len(dfpd2.delta_dict['added']) == 0

    assert len(dfpd3.delta_dict['added']) == 1
    assert dfpd3.delta_dict['added'][0] == os.path.join("source", "Test-Regular.ufo", "metainfo.plist")


def test_ufodiff_dfpd_add_deleted_fp_method():
    dfpd = DeltaFilepathStringDict([])
    dfpd2 = DeltaFilepathStringDict(['Test-Regular.ufo'])
    dfpd3 = DeltaFilepathStringDict(['Test-Regular.ufo'])
    deleted_list = [os.path.join('source', 'NotPath-Regular.ufo', 'fontinfo.plist')]
    deleted_filterpath_list = [os.path.join('source', 'Test-Regular.ufo', 'metainfo.plist')]

    # this one tests when no user requested source filter applied
    dfpd.add_deleted_filepaths(deleted_list)
    # this one tests when file path is not on source filter filepath, should remain empty
    dfpd2.add_deleted_filepaths(deleted_list)
    # this one tests when file path is on source filter path, should include in the dictionary
    dfpd3.add_deleted_filepaths(deleted_filterpath_list)

    assert len(dfpd.delta_dict['deleted']) == 1
    assert dfpd.delta_dict['deleted'][0] == os.path.join('source', 'NotPath-Regular.ufo', 'fontinfo.plist')

    assert len(dfpd2.delta_dict['deleted']) == 0

    assert len(dfpd3.delta_dict['deleted']) == 1
    assert dfpd3.delta_dict['deleted'][0] == os.path.join("source", "Test-Regular.ufo", "metainfo.plist")


def test_ufodiff_dfpd_add_modified_fp_method():
    dfpd = DeltaFilepathStringDict([])
    dfpd2 = DeltaFilepathStringDict(['Test-Regular.ufo'])
    dfpd3 = DeltaFilepathStringDict(['Test-Regular.ufo'])
    modified_list = [os.path.join('source', 'NotPath-Regular.ufo', 'fontinfo.plist')]
    modified_filterpath_list = [os.path.join('source', 'Test-Regular.ufo', 'metainfo.plist')]

    # this one tests when no user requested source filter applied
    dfpd.add_modified_filepaths(modified_list)
    # this one tests when file path is not on source filter filepath, should remain empty
    dfpd2.add_modified_filepaths(modified_list)
    # this one tests when file path is on source filter path, should include in the dictionary
    dfpd3.add_modified_filepaths(modified_filterpath_list)

    assert len(dfpd.delta_dict['modified']) == 1
    assert dfpd.delta_dict['modified'][0] == os.path.join('source', 'NotPath-Regular.ufo', 'fontinfo.plist')

    assert len(dfpd2.delta_dict['modified']) == 0

    assert len(dfpd3.delta_dict['modified']) == 1
    assert dfpd3.delta_dict['modified'][0] == os.path.join("source", "Test-Regular.ufo", "metainfo.plist")


