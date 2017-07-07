#!/usr/bin/env python
# -*- coding: utf-8 -*-

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

