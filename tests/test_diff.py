#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import pytest
import types

from git import Repo

from ufodiff.subcommands.diff import Diff

test_dirty_diff_string_commits_nocolor = """diff --git a/README.md b/README.md
index c13403487..8e84d1d01
--- a/source/ufo/vfb2ufo/Hack-Regular-PS.ufo/fontinfo.plist
+++ b/source/ufo/vfb2ufo/Hack-Regular-PS.ufo/fontinfo.plist
@@ -7,7 +7,7 @@
   <key>capHeight</key>
   <integer>1493</integer>
   <key>copyright</key>
-  <string>Copyright (c) 2015 Christopher Simpkins / Copyright (c) 2003 by Bitstream, Inc. All Rights Reserved.</string>
+  <string>Copyright (c) 2017 Christopher Simpkins / Copyright (c) 2003 by Bitstream, Inc. All Rights Reserved.</string>
   <key>descender</key>
   <integer>-492</integer>
   <key>familyName</key>"""

test_dirty_diff_string_commits_color = """\x1b[1mdiff --git a/README.md b/README.md^[[m
\x1b[1mindex 47e8ec3d2..f5436222b 100644^[[m
^[[1m--- a/README.md^[[m
^[[1m+++ b/README.md^[[m
^[[36m@@ -1,6 +1,6 @@^[[m
 ^[[m
 # Hack^[[m
^[[31m-### A typeface designed for source code^[[m
^[[32m+^[[m^[[32m### A typeface designed for source code-test^[[m
 ^[[m
 <a href="https://sourcefoundry.org/hack/"><img src="img/hack-specimen-2.png" a$
 <br>^[[m
^[[1mdiff --git a/source/ufo/vfb2ufo/Hack-Regular-PS.ufo/fontinfo.plist b/sourc$
^[[1mindex c13403487..8e84d1d01 100644^[[m
^[[1m--- a/source/ufo/vfb2ufo/Hack-Regular-PS.ufo/fontinfo.plist^[[m
^[[1m+++ b/source/ufo/vfb2ufo/Hack-Regular-PS.ufo/fontinfo.plist^[[m
^[[36m@@ -7,7 +7,7 @@^[[m
   <key>capHeight</key>^[[m
   <integer>1493</integer>^[[m
   <key>copyright</key>^[[m
^[[31m-  <string>Copyright (c) 2015 Christopher Simpkins / Copyright (c) 2003 b$
^[[32m+^[[m^[[32m  <string>Copyright (c) 2017 Christopher Simpkins / Copyright $
   <key>descender</key>^[[m
   <integer>-492</integer>^[[m
   <key>familyName</key>^[[m"""


# creates a temporary new git branch (testing_branch) for testing
def make_testing_branch():
    repo = Repo(".")
    gitobj = repo.git
    # create 'test' branch if it doesn't exist so that it can be used for tests in this module
    git_branch_string = gitobj.branch()
    git_branch_list = git_branch_string.split("\n")
    clean_branch_list = []
    for branch in git_branch_list:
        branch = branch.replace("*", "")
        branch = branch.replace(" ", "")
        clean_branch_list.append(branch)
    if "testing_branch" in clean_branch_list:
        pass
    else:
        gitobj.branch("testing_branch")


# deletes the temporary new git branch (testing_branch) for testing
def delete_testing_branch():
    repo = Repo(".")
    gitobj = repo.git
    # create 'test' branch if it doesn't exist so that it can be used for tests in this module
    git_branch_string = gitobj.branch()
    git_branch_list = git_branch_string.split("\n")
    clean_branch_list = []
    for branch in git_branch_list:
        branch = branch.replace("*", "")
        branch = branch.replace(" ", "")
        clean_branch_list.append(branch)
    if "testing_branch" in clean_branch_list:
        gitobj.branch("-d", "testing_branch")


# ///////////////////////////////////////////////////////
#
#  Diff class tests
#
# ///////////////////////////////////////////////////////


def test_ufodiff_diff_class_instantiation_default():
    diff = Diff(".")
    assert diff.is_color_diff is False
    assert diff.gitrepo_path == "."


def test_ufodiff_diff_class_instantation_color_true():
    diff = Diff(".", color_diff=True)
    assert diff.is_color_diff is True
    assert diff.gitrepo_path == "."


def test_ufodiff_diff_clean_diff_string_method_uncolored_string():
    diff = Diff(".")
    cleaned_string = diff._clean_diff_string(test_dirty_diff_string_commits_nocolor)
    assert cleaned_string.startswith("diff --git") is False
    assert cleaned_string.startswith("index c13403487") is True


def test_ufodiff_diff_clean_diff_string_method_colored_string():
    diff = Diff(".")
    cleaned_string = diff._clean_diff_string(test_dirty_diff_string_commits_color)
    assert cleaned_string.startswith("\x1b[1mdiff") is False
    assert cleaned_string.startswith("\x1b[1mindex 47e8ec3d2") is True


def test_ufodiff_diff_get_diff_string_generator_method_uncolored_commits():
    diffobj = Diff(".")
    test_generator = diffobj.get_diff_string_generator("commits:1")
    for thing in test_generator:
        pass
    assert isinstance(test_generator, types.GeneratorType)


def test_ufodiff_diff_get_diff_string_generator_method_colored_commits():
    diffobj = Diff(".", color_diff=True)
    test_generator = diffobj.get_diff_string_generator("commits:1")
    for thing in test_generator:
        pass
    assert isinstance(test_generator, types.GeneratorType)


def test_ufodiff_diff_get_diff_string_generator_method_uncolored_branch():
    make_testing_branch()

    diffobj = Diff(".")
    test_generator = diffobj.get_diff_string_generator("branch:testing_branch")
    for thing in test_generator:
        pass
    assert isinstance(test_generator, types.GeneratorType)

    delete_testing_branch()


def test_ufodiff_diff_get_diff_string_generator_method_colored_branch():
    make_testing_branch()

    diffobj = Diff(".", color_diff=True)
    test_generator = diffobj.get_diff_string_generator("branch:testing_branch")
    for thing in test_generator:
        pass
    assert isinstance(test_generator, types.GeneratorType)

    delete_testing_branch()


def test_ufodiff_diff_get_diff_string_generator_method_uncolored_gitidiom():
    diffobj = Diff(".")
    test_generator = diffobj.get_diff_string_generator("HEAD~1")
    for thing in test_generator:
        pass
    assert isinstance(test_generator, types.GeneratorType)


def test_ufodiff_diff_get_diff_string_generator_method_colored_gitidiom():
    diffobj = Diff(".", color_diff=True)
    test_generator = diffobj.get_diff_string_generator("HEAD~1")
    for thing in test_generator:
        pass
    assert isinstance(test_generator, types.GeneratorType)
