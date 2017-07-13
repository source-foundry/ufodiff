#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import pytest
import mock

from git import Repo

from ufodiff.app import get_git_root_path


# creates a temporary new git branch (testing_branch) for testing
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


# deletes the temporary new git branch (testing_branch) for testing
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

# ///////////////////////////////////////////////////////
#
# pytest capsys capture tests
#    confirms capture of std output and std error streams
#
# ///////////////////////////////////////////////////////


def test_pytest_capsys(capsys):
    print("bogus text for a test")
    sys.stderr.write("more text for a test")
    out, err = capsys.readouterr()
    assert out == "bogus text for a test\n"
    assert out != "something else"
    assert err == "more text for a test"
    assert err != "something else"


# ///////////////////////////////////////////////////////
#
# Standard output tests for help, usage, version
#
# ///////////////////////////////////////////////////////

def test_ufodiff_commandline_shorthelp(capsys):
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        from ufodiff.app import main
        sys.argv = ['ufodiff', '-h']
        main()

    out, err = capsys.readouterr()
    assert out.startswith("====================================================") is True
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 0


def test_ufodiff_commandline_longhelp(capsys):
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        from ufodiff.app import main
        sys.argv = ['ufodiff', '--help']
        main()

    out, err = capsys.readouterr()
    assert out.startswith("====================================================") is True
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 0


def test_ufodiff_commandline_shortversion(capsys):
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        from ufodiff.app import main
        from ufodiff.app import settings
        sys.argv = ['ufodiff', '-v']
        main()

    out, err = capsys.readouterr()
    assert out.startswith(settings.VERSION)
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 0


def test_ufodiff_commandline_longversion(capsys):
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        from ufodiff.app import main
        from ufodiff.app import settings
        sys.argv = ['ufodiff', '--version']
        main()

    out, err = capsys.readouterr()
    assert out.startswith(settings.VERSION)
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 0


def test_ufodiff_commandline_longusage(capsys):
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        from ufodiff.app import main
        from ufodiff.app import settings
        sys.argv = ['ufodiff', '--usage']
        main()

    out, err = capsys.readouterr()
    assert out.startswith(settings.USAGE)
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 0


# ///////////////////////////////////////////////////////////////////
#
# Standard output tests for non-command specific argument validations
#
# ///////////////////////////////////////////////////////////////////

def test_ufodiff_commandline_missingargs(capsys):
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        from ufodiff.app import main
        sys.argv = ['ufodiff']
        main()

    out, err = capsys.readouterr()
    assert err.startswith("[ufodiff] ERROR: Please include the appropriate arguments")
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 1

# ////////////////////////////////////////////////////////////
#
# Standard output tests for delta command argument validations
#
# ////////////////////////////////////////////////////////////


def test_ufodiff_commandline_delta_missingargs(capsys):
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        from ufodiff.app import main
        sys.argv = ['ufodiff', 'delta']
        main()

    out, err = capsys.readouterr()
    assert err.startswith("[ufodiff] ERROR: ")
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 1


def test_ufodiff_commandline_delta_unacceptable_subsub(capsys):
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        from ufodiff.app import main
        sys.argv = ['ufodiff', 'delta', 'bogus', 'commits:1']
        main()

    out, err = capsys.readouterr()
    assert err.startswith("[ufodiff] ERROR:")
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 1


def test_ufodiff_commandline_delta_missing_commits_arg(capsys):
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        from ufodiff.app import main
        sys.argv = ['ufodiff', 'delta', 'all', 'bogus']
        main()

    out, err = capsys.readouterr()
    assert err.startswith("[ufodiff] ERROR:")
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 1


def test_ufodiff_commandline_delta_missing_commits_number(capsys):
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        from ufodiff.app import main
        sys.argv = ['ufodiff', 'delta', 'all', 'commits:']
        main()

    out, err = capsys.readouterr()
    assert err.startswith("[ufodiff] ERROR:")
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 1


def test_ufodiff_commandline_delta_commits_number_notdigit(capsys):
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        from ufodiff.app import main
        sys.argv = ['ufodiff', 'delta', 'all', 'commits:a']
        main()

    out, err = capsys.readouterr()
    assert err.startswith("[ufodiff] ERROR:")
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 1


