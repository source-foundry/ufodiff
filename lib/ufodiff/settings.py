#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ====================================================
# Copyright 2017 Christopher Simpkins
# MIT License
# ====================================================

# ------------------------------------------------------------------------------
# Library Name
# ------------------------------------------------------------------------------
lib_name = 'ufodiff'

# ------------------------------------------------------------------------------
# Version Number
# ------------------------------------------------------------------------------
major_version = "0"
minor_version = "2"
patch_version = "4"

# ------------------------------------------------------------------------------
# Help String
# ------------------------------------------------------------------------------

HELP = """====================================================
ufodiff
Copyright 2017 Christopher Simpkins
MIT License
Source: https://github.com/source-foundry/ufodiff
====================================================

ufodiff is a source file diff tool for typefaces developed with UFO source.

Subcommands:

- delta         --- text output to standard output stream
   - all
- deltajson     --- json output to standard output stream
   - all
- deltamd       --- Markdown output to standard output stream
   - all
  
Examples:
  ufodiff delta all commits:3 <optional UFO filter>
  ufodiff deltajson all commits:3 <optional UFO filter>
  ufodiff deltamd all commits:3 <optional UFO filter>
  
Increase or decrease integer value after the `commit:` argument to modify evaluation to that number of previous commits in the git repository.

"""

# ------------------------------------------------------------------------------
# Usage String
# ------------------------------------------------------------------------------

USAGE = "ufodiff [subcommand] [subcommand specific arguments]"

# ------------------------------------------------------------------------------
# Version String
# ------------------------------------------------------------------------------

VERSION = "ufodiff v" + major_version + "." + minor_version + "." + patch_version
