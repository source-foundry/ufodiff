#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ====================================================
# Copyright 2017 Christopher Simpkins
# MIT License
# ====================================================

"""
The app.py module defines a main() function that includes the logic for the `ufodiff` command line executable.

This command line executable performs diff comparisons of UFO source files that are used in typeface development.
"""

import os
import sys
from commandlines import Command
from standardstreams import stdout, stderr

from ufodiff import settings  # defines application version, help string, version string, usage string
from ufodiff.subcommands.delta import Delta, get_delta_string

from ufodiff.utilities import dir_exists


def main():
    """Defines the logic for the `ufodiff` command line executable"""
    c = Command()

    if c.does_not_validate_missing_args():
        stderr("[ufodiff] ERROR: Please include the appropriate arguments with your command.")
        sys.exit(1)

    if c.is_help_request():
        stdout(settings.HELP)
        sys.exit(0)
    elif c.is_version_request():
        stdout(settings.VERSION)
        sys.exit(0)
    elif c.is_usage_request():
        stdout(settings.USAGE)
        sys.exit(0)

    # DELTA + DELTAJSON + DELTAMD sub-commands
    #  ufodiff [delta|deltajson|deltamd] [all|glyph|nonglyph] [commits:number] <UFO file path>
    acceptable_delta_ufodiff_subcmd_list = ['delta', 'deltajson', 'deltamd']
    if c.subcmd in acceptable_delta_ufodiff_subcmd_list:
        acceptable_deltacommands = ['all', 'glyph', 'nonglyph']  # used in command line argument validations

        # Command line argument validations
        # TODO: add test that commits integer requested by user is < number of total commits in the repository
        if c.argc < 3:  # expected argument number
            stderr("[ufodiff] ERROR: Too few arguments to the ufodiff delta command.")
            sys.exit(1)
        elif c.arg1 not in acceptable_deltacommands:  # acceptable sub command to delta
            stderr("[ufodiff] ERROR: 'ufodiff " + c.arg0 + " " + c.arg1 + "' is not a valid request")
            stderr("Acceptable arguments to " + c.arg0 + " include:")
            for acceptable_deltacommand in acceptable_deltacommands:
                stderr(" " + acceptable_deltacommand)
            sys.exit(1)
        elif not c.arg2.startswith("commits:"):  # did not include commits argument
            stderr("[ufodiff] ERROR: Please include the 'commits:[number]' argument immediately after '" + c.arg1 + "'")
            sys.exit(1)
        elif len(c.arg2) < 9:  # did not include an integer with the commits argument
            stderr("[ufodiff] ERROR: Please include an integer after the colon in the 'commits:[number]' argument")
            sys.exit(1)

        # Variable definitions
        ufo_directory_list = []  # used to filter the UFO directories for delta reports
        for arg in c.argv:
            if arg.endswith('.ufo'):
                ufo_directory_list.append(arg)
        commits_list = c.arg2.split(':')
        commits_number = commits_list[1]

        # define root of git repository
        unverified_gitroot_path = os.path.abspath('.')

        # define Git repository root path in variable
        # check working directory for git repository root
        if dir_exists(os.path.join(unverified_gitroot_path, '.git')):
            verified_gitroot_path = os.path.join(unverified_gitroot_path, '.git')
        else:
            # recursive search for the root of the git repository x 3 levels if not found in working directory
            try:
                one_level_up = os.path.abspath(os.path.join(unverified_gitroot_path, os.pardir))
                two_levels_up = os.path.dirname(one_level_up)
                three_levels_up = os.path.dirname(two_levels_up)

                one_level_up_path = os.path.join(one_level_up, '.git')
                two_levels_up_path = os.path.join(two_levels_up, '.git')
                three_levels_up_path = os.path.join(three_levels_up, '.git')

                if dir_exists(one_level_up_path):  # check one directory level up
                    verified_gitroot_path = os.path.dirname(one_level_up_path)
                elif dir_exists(two_levels_up_path):  # check two directory levels up
                    verified_gitroot_path = os.path.dirname(two_levels_up_path)
                elif dir_exists(three_levels_up_path):  # check three directory levels up
                    verified_gitroot_path = os.path.dirname(three_levels_up_path)
                else:
                    stderr("[ufodiff] ERROR: Unable to identify the root of your git repository. Please try again from "
                           "the root of your repository")
                    sys.exit(1)
            except Exception as e:
                stderr("[ufodiff] ERROR: Unable to identify the root of your git repository. Please try again from "
                       "the root of your repository")
                stderr(" ")
                stderr(e)  # display exception if exception raised with this attempt to define path
                sys.exit(1)

        # Variable validations
        if not commits_number.isdigit():  # validate that user entered number of commits for diff is an integer
            stderr("[ufodiff] ERROR: The value following the colon in the 'commits:[number]' argument is not a valid "
                   "integer value")
            sys.exit(1)
        elif int(commits_number) == 0 or int(commits_number) < 0:   # validate that the number of commits is > 0
            stderr("[ufodiff] ERROR: Please define a value over zero for the number of previous commits to diff")
            sys.exit(1)

        # perform the delta analysis on the repository
        delta = Delta(verified_gitroot_path, ufo_directory_list, commits_number)

        # handle subcommand + subsubcommand combinations
        if c.arg1 == "all":
            filepath_dict = delta.get_all_ufo_delta_fp_dict()
            if c.subcmd == "delta":
                stdout_string = get_delta_string(filepath_dict, write_format='text')
            elif c.subcmd == "deltajson":
                stdout_string = get_delta_string(filepath_dict, write_format='json')
            elif c.subcmd == "deltamd":
                stdout_string = get_delta_string(filepath_dict, write_format='markdown')
            sys.stdout.write(stdout_string)
        elif c.arg1 == "glyph":
            pass  # TODO: implement glyph only command handling with 'ufo delta glyph'
        elif c.arg1 == "nonglyph":
            pass  # TODO: implement nonglyph only command handling with 'ufo delta nonglyph'


if __name__ == '__main__':
    main()
