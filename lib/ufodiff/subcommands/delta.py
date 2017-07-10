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
    def __init__(self, gitrepo_path, ufo_directory_list, commit_number):
        self.gitrepo_path = gitrepo_path               # path to root of git repository
        self.ufo_directory_list = ufo_directory_list   # used to filter results by user defined UFO source directory
        self.commit_number = commit_number             # user defined number of commits in git history to compare
        self.ufo = Ufo()                               # Ufo class used for UFO source validations
        self.delta_fp_dict = DeltaFilepathDict(ufo_directory_list)  # stores GitPython diffobj.a_rawpath values

        self.commit_sha1_list = []
        self.all_ufo_diffobj_list = []
        self.added_ufo_diffobj_list = []
        self.modified_ufo_diffobj_list = []
        self.deleted_ufo_diffobj_list = []
        # self.renamed_diffobj_list = []

        # filters files for UFO spec and includes only diff files that are part of spec
        self._define_and_validate_ufo_diff_lists()

    # PRIVATE METHODS
    def _define_and_validate_ufo_diff_lists(self):
        commit_number_string = "HEAD~" + self.commit_number
        repo = Repo(self.gitrepo_path)
        git = repo.git
        hcommit = repo.head.commit

        # add file changes to the class attribute lists
        for diff_file in hcommit.diff(commit_number_string):  # TODO: add support for branch v branch comparisons
            self.all_ufo_diffobj_list.append(diff_file)
            self._validate_ufo_and_load_lists(diff_file)

        # add commit SHA1 values to class attribute lists
        self._add_commit_sha1_to_lists(git)

    def _add_commit_sha1_to_lists(self, git):
        # add the commit SHA1 shortcodes for commits requested by user to the class property list
        sha1_num_commits = "-" + self.commit_number
        sha1_args = [sha1_num_commits, '--pretty=%h']
        sha1_string = git.log(sha1_args)   # git log -[N] --pretty=%h  ===> newline delimited list of SHA1 for N commits
        self.commit_sha1_list = sha1_string.split("\n")  # do not modify to os.linesep, Win fails tests with this change

    def _validate_ufo_and_load_lists(self, diff_file):
        # test for valid UFO files and add the diff object from gitpython (git import) to the list
        if diff_file.new_file is True and self.ufo.validate_file(diff_file.a_rawpath) is True:      # added files
            self.added_ufo_diffobj_list.append(diff_file)
        if diff_file.change_type == "M" and self.ufo.validate_file(diff_file.a_rawpath) is True:    # modified files
            self.modified_ufo_diffobj_list.append(diff_file)
        if diff_file.deleted_file is True and self.ufo.validate_file(diff_file.a_rawpath) is True:  # deleted files
            self.deleted_ufo_diffobj_list.append(diff_file)
            # if diff_file.renamed is True:
            #     self.renamed_diffobj_list.append(diff_file)

    # PUBLIC METHODS
    def get_all_ufo_delta_fp_dict(self):
        self.delta_fp_dict.add_commit_sha1(self.commit_sha1_list)
        self.delta_fp_dict.add_added_filepaths(self.added_ufo_diffobj_list)
        self.delta_fp_dict.add_modified_filepaths(self.modified_ufo_diffobj_list)
        self.delta_fp_dict.add_deleted_filepaths(self.deleted_ufo_diffobj_list)
        return self.delta_fp_dict

    # TODO: implement glyph only data
    # def get_glyph_delta_fp_dict(self):
    #     pass

    # TODO: implement nonglyph only data
    # def get_nonglyph_delta_fp_dict(self):
    #     pass


