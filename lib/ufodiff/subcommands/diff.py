#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ====================================================
# Copyright 2017 Christopher Simpkins
# MIT License
# ====================================================

import os

from git import Repo
from ufodiff.utilities.ufo import Ufo


class Diff(object):
    def __init__(self, gitrepo_path, color_diff=False):
        self.gitrepo_path = gitrepo_path
        self.is_color_diff = color_diff
        self.repo = Repo(self.gitrepo_path)
        self.git = self.repo.git
        self.ufo = Ufo()
        self.current_branch = self.git.rev_parse('--abbrev-ref', 'HEAD')

    # PRIVATE METHODS

    def _clean_diff_string(self, dirty_diff_string):
        dirty_diffstring_list = dirty_diff_string.split('\n')
        clean_diff_string = ""
        for a_string in dirty_diffstring_list:
            if a_string.startswith("\x1b[1mdiff --git") or a_string.startswith("diff --git"):
                pass
            elif '100644' in a_string:
                clean_a_string = a_string.replace('100644', '')
                clean_diff_string += clean_a_string + os.linesep
            else:
                clean_diff_string += a_string + os.linesep
        return clean_diff_string

    # PUBLIC METHODS

    def get_diff_string_generator(self, git_user_diff_string):
        ufo_file_list = self.ufo.get_valid_file_filterlist_for_diff()  # valid UFO files
        is_branch_test = False   # default is a test between commits, not a test between branches, modified below

        if git_user_diff_string.startswith("commits:"):
            commits_list = git_user_diff_string.split(":")
            commits_number = commits_list[1]
            diff_arg_string = "HEAD~" + commits_number
        elif git_user_diff_string.startswith("branch:"):
            is_branch_test = True
            diff_arg_string = self.current_branch + "..." + git_user_diff_string[7:]
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

    # def get_diff_string_generator_userfilter(self, git_user_diff_list):
    #     pass
