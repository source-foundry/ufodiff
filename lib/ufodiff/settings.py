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
minor_version = "3"
patch_version = "0"

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

- delta         --- UFO source file add/del/mod as plain text
   - all
- deltajson     --- UFO source file add/del/mod as JSON
   - all
- deltamd       --- UFO source file add/del/mod as Markdown
   - all
- diff          --- colored text diff of UFO spec files (only)
- diffnc        --- uncolored text diff of UFO spec files (only)
  
Examples:
  ufodiff delta all commits:3 <optional UFO filter>
  ufodiff deltajson all commits:3 <optional UFO filter>
  ufodiff deltamd all commits:3 <optional UFO filter>
  ufodiff diff commits:3
  ufodiff diff branch:development
  ufodiff diff master..development
  ufodiff diff HEAD~3
  
Increase or decrease integer value after the `commits:` argument to modify evaluation to that number of previous commits in the git repository.

Specify the branch for comparison with your current branch after the `branch:` argument in the diff subcommands.
"""

# ------------------------------------------------------------------------------
# Usage String
# ------------------------------------------------------------------------------

USAGE = "ufodiff [subcommand] [subcommand specific arguments]"

# ------------------------------------------------------------------------------
# Version String
# ------------------------------------------------------------------------------

VERSION = "ufodiff v" + major_version + "." + minor_version + "." + patch_version