class DeltaFilepathDict(object):
    def __init__(self, ufo_directory_list):
        self.delta_dict = {}
        self.ufo_directory_list = ufo_directory_list

    def _filter_and_load_lists(self, diffobj_list):
        the_filepath_list = []
        if len(self.ufo_directory_list) == 0:  # no user defined UFO source filters, include all UFO source
            for a_diffobj in diffobj_list:
                the_filepath_list.append(a_diffobj.a_rawpath)
        else:
            for a_diffobj in diffobj_list:
                for ufo_directory_filter_path in self.ufo_directory_list:  # filter for user defined UFO source
                    if ufo_directory_filter_path in a_diffobj.a_rawpath:
                        the_filepath_list.append(a_diffobj.a_rawpath)

        return the_filepath_list

    def add_added_filepaths(self, diffobj_list):

        self.delta_dict['added'] = self._filter_and_load_lists(diffobj_list)

    def add_modified_filepaths(self, diffobj_list):

        self.delta_dict['modified'] = self._filter_and_load_lists(diffobj_list)

    def add_deleted_filepaths(self, diffobj_list):

        self.delta_dict['deleted'] = self._filter_and_load_lists(diffobj_list)

    def add_commit_sha1(self, sha1_list):
        self.delta_dict['commits'] = sha1_list


def get_delta_string(delta_fp_dict_obj, write_format):
    """
    Generates standard output text strings, JSON strings, and Markdown formatted strings for delta / deltajson / deltamd
    commands
    :param delta_fp_dict_obj: dictionary of GitPython diff objects as DeltaFilepathDict object class property .delta_dict
    :param write_format: 'text', 'json', or 'markdown', defines delta, deltajson, and deltamd subcommand string generated
    :return: string
    """
    if write_format == 'text':
        textstring = ""

        delta_fp_dict = delta_fp_dict_obj.delta_dict

        # Write SHA1 commits under examination
        if len(delta_fp_dict['commits']) > 0:
            textstring += os.linesep + "Commit history SHA1 for this analysis:" + os.linesep
            for sha1_commit in delta_fp_dict['commits']:
                textstring += " " + sha1_commit + os.linesep
            textstring += os.linesep

        if len(delta_fp_dict['added']) > 0:
            for added_file in delta_fp_dict['added']:
                add_append_string = "[A]:" + added_file + os.linesep
                textstring += add_append_string

        if len(delta_fp_dict['deleted']) > 0:
            for deleted_file in delta_fp_dict['deleted']:
                del_append_string = "[D]:" + deleted_file + os.linesep
                textstring += del_append_string

        if len(delta_fp_dict['modified']) > 0:
            for modified_file in delta_fp_dict['modified']:
                mod_append_string = "[M]:" + modified_file + os.linesep
                textstring += mod_append_string
        # return the text string
        return textstring
    elif write_format == 'json':
        return json.dumps(delta_fp_dict_obj.delta_dict)
    elif write_format == "markdown":
        markdown_string = ""

        delta_fp_dict = delta_fp_dict_obj.delta_dict

        # SHA1 shortcode for included commits block
        if len(delta_fp_dict['commits']) > 0:
            markdown_string += "## Commit history SHA1 for this analysis:" + os.linesep
            for sha1_commit in delta_fp_dict['commits']:
                markdown_string += "- `" + sha1_commit + "`" + os.linesep
            markdown_string += os.linesep

        # Added files block
        markdown_string += "## Added Files" + os.linesep

        if len(delta_fp_dict['added']) > 0:
            for added_file in delta_fp_dict['added']:
                markdown_string += "- " + added_file + os.linesep
        else:
            markdown_string += "- None" + os.linesep

        # Deleted files block
        markdown_string += os.linesep + os.linesep + "## Deleted Files" + os.linesep
        if len(delta_fp_dict['deleted']) > 0:
            for deleted_file in delta_fp_dict['deleted']:
                markdown_string += "- " + deleted_file + os.linesep
        else:
            markdown_string += "- None" + os.linesep

        # Modified files block
        markdown_string += os.linesep + os.linesep + "## Modified Files" + os.linesep
        if len(delta_fp_dict['modified']) > 0:
            for modified_file in delta_fp_dict['modified']:
                markdown_string += "- " + modified_file + os.linesep
        else:
            markdown_string += "- None" + os.linesep

        markdown_string += os.linesep + os.linesep + '---' + os.linesep + "[ufodiff](https://github.com/source-foundry/ufodiff) v" + major_version + "." + minor_version + "." + patch_version
        markdown_string += " | [Report Issue](https://github.com/source-foundry/ufodiff/issues)"
        return markdown_string