def test_ufodiff_commandline_delta_missing_branch_name(capsys):
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        from ufodiff.app import main
        sys.argv = ['ufodiff', 'delta', 'all', 'branch:']
        main()

    out, err = capsys.readouterr()
    assert err.startswith("[ufodiff] ERROR:")
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 1


def test_commandline_delta_existing_branch_name(capsys):
    make_testing_branch()

    with pytest.raises(SystemExit) as pytest_wrapped_e:
        from ufodiff.app import main
        sys.argv = ['ufodiff', 'delta', 'all', 'branch:testing_branch']
        main()

    out, err = capsys.readouterr()
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 0

    delete_testing_branch()


def test_ufodiff_commandline_delta_commits_number_with_ufo_filter(capsys):
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        from ufodiff.app import main
        sys.argv = ['ufodiff', 'delta', 'all', 'commits:1', 'Test-Regular.ufo']
        main()

    out, err = capsys.readouterr()
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 0


def test_ufodiff_commandline_delta_git_root_check_one_level_below(capsys):
    the_cwd = os.getcwd()
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        from ufodiff.app import main
        sys.argv = ['ufodiff', 'delta', 'all', 'commits:1']
        os.chdir(os.path.join(the_cwd, 'tests'))
        main()

    out, err = capsys.readouterr()
    os.chdir(the_cwd)
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 0


def test_ufodiff_commandline_delta_git_root_check_two_levels_below(capsys):
    the_cwd = os.getcwd()
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        from ufodiff.app import main
        sys.argv = ['ufodiff', 'delta', 'all', 'commits:1']
        os.chdir(os.path.join(the_cwd, 'tests', 'testfiles'))
        main()

    out, err = capsys.readouterr()
    os.chdir(the_cwd)
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 0


def test_ufodiff_commandline_delta_git_root_check_three_levels_below(capsys):
    the_cwd = os.getcwd()
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        from ufodiff.app import main
        sys.argv = ['ufodiff', 'delta', 'all', 'commits:1']
        os.chdir(os.path.join(the_cwd, 'tests', 'testfiles', 'depth2'))
        main()

    out, err = capsys.readouterr()
    os.chdir(the_cwd)
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 0


# should fail at depth of four directory levels deep in the repository
def test_ufodiff_commandline_delta_git_root_check_four_levels_below(capsys):
    the_cwd = os.getcwd()
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        from ufodiff.app import main
        sys.argv = ['ufodiff', 'delta', 'all', 'commits:1']
        os.chdir(os.path.join(the_cwd, 'tests', 'testfiles', 'depth2', 'depth3'))
        main()

    out, err = capsys.readouterr()
    os.chdir(the_cwd)
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 1


def test_ufodiff_commandline_delta_commits_number_is_zero(capsys):
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        from ufodiff.app import main
        sys.argv = ['ufodiff', 'delta', 'all', 'commits:0']
        main()

    out, err = capsys.readouterr()
    assert err.startswith("[ufodiff] ERROR:")
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 1


def test_ufodiff_commandline_delta_commits_number_is_lessthan_zero(capsys):
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        from ufodiff.app import main
        sys.argv = ['ufodiff', 'delta', 'all', 'commits:-1']
        main()

    out, err = capsys.readouterr()
    assert err.startswith("[ufodiff] ERROR:")
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 1


## SUCCESS COMMANDS FOR DELTAJSON and DELTAMD

def test_ufodiff_commandline_deltajson_exit_success(capsys):
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        from ufodiff.app import main
        sys.argv = ['ufodiff', 'deltajson', 'all', 'commits:2']
        main()

    out, err = capsys.readouterr()
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 0


def test_ufodiff_commandline_deltamd_exit_success(capsys):
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        from ufodiff.app import main
        sys.argv = ['ufodiff', 'deltamd', 'all', 'commits:2']
        main()

    out, err = capsys.readouterr()
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 0


# ////////////////////////////////////////////////////////////
#
# Standard output tests for diff + diffnc command argument validations
#
# ////////////////////////////////////////////////////////////

def test_ufodiff_commandline_diff_missingargs(capsys):
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        from ufodiff.app import main
        sys.argv = ['ufodiff', 'diff']
        main()

    out, err = capsys.readouterr()
    assert err.startswith("[ufodiff] ERROR: ")
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 1


