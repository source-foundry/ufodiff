#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ====================================================
# Copyright 2017 Christopher Simpkins
# MIT License
# ====================================================

import os
import json

from git import Repo

from ufodiff.utilities.ufo import Ufo
from ufodiff.settings import major_version, minor_version, patch_version


class Delta(object):
    """
    Delta class stores delta subcommand data and provides methods to support creation of
    delta / deltajson / deltamd reports.  Uses DeltaFilepathDict class to filter diff file list
    by user specified UFO source directory filter and sort by added/deleted/modified status of the files

    :param gitrepo_path: absolute file path to the root level of the git repository for analysis (automatically detected in ufodiff.app.py)
    :param ufo_directory_list: list of one or more UFO directories for filter of results (user specified on CL)
    :param commit_number: the number of requested in the git history to analyze (user specified on CL)
    """
    def __init__(self, gitrepo_path, ufo_directory_list, is_commit_test=False, commit_number="0", is_branch_test=False, compare_branch_name=None):
        self.gitrepo_path = gitrepo_path               # path to root of git repository
        self.ufo_directory_list = ufo_directory_list   # used to filter results by user defined UFO source directory
        self.is_commit_test = is_commit_test
        self.commit_number = commit_number             # user defined number of commits in git history to compare
        self.is_branch_test = is_branch_test
        self.compare_branch_name = compare_branch_name
        self.current_branch_name = ""    # defined in _define_and_validate_ufo_diff_lists if branch test
        self.ufo = Ufo()                               # Ufo class used for UFO source validations
        self.git = None
        self.delta_fp_string_dict = DeltaFilepathStringDict(ufo_directory_list)  # stores delta file strings in .delta_dict attribute

        self.commit_sha1_list = []

        # file string lists
        self.added_ufo_file_list = []
        self.modified_ufo_file_list = []
        self.deleted_ufo_file_list = []

        # filters files for UFO spec and includes only diff files that are part of spec
        self._define_and_validate_ufo_diff_lists()

    # PRIVATE METHODS
    def _define_and_validate_ufo_diff_lists(self):
        # instantiate git Repo object
        repo = Repo(self.gitrepo_path)
        # define class attribute git object
        self.git = repo.git

        if self.is_commit_test is True:
            commit_number_string = "HEAD~" + self.commit_number  # with HEAD~N syntax
            added_file_string = self.git.diff('--name-only', '--diff-filter=A', commit_number_string)
            added_filepath_list = added_file_string.split("\n")
            deleted_file_string = self.git.diff('--name-only', '--diff-filter=D', commit_number_string)
            deleted_filepath_list = deleted_file_string.split("\n")
            modified_file_string = self.git.diff('--name-only', '--diff-filter=M', commit_number_string)
            modified_filepath_list = modified_file_string.split("\n")
        elif self.is_branch_test is True:
            self.current_branch_name = self.git.rev_parse(['--abbrev-ref', 'HEAD'])
            branch_comparison_string = self.compare_branch_name + ".." + self.current_branch_name
            added_file_string = self.git.diff(['--name-only', '--diff-filter=A', branch_comparison_string])
            added_filepath_list = added_file_string.split('\n')
            deleted_file_string = self.git.diff(['--name-only', '--diff-filter=D', branch_comparison_string])
            deleted_filepath_list = deleted_file_string.split('\n')
            modified_file_string = self.git.diff(['--name-only', '--diff-filter=M', branch_comparison_string])
            modified_filepath_list = modified_file_string.split('\n')

        # load class attribute lists with the filepaths that are validated to be UFO in the following method
        self._validate_ufo_and_load_dict_from_filepath_strings(added_filepath_list, deleted_filepath_list, modified_filepath_list)

    def _add_commit_sha1_to_lists(self):
        # add the commit SHA1 shortcodes for commits requested by user to the class property list
        sha1_num_commits = "-" + self.commit_number
        sha1_args = [sha1_num_commits, '--pretty=%h']
        sha1_string = self.git.log(sha1_args)   # git log -[N] --pretty=%h  ===> newline delimited list of SHA1 for N commits
        self.commit_sha1_list = sha1_string.split("\n")  # do not modify to os.linesep, Win fails tests with this change

    def _validate_ufo_and_load_dict_from_filepath_strings(self, added_filepath_list, deleted_filepath_list, modified_filepath_list):
        # test for valid UFO files and add the filepath string to the appropriate class instance attribute
        # load added files list
        if len(added_filepath_list) > 0:
            for added_file in added_filepath_list:
                if self.ufo.validate_file(added_file) is True:
                    self.added_ufo_file_list.append(added_file)

        # load deleted files list
        if len(deleted_filepath_list) > 0:
            for deleted_file in deleted_filepath_list:
                if self.ufo.validate_file(deleted_file) is True:
                    self.deleted_ufo_file_list.append(deleted_file)

        # load modified files list
        if len(modified_filepath_list) > 0:
            for modified_file in modified_filepath_list:
                if self.ufo.validate_file(modified_file) is True:
                    self.modified_ufo_file_list.append(modified_file)

        # define the key:value structure of the dictionary attribute on the DeltaFilepathStringDict() class
        if self.is_commit_test:
            self._add_commit_sha1_to_lists()
            self.delta_fp_string_dict.add_commit_sha1(self.commit_sha1_list)          # create 'commits' dict key
        elif self.is_branch_test:
            branch_list = [self.compare_branch_name, self.current_branch_name]
            self.delta_fp_string_dict.add_branches(branch_list)                        # create 'branches' dict key
        self.delta_fp_string_dict.add_added_filepaths(self.added_ufo_file_list)        # create 'added' dict key
        self.delta_fp_string_dict.add_deleted_filepaths(self.deleted_ufo_file_list)    # create 'deleted' dict key
        self.delta_fp_string_dict.add_modified_filepaths(self.modified_ufo_file_list)  # create 'modified' dict key

    def _get_delta_text_string(self):
        textstring = ""
        if self.is_commit_test is True:                   # include commits if this is an analysis of commit history
            # Write SHA1 commits under examination
            if len(self.delta_fp_string_dict.delta_dict['commits']) > 0:
                textstring += os.linesep + "Commit history SHA1 for this analysis:" + os.linesep
                for sha1_commit in self.delta_fp_string_dict.delta_dict['commits']:
                    textstring += " " + sha1_commit + os.linesep
                textstring += os.linesep
        elif self.is_branch_test is True:                 # include branches if this is a branch v branch analysis
            if len(self.delta_fp_string_dict.delta_dict['branches']) > 0:
                textstring += os.linesep + "Branches under analysis:" + os.linesep
                for branch in self.delta_fp_string_dict.delta_dict['branches']:
                    textstring += " " + branch + os.linesep
                textstring += os.linesep

        # include added files
        if len(self.delta_fp_string_dict.delta_dict['added']) > 0:
            for added_file in self.delta_fp_string_dict.delta_dict['added']:
                add_append_string = "[A]:" + added_file + os.linesep
                textstring += add_append_string
        # include deleted files
        if len(self.delta_fp_string_dict.delta_dict['deleted']) > 0:
            for deleted_file in self.delta_fp_string_dict.delta_dict['deleted']:
                del_append_string = "[D]:" + deleted_file + os.linesep
                textstring += del_append_string
        # include modified files
        if len(self.delta_fp_string_dict.delta_dict['modified']) > 0:
            for modified_file in self.delta_fp_string_dict.delta_dict['modified']:
                mod_append_string = "[M]:" + modified_file + os.linesep
                textstring += mod_append_string

        return textstring

    def _get_delta_json_string(self):
        return json.dumps(self.delta_fp_string_dict.delta_dict)

    def _get_delta_markdown_string(self):
        markdown_string = ""

        if self.is_commit_test is True:
            if len(self.delta_fp_string_dict.delta_dict['commits']) > 0:
                markdown_string += os.linesep + "## Commit history SHA1 for this analysis:" + os.linesep
                for sha1_commit in self.delta_fp_string_dict.delta_dict['commits']:
                    markdown_string += "- `" + sha1_commit + "`" + os.linesep
                markdown_string += os.linesep
        elif self.is_branch_test is True:
            if len(self.delta_fp_string_dict.delta_dict['branches']) > 0:
                markdown_string += os.linesep + "## Branches under analysis:" + os.linesep
                for branch in self.delta_fp_string_dict.delta_dict['branches']:
                    markdown_string += " -" + branch + os.linesep
                markdown_string += os.linesep

        # Added files block
        markdown_string += "## Added Files" + os.linesep
        if len(self.delta_fp_string_dict.delta_dict['added']) > 0:
            for added_file in self.delta_fp_string_dict.delta_dict['added']:
                markdown_string += "- " + added_file + os.linesep
        else:
            markdown_string += "- None" + os.linesep

        # Deleted files block
        markdown_string += os.linesep + os.linesep + "## Deleted Files" + os.linesep
        if len(self.delta_fp_string_dict.delta_dict['deleted']) > 0:
            for deleted_file in self.delta_fp_string_dict.delta_dict['deleted']:
                markdown_string += "- " + deleted_file + os.linesep
        else:
            markdown_string += "- None" + os.linesep

        # Modified files block
        markdown_string += os.linesep + os.linesep + "## Modified Files" + os.linesep
        if len(self.delta_fp_string_dict.delta_dict['modified']) > 0:
            for modified_file in self.delta_fp_string_dict.delta_dict['modified']:
                markdown_string += "- " + modified_file + os.linesep
        else:
            markdown_string += "- None" + os.linesep

        # Project URL + version footer
        markdown_string += os.linesep + os.linesep + '---' + os.linesep + \
                           "[ufodiff](https://github.com/source-foundry/ufodiff) v" + \
                           major_version + "." + minor_version + "." + patch_version

        return markdown_string

    # PUBLIC METHODS

    def get_stdout_string(self, write_format=None):
        if write_format == 'text':
            return self._get_delta_text_string()
        elif write_format == 'json':
            return self._get_delta_json_string()
        elif write_format == 'markdown':
            return self._get_delta_markdown_string()

    # TODO: implement glyph only data
    # def get_stdout_string_glyph_only(self):
    #     pass

    # TODO: implement nonglyph only data
    # def get_stdout_string_nonglyph_only(self):
    #     pass


