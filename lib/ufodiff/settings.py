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
minor_version = "5"
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

ufodiff is a UFO source file text diff and file modification reporting tool for collaborative typeface development.

Subcommands:

- delta         --- UFO source file add/del/mod report as plain text
   - all
- deltajson     --- UFO source file add/del/mod report as JSON
   - all
- deltamd       --- UFO source file add/del/mod report as Markdown
   - all
- diff          --- colored text diff of UFO spec files (only)
- diffnc        --- uncolored text diff of UFO spec files (only)
  
Syntax:
  ufodiff delta all [commits:[N] | branch:[name]] <optional UFO filter>
  ufodiff deltajson all [commits:[N] | branch:[name]] <optional UFO filter>
  ufodiff deltamd all [commits:[N] | branch:[name]] <optional UFO filter>
  ufodiff diff [commits:[N] | branch:[name]]
  ufodiff diffnc [commits:[N] | branch:[name]]
  
Increase or decrease integer value after the `commits:` argument to analyze across that number of commits in the commit history.

Include an existing git branch for comparison with your current branch after the `branch:` argument.
"""

# ------------------------------------------------------------------------------
# Usage String
# ------------------------------------------------------------------------------

USAGE = "ufodiff [subcommand] [subcommand arguments]"

# ------------------------------------------------------------------------------
# Version String
# ------------------------------------------------------------------------------

VERSION = "ufodiff v" + major_version + "." + minor_version + "." + patch_version