def test_ufodiff_commandline_diffnc_missingargs(capsys):
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        from ufodiff.app import main
        sys.argv = ['ufodiff', 'diffnc']
        main()

    out, err = capsys.readouterr()
    assert err.startswith("[ufodiff] ERROR: ")
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 1


def test_ufodiff_commandline_diff_missing_commits(capsys):
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        from ufodiff.app import main
        sys.argv = ['ufodiff', 'diff', 'commits:']
        main()

    out, err = capsys.readouterr()
    assert err.startswith("[ufodiff] ERROR:")
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 1


def test_ufodiff_commandline_diffnc_missing_commits(capsys):
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        from ufodiff.app import main
        sys.argv = ['ufodiff', 'diffnc', 'commits:']
        main()

    out, err = capsys.readouterr()
    assert err.startswith("[ufodiff] ERROR:")
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 1


def test_ufodiff_commandline_diff_missing_branch(capsys):
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        from ufodiff.app import main
        sys.argv = ['ufodiff', 'diff', 'branch:']
        main()

    out, err = capsys.readouterr()
    assert err.startswith("[ufodiff] ERROR:")
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 1


def test_ufodiff_commandline_diffnc_missing_branch(capsys):
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        from ufodiff.app import main
        sys.argv = ['ufodiff', 'diffnc', 'branch:']
        main()

    out, err = capsys.readouterr()
    assert err.startswith("[ufodiff] ERROR:")
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 1


def test_ufodiff_commandline_diff_success_commits_arg(capsys):
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        from ufodiff.app import main
        sys.argv = ['ufodiff', 'diff', 'commits:1']
        main()

    out, err = capsys.readouterr()
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 0


def test_ufodiff_commandline_diffnc_success_commits_arg(capsys):
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        from ufodiff.app import main
        sys.argv = ['ufodiff', 'diffnc', 'commits:1']
        main()

    out, err = capsys.readouterr()
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 0


def test_ufodiff_commandline_diff_success_branch_arg(capsys):
    make_testing_branch()

    with pytest.raises(SystemExit) as pytest_wrapped_e:
        from ufodiff.app import main
        sys.argv = ['ufodiff', 'diff', 'branch:testing_branch']
        main()

    out, err = capsys.readouterr()
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 0

    delete_testing_branch()


def test_ufodiff_commandline_diffnc_success_branch_arg(capsys):
    make_testing_branch()

    with pytest.raises(SystemExit) as pytest_wrapped_e:
        from ufodiff.app import main
        sys.argv = ['ufodiff', 'diffnc', 'branch:testing_branch']
        main()

    out, err = capsys.readouterr()
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 0

    delete_testing_branch()


def test_ufodiff_commandline_diff_success_git_arg(capsys):
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        from ufodiff.app import main
        sys.argv = ['ufodiff', 'diff', 'HEAD~1']
        main()

    out, err = capsys.readouterr()
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 0


def test_ufodiff_commandline_diffnc_success_git_arg(capsys):
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        from ufodiff.app import main
        sys.argv = ['ufodiff', 'diffnc', 'HEAD~1']
        main()

    out, err = capsys.readouterr()
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 0


# raise exceptions in underlying GitPython (git import) library and demonstrate catch them

def test_ufodiff_commandline_diff_exception_git_request(capsys):
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        from ufodiff.app import main
        sys.argv = ['ufodiff', 'diff', 'bogus']
        main()

    out, err = capsys.readouterr()
    assert err.startswith("[ufodiff] ERROR: ")
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 1


def test_ufodiff_commandline_diffnc_exception_git_request(capsys):
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        from ufodiff.app import main
        sys.argv = ['ufodiff', 'diffnc', 'bogus']
        main()

    out, err = capsys.readouterr()
    assert err.startswith("[ufodiff] ERROR: ")
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 1


# raise exception in git root path handling
def test_ufodiff_commandline_git_repo_root_exception(capsys):
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        with mock.patch('os.path.join') as opj:
            opj.side_effect = OSError()  # mock an exception from os.path.join inside the function
            get_git_root_path()

    out, err = capsys.readouterr()
    assert err.startswith("[ufodiff] ERROR:")
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 1


