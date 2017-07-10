#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ====================================================
# Copyright 2017 Christopher Simpkins
# MIT License
# ====================================================

import os


class Ufo(object):
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

    # TODO: include information in images and data directories of UFO 3 spec
    def validate_file(self, filepath):
        if os.path.basename(filepath) in self.acceptable_files or filepath[-5:] == ".glif":
            return True
        else:
            return False

    def get_valid_file_filterlist_for_diff(self):
        filter_list = []
        # add valid non-glyph file filters
        for a_file in self.acceptable_files:
            filter_string = "*" + a_file
            filter_list.append(filter_string)
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
