#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ====================================================
# Copyright 2017 Christopher Simpkins
# MIT License
# ====================================================

import os
import sys

from git import Repo
from ufodiff.utilities.ufo import Ufo


class Diff(object):
    """
    Diff class performs git diff on repository with filters for the UFO specification, cleans diff reports for
    improved readability and prepends branch names to the report for branch vs. branch analyses.  Supports git diff
    reports with ANSI color codes and without ANSI color codes.

    :param gitrepo_path: (string) path to root of git repository
    :param color_diff: (boolean) indicator for request for color diff (True) or uncolored diff (False)
    """
    def __init__(self, gitrepo_path, color_diff=False):
        self.gitrepo_path = gitrepo_path                                    # root path for git repository
        self.is_color_diff = color_diff                                     # is request for color diff = True
        self.repo = Repo(self.gitrepo_path)                                 # GitPython Repo object
        self.git = self.repo.git                                            # GitPython Repo.git object
        self.ufo = Ufo()                                                    # ufodiff.utilities.ufo.Ufo object
        self.current_branch = self.git.rev_parse('--abbrev-ref', 'HEAD')    # current git branch automatically detected

    # PRIVATE METHODS

    def _clean_diff_string(self, dirty_diff_string):
        """
        'Cleans' the raw git diff string to improve readability and eliminate data that was not felt to be warranted in
        ufodiff text diff reports.

        :param dirty_diff_string: (string) the raw git diff string
        :return: (string) the cleaned git diff string
        """
        dirty_diffstring_list = dirty_diff_string.split('\n')
        clean_diff_string = ""
        for a_string in dirty_diffstring_list:
            if a_string.startswith("\x1b[1mdiff --git") or a_string.startswith("diff --git"):
                clean_a_string = a_string.replace('diff --git', '')
                clean_a_string = clean_a_string.replace(' ', os.linesep)
                clean_diff_string += clean_a_string + os.linesep
            elif '100644' in a_string:
                clean_a_string = a_string.replace('100644', '')
                clean_a_string = clean_a_string.replace('mode', '')
                clean_diff_string += clean_a_string + os.linesep
            else:
                clean_diff_string += a_string + os.linesep
        # remove two lead lines from text diffs (unnecessary duplication of the two files)
        if "---" in clean_diff_string and "+++" in clean_diff_string:
            clean_diff_string_list = clean_diff_string.split(os.linesep)
            purged_head_paths_diff_string_list = clean_diff_string_list[3:]
            clean_diff_string = ""  # reset the diff string to empty string and start again
            for line in purged_head_paths_diff_string_list:
                clean_diff_string += line + os.linesep
        return clean_diff_string

    # PUBLIC METHODS

    def get_diff_string_generator(self, git_user_diff_string):
        """
        Creates a Python generator that returns individual diff reports for filepaths that match UFO spec filters.

        Generator used as the creation of diff string across large numbers of *.glif file changes can take time to
        create.
        :param git_user_diff_string: (string) the string provided as third argument in user command (ufodiff diff [arg3])
        :return: (Python generator of strings) iterable list of diff text strings intended for standard output
        """
        ufo_file_list = self.ufo.get_valid_file_filterlist_for_diff()  # valid UFO files
        is_branch_test = False   # default is a test between commits, not a test between branches, modified below

        if git_user_diff_string.startswith("commits:"):
            commits_list = git_user_diff_string.split(":")
            commits_number = commits_list[1]
            diff_arg_string = "HEAD~" + commits_number
        elif git_user_diff_string.startswith("branch:"):
            is_branch_test = True
            diff_arg_string = git_user_diff_string[7:] + ".." + self.current_branch
        else:
            diff_arg_string = git_user_diff_string

        if self.is_color_diff is True:
            for ufo_file in ufo_file_list:
                dirty_diff_string = self.git.diff(diff_arg_string, '--minimal', '--color', '--', ufo_file)
                cleaned_diff_string = self._clean_diff_string(dirty_diff_string)
                if len(cleaned_diff_string) > 1:  # eliminates diff filters that did not include identified files
                    if is_branch_test is True:
                        cleaned_diff_string = "branch " + diff_arg_string + os.linesep + cleaned_diff_string
                    yield cleaned_diff_string
        else:
            for ufo_file in ufo_file_list:
                dirty_diff_string = self.git.diff(diff_arg_string, '--minimal', '--', ufo_file)
                cleaned_diff_string = self._clean_diff_string(dirty_diff_string)
                if len(cleaned_diff_string) > 1:  # eliminates diff filters that did not include identified files
                    if is_branch_test is True:  # add branch descriptions to the output from the diff
                        cleaned_diff_string = "branch " + diff_arg_string + os.linesep + cleaned_diff_string
                    yield cleaned_diff_string