class DeltaFilepathStringDict(object):
    """
    Object that maintains a Python dictionary of filepaths that meet UFO spec and any user defined UFO path filters
    for use in the generation of standard output strings.

    UFO spec validation occurs here.

    User defined UFO directory path filter occurs here.
    """
    def __init__(self, ufo_directory_list):
        self.delta_dict = {}
        self.ufo_directory_list = ufo_directory_list

    def _filter_and_load_lists(self, filepath_list):
        the_filepath_list = []
        if len(self.ufo_directory_list) == 0:  # no user defined UFO source filters, include all UFO source
            for delta_file in filepath_list:
                the_filepath_list.append(delta_file)
        else:  # user wants the results to be filtered by specific UFO directory(ies)
            for delta_file in filepath_list:
                for ufo_directory_filter_path in self.ufo_directory_list:
                    if ufo_directory_filter_path in delta_file:
                        the_filepath_list.append(delta_file)
        return the_filepath_list

    def add_added_filepaths(self, added_filepath_list):
        self.delta_dict['added'] = self._filter_and_load_lists(added_filepath_list)

    def add_deleted_filepaths(self, deleted_filepath_list):
        self.delta_dict['deleted'] = self._filter_and_load_lists(deleted_filepath_list)

    def add_modified_filepaths(self, modified_filepath_list):
        self.delta_dict['modified'] = self._filter_and_load_lists(modified_filepath_list)

    def add_commit_sha1(self, commit_sha1_list):
        self.delta_dict['commits'] = self._filter_and_load_lists(commit_sha1_list)

    def add_branches(self, branch_name_list):
        self.delta_dict['branches'] = self._filter_and_load_lists(branch_name_list)
