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


class Delta(object):
    def __init__(self, gitrepo_path, ufo_directory_list, commit_number):
        self.gitrepo_path = gitrepo_path
        self.ufo_directory_list = ufo_directory_list   # used to filter results by user defined UFO source directory
        self.commit_number = commit_number
        self.ufo = Ufo()
        self.delta_fp_dict = DeltaFilepathDict(ufo_directory_list)

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
        hcommit = repo.head.commit
        for diff_file in hcommit.diff(commit_number_string):
            self.all_ufo_diffobj_list.append(diff_file)

            # test for valid UFO files and add the diff object from gitpython (git import) to the list
            if diff_file.new_file is True and self.ufo.validate_file(diff_file.a_rawpath) is True:
                self.added_ufo_diffobj_list.append(diff_file)
            if diff_file.change_type == "M" and self.ufo.validate_file(diff_file.a_rawpath) is True:
                self.modified_ufo_diffobj_list.append(diff_file)
            if diff_file.deleted_file is True and self.ufo.validate_file(diff_file.a_rawpath) is True:
                self.deleted_ufo_diffobj_list.append(diff_file)
            # if diff_file.renamed is True:
            #     self.renamed_diffobj_list.append(diff_file)

    # PUBLIC METHODS
    def get_all_ufo_delta_fp_dict(self):
        self.delta_fp_dict.add_added_filepaths(self.added_ufo_diffobj_list)
        self.delta_fp_dict.add_modified_filepaths(self.modified_ufo_diffobj_list)
        self.delta_fp_dict.add_deleted_filepaths(self.deleted_ufo_diffobj_list)
        return self.delta_fp_dict

    # TODO: implement glyph only data
    def get_glyph_delta_fp_dict(self):
        pass

    # TODO: implement nonglyph only data
    def get_nonglyph_delta_fp_dict(self):
        pass


class DeltaFilepathDict(object):
    def __init__(self, ufo_directory_list):
        self.delta_dict = {}
        self.ufo_directory_list = ufo_directory_list

    def add_added_filepaths(self, diffobj_list):
        added_filepath_list = []

        if len(self.ufo_directory_list) == 0:  # no user defined UFO source filters, include all UFO source
            for a_diffobj in diffobj_list:
                added_filepath_list.append(a_diffobj.a_rawpath)
        else:
            for a_diffobj in diffobj_list:
                for ufo_directory_filter_path in self.ufo_directory_list:  # filter for user defined UFO source
                    if ufo_directory_filter_path in a_diffobj.a_rawpath:
                        added_filepath_list.append(a_diffobj.a_rawpath)

        self.delta_dict['added'] = added_filepath_list

    def add_modified_filepaths(self, diffobj_list):
        modified_filepath_list = []

        if len(self.ufo_directory_list) == 0:  # no user defined UFO source filters, include all UFO source
            for a_diffobj in diffobj_list:
                modified_filepath_list.append(a_diffobj.a_rawpath)
        else:
            for a_diffobj in diffobj_list:
                for ufo_directory_filter_path in self.ufo_directory_list:   # filter for user defined UFO source
                    if ufo_directory_filter_path in a_diffobj.a_rawpath:
                        modified_filepath_list.append(a_diffobj.a_rawpath)

        self.delta_dict['modified'] = modified_filepath_list

    def add_deleted_filepaths(self, diffobj_list):
        deleted_filepath_list = []

        if len(self.ufo_directory_list) == 0:
            for a_diffobj in diffobj_list:
                deleted_filepath_list.append(a_diffobj.a_rawpath)
        else:
            for a_diffobj in diffobj_list:
                for ufo_directory_filter_path in self.ufo_directory_list:
                    if ufo_directory_filter_path in a_diffobj.a_rawpath:
                        deleted_filepath_list.append(a_diffobj.a_rawpath)

        self.delta_dict['deleted'] = deleted_filepath_list


def get_delta_string(delta_fp_dict_obj, commits_number, write_format):
    if write_format == 'text':
        textstring = ""

        delta_fp_dict = delta_fp_dict_obj.delta_dict

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
        pass
