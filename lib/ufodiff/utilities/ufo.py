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
        if os.path.basename(filepath) in self.acceptable_files or filepath.endswith(".glif"):
            return True
        else:
            return False

    def is_nonglyph_file(self, filepath):
        if filepath.endswith('.plist') or filepath.endswith('.fea'):
            return True
        else:
            return False

    def is_glyph_file(self, filepath):
        if filepath.endswith('.glif'):
            return True
        else:
            return False

    def is_ufo_version_file(self, filepath):
        if os.path.basename(filepath) == "metainfo.plist":
            return True
        else:
            return False
