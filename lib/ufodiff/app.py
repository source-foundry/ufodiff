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
from ufodiff.subcommands.diff import Diff

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
    if c.subcmd in {'delta', 'deltajson', 'deltamd'}:
        # argument validation
        validate_delta_commands_args(c)
        # create list for UFO filtered analyses as requested by user
        ufo_directory_list = []
        for arg in c.argv:
            if arg.endswith('.ufo'):
                ufo_directory_list.append(arg)
        # TODO: add branch: support here (in addition to commits: shortcut)
        commits_list = c.arg2.split(':')
        commits_number = commits_list[1]
        # Commit number integer validation
        validate_commits_number(commits_number)

        # recursive search for the root of the git repository x 3 levels if not found in working directory
        verified_gitroot_path = get_git_root_path()

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
        # elif c.arg1 == "glyph":
        #     pass  # TODO: implement glyph only command handling with 'ufo delta glyph'
        # elif c.arg1 == "nonglyph":
        #     pass  # TODO: implement nonglyph only command handling with 'ufo delta nonglyph'
    # DIFF SUBCOMMAND
    elif c.subcmd == "diff":
        # argument validation
        validate_diff_commands_args(c)
        # execute the command
        try:
            verified_gitroot_path = get_git_root_path()
            diff = Diff(verified_gitroot_path, color_diff=True)
            for diff_string in diff.get_diff_string_generator(c.arg1):
                stdout(diff_string)
        except Exception as e:
            stderr("[ufodiff] ERROR: Unable to excecute your request. Error returned as: " + os.linesep + str(e))
            sys.exit(1)
    # DIFFNC SUBCOMMAND
    elif c.subcmd == "diffnc":
        # argument validations
        validate_diff_commands_args(c)
        # execute the command
        try:
            verified_gitroot_path = get_git_root_path()
            diff = Diff(verified_gitroot_path, color_diff=False)
            for diff_string in diff.get_diff_string_generator(c.arg1):
                stdout(diff_string)
        except Exception as e:
            stderr("[ufodiff] ERROR: Unable to excecute your request. Error returned as: " + os.linesep + str(e))
            sys.exit(1)
    # # DIFF-FILE SUBCOMMAND
    # elif c.subcmd == "diff-filter":  # user specified file/directory filters on the diff performed
    #     pass
    # # DIFF-FILENC SUBCOMMAND
    # elif c.subcmd == "diff-filternc":
    #     pass
    sys.exit(0)


# Command Line Utility Functions

def validate_delta_commands_args(command_obj):
    acceptable_deltacommands = ['all', 'glyph', 'nonglyph']  # used in command line argument validations
    # Command line argument validations
    if command_obj.argc < 3:  # expected argument number
        stderr("[ufodiff] ERROR: Missing arguments.")
        sys.exit(1)
    if command_obj.arg1 not in acceptable_deltacommands:  # acceptable sub command to delta
        stderr("[ufodiff] ERROR: 'ufodiff " + command_obj.arg0 + " " + command_obj.arg1 + "' is not a valid request")
        stderr("Acceptable arguments to " + command_obj.arg0 + " include:")
        for acceptable_deltacommand in acceptable_deltacommands:
            stderr(" " + acceptable_deltacommand)
        sys.exit(1)
    if not command_obj.arg2.startswith("commits:"):  # did not include commits argument
        stderr("[ufodiff] ERROR: Please include the 'commits:[number]' argument immediately after '" + command_obj.arg1 + "'")
        sys.exit(1)
    if len(command_obj.arg2) < 9:  # did not include an integer with the commits argument
        stderr("[ufodiff] ERROR: Please include an integer after the colon in the 'commits:[number]' argument")
        sys.exit(1)


def validate_diff_commands_args(command_obj):
    # argument validations
    if command_obj.argc < 2:
        stderr("[ufodiff] ERROR: Missing arguments.")
        sys.exit(1)
    if command_obj.arg1.startswith("commits:"):
        if len(command_obj.arg1) < 9:
            stderr("[ufodiff] ERROR: Please include an integer after the colon in the 'commits:[number]' argument")
            sys.exit(1)
        else:
            commits_list = command_obj.arg1.split(':')
            commits_number = commits_list[1]
            # validate the number of commits as an integer value, exit with error message if not an integer
            validate_commits_number(commits_number)
    if command_obj.arg1.startswith("branch:"):
        if len(command_obj.arg1) < 8:
            stderr("[ufodiff] ERROR: Please include the name of a git branch following the colon in the "
                   "'branch:[name]' argument")
            sys.exit(1)


def validate_commits_number(commits_number):
    if not commits_number.isdigit():  # validate that user entered number of commits for diff is an integer
        stderr("[ufodiff] ERROR: The value following the colon in the 'commits:[number]' argument is not a valid "
               "integer value")
        sys.exit(1)
    elif int(commits_number) == 0 or int(commits_number) < 0:  # validate that the number of commits is > 0
        stderr("[ufodiff] ERROR: Please define a value over zero for the number of previous commits")
        sys.exit(1)


def get_git_root_path():
    try:
        # begin by defining current working directory as root of git repository
        unverified_gitroot_path = os.path.abspath('.')

        # check to see if this assumption is correct
        if dir_exists(os.path.join(unverified_gitroot_path, '.git')):
            verified_gitroot_path = os.path.join(unverified_gitroot_path, '.git')
        else:  # if not, recursive search up to three directories above for the git repo root
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
               "the root of your repository. " + str(e))
        sys.exit(1)

    return verified_gitroot_path

# if __name__ == '__main__':
#     main()
