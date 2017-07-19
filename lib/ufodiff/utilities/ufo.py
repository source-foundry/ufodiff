#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ====================================================
# Copyright 2017 Christopher Simpkins
# MIT License
# ====================================================

import os


class Ufo(object):
    """
    Validates filepaths based upon the Unified Font Object source specification
    """
    def __init__(self):
        self.acceptable_files = {
            'metainfo.plist',
            'fontinfo.plist',
            'groups.plist',
            'kerning.plist',
            'features.fea',
            'lib.plist',
            'contents.plist',
            'layercontents.plist',
            'layerinfo.plist'
        }

    def _is_images_directory_file(self, filepath):
        path_list = filepath.split(os.path.sep)
        index = 0
        for path_part in path_list:
            if path_part == "images":
                ufo_test_directory = path_list[index - 1]  # .ufo directory should be one directory level above images
                base_filename = path_list[-1]              # base filename should have .png extension
                if len(base_filename) > 4 and base_filename[-4:] == '.png' and ufo_test_directory[-4:] == '.ufo':
                    return True                            # .png file in *.ufo/images directory = pass
            else:
                index += 1
        return False  # if iterate through entire path and never satisfy above test conditions, test fails

    def _is_data_directory_file(self, filepath):
        path_list = filepath.split(os.path.sep)
        index = 0
        for path_part in path_list:
            if path_part == "data":
                ufo_test_directory = path_list[index - 1]    # .ufo directory should be one level above data
                if ufo_test_directory[-4:] == '.ufo':        # test for presence of *.ufo directory one level up
                    return True                              # any file in *.ufo/data directory = pass
            else:
                index += 1
        return False  # if iterate through entire path and never satisfy above test conditions, test fails

    def validate_file(self, filepath):
        if os.path.basename(filepath) in self.acceptable_files or filepath[-5:] == ".glif":
            return True
        elif self._is_data_directory_file(filepath) is True:    # UFO v3 data directory file test
            return True
        elif self._is_images_directory_file(filepath) is True:  # UFO v3 images directory file test
            return True
        else:
            return False

    def get_valid_file_filterlist_for_diff(self):
        filter_list = []
        # add valid non-glyph file wildcards
        for a_file in self.acceptable_files:
            filter_string = "*" + a_file
            filter_list.append(filter_string)
        # add images directory wildcard (added in UFO v3)
        filter_list.append('*\.ufo/images/*')
        # add data directory wildcard (added in UFO v3)
        filter_list.append('*\.ufo/data/*')
        # add glyph file filters
        filter_list.append('*.glif')
        return filter_list

    def is_nonglyph_file(self, filepath):
        if filepath[-6:] == ".plist" or filepath[-4:] == ".fea":
            return True
        else:
            return False

    def is_glyph_file(self, filepath):
        if filepath[-5:] == ".glif":
            return True
        else:
            return False

    def is_ufo_version_file(self, filepath):
        if os.path.basename(filepath) == "metainfo.plist":
            return True
        else:
            return False

