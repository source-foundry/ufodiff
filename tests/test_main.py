#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import pytest

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
    with pytest.raises(SystemExit):
        from ufodiff.app import main
        sys.argv = ['ufodiff', '-h']
        main()

    out, err = capsys.readouterr()
    assert out.startswith("====================================================") is True


def test_ufodiff_commandline_longhelp(capsys):
    with pytest.raises(SystemExit):
        from ufodiff.app import main
        sys.argv = ['ufodiff', '--help']
        main()

    out, err = capsys.readouterr()
    assert out.startswith("====================================================") is True


def test_ufodiff_commandline_shortversion(capsys):
    with pytest.raises(SystemExit):
        from ufodiff.app import main
        from ufodiff.app import settings
        sys.argv = ['ufodiff', '-v']
        main()

    out, err = capsys.readouterr()
    assert out.startswith(settings.VERSION)


def test_ufodiff_commandline_longversion(capsys):
    with pytest.raises(SystemExit):
        from ufodiff.app import main
        from ufodiff.app import settings
        sys.argv = ['ufodiff', '--version']
        main()

    out, err = capsys.readouterr()
    assert out.startswith(settings.VERSION)


def test_ufodiff_commandline_longusage(capsys):
    with pytest.raises(SystemExit):
        from ufodiff.app import main
        from ufodiff.app import settings
        sys.argv = ['ufodiff', '--usage']
        main()

    out, err = capsys.readouterr()
    assert out.startswith(settings.USAGE)


# ///////////////////////////////////////////////////////
#
# Standard output tests for argument validations
#
# ///////////////////////////////////////////////////////


def test_ufodiff_commandline_missingargs(capsys):
    with pytest.raises(SystemExit):
        from ufodiff.app import main
        sys.argv = ['ufodiff']
        main()

    out, err = capsys.readouterr()
    assert err.startswith("[ufodiff] ERROR: Please include the appropriate arguments with your command.")


def test_ufodiff_commandline_delta_missingargs(capsys):
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        from ufodiff.app import main
        sys.argv = ['ufodiff', 'delta']
        main()

    out, err = capsys.readouterr()
    assert err.startswith("[ufodiff] ERROR: Too few arguments to the ufodiff delta command.")
    assert pytest_wrapped_e.value.code == 1


def test_ufodiff_commandline_delta_unacceptable_subsub(capsys):
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        from ufodiff.app import main
        sys.argv = ['ufodiff', 'delta', 'bogus', 'commits:1']
        main()

    out, err = capsys.readouterr()
    assert err.startswith("[ufodiff] ERROR:")
    assert pytest_wrapped_e.value.code == 1


def test_ufodiff_commandline_delta_missing_commits_arg(capsys):
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        from ufodiff.app import main
        sys.argv = ['ufodiff', 'delta', 'all', 'bogus']
        main()

    out, err = capsys.readouterr()
    assert err.startswith("[ufodiff] ERROR:")
    assert pytest_wrapped_e.value.code == 1


def test_ufodiff_commandline_delta_missing_commits_number(capsys):
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        from ufodiff.app import main
        sys.argv = ['ufodiff', 'delta', 'all', 'commits:']
        main()

    out, err = capsys.readouterr()
    assert err.startswith("[ufodiff] ERROR:")
    assert pytest_wrapped_e.value.code == 1


def test_ufodiff_commandline_delta_commits_number_notdigit(capsys):
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        from ufodiff.app import main
        sys.argv = ['ufodiff', 'delta', 'all', 'commits:a']
        main()

    out, err = capsys.readouterr()
    assert err.startswith("[ufodiff] ERROR:")
    assert pytest_wrapped_e.value.code == 1


def test_ufodiff_commandline_delta_commits_number_with_ufo_filter(capsys):
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        from ufodiff.app import main
        sys.argv = ['ufodiff', 'delta', 'all', 'commits:1', 'Test-Regular.ufo']
        main()

    out, err = capsys.readouterr()
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
    assert pytest_wrapped_e.value.code == 1


def test_ufodiff_commandline_delta_commits_number_is_zero(capsys):
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        from ufodiff.app import main
        sys.argv = ['ufodiff', 'delta', 'all', 'commits:0']
        main()

    out, err = capsys.readouterr()
    assert err.startswith("[ufodiff] ERROR:")
    assert pytest_wrapped_e.value.code == 1


def test_ufodiff_commandline_delta_commits_number_is_lessthan_zero(capsys):
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        from ufodiff.app import main
        sys.argv = ['ufodiff', 'delta', 'all', 'commits:-1']
        main()

    out, err = capsys.readouterr()
    assert err.startswith("[ufodiff] ERROR:")
    assert pytest_wrapped_e.value.code == 1


def test_ufodiff_commandline_deltajson_exit_success(capsys):
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        from ufodiff.app import main
        sys.argv = ['ufodiff', 'deltajson', 'all', 'commits:2']
        main()

    out, err = capsys.readouterr()
    assert pytest_wrapped_e.value.code == 0


def test_ufodiff_commandline_deltamd_exit_success(capsys):
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        from ufodiff.app import main
        sys.argv = ['ufodiff', 'deltamd', 'all', 'commits:2']
        main()

    out, err = capsys.readouterr()
    assert pytest_wrapped_e.value.code == 0

# Test for exit code in pytest:

# with pytest.raises(SystemExit) as pytest_wrapped_e:
#     somefunction()
# assert pytest_wrapped_e.type == SystemExit
# assert pytest_wrapped_e.value.code == 0