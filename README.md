<img src="https://github.com/source-foundry/ufodiff/blob/images/images/ufodiff-logo-2-crunch.png?raw=true">

[![PyPI](https://img.shields.io/pypi/v/ufodiff?color=blueviolet&label=PyPI&logo=python&logoColor=white)](https://pypi.org/project/ufodiff)
[![Build Status](https://travis-ci.com/source-foundry/ufodiff.svg?branch=master)](https://travis-ci.com/source-foundry/ufodiff)
[![Build status](https://ci.appveyor.com/api/projects/status/o2vdn1uf7uxau3o7/branch/master?svg=true)](https://ci.appveyor.com/project/chrissimpkins/ufodiff/branch/master)
![Python Lints](https://github.com/source-foundry/ufodiff/workflows/Python%20Lints/badge.svg)
[![codecov](https://codecov.io/gh/source-foundry/ufodiff/branch/master/graph/badge.svg)](https://codecov.io/gh/source-foundry/ufodiff)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/23e4187ff4474576b7e3334075180202)](https://app.codacy.com/app/SourceFoundry/ufodiff)

ufodiff is a command line UFO source file diff tool for collaborative typeface development projects.

It examines git repositories for changes to files that are part of the UFO source spec only (i.e. all file changes in the repository external to the UFO source code are not considered by the tool). It supports reporting of UFO source file additions, deletions, and modifications as well as colored and uncolored text diffs for UFO source files that were modified between branches or across one or more commits.

UFO versions 2 and 3 are fully supported in the current release.

<img src="https://github.com/source-foundry/ufodiff/blob/images/images/diff-delta-crunch.png?raw=true">

## Contents

- [Contents](#contents)
- [Install](#install)
- [Quickstart Examples](#quickstart-examples)
    - [Plain Text](#plain-text)
    - [Markdown](#markdown)
    - [JSON](#json)
    - [Colored text diff](#colored-text-diff)
      - [_For terminals with ANSI color code support_](#for-terminals-with-ansi-color-code-support)
    - [Uncolored text diff](#uncolored-text-diff)
- [Usage](#usage)
    - [View Results in Terminal](#view-results-in-terminal)
    - [Piping Data to Other Applications](#piping-data-to-other-applications)
    - [File Writes](#file-writes)
  - [ufodiff Subcommands](#ufodiff-subcommands)
    - [Subcommand List](#subcommand-list)
- [Issues](#issues)
- [License](#license)

## Install

Installation with `pip` is recommended:

`$ pip install ufodiff`

Upgrade a previous installation with:

`$ pip install --upgrade ufodiff`

## Quickstart Examples

<h3><a href="">List UFO source file additions, deletions, and modifications</h3>

#### Plain Text

For the last two commits:

```
$ ufodiff delta all commits:2
```

For the last five commits:

```
$ ufodiff delta all commits:5
```

For the last five commits, only from the Test-Regular.ufo source directory (note: not a filepath to source, only include UFO directory name):

```
$ ufodiff delta all commits:5 Test-Regular.ufo
```

Between the current branch and the `development` branch

```
# ufodiff delta all branch:development
```

#### Markdown

For the last two commits in current branch:

```
$ ufodiff deltamd all commits:2
```

For the last five commits in current branch:

```
$ ufodiff deltamd all commits:5
```

For the last five commits in current branch, only from the Test-Regular.ufo source directory (note: not a filepath to source, only include UFO directory name):

```
$ ufodiff deltamd all commits:5 Test-Regular.ufo
```

Between the current branch and the `development` branch

```
# ufodiff deltamd all branch:development
```

#### JSON

For the last two commits in current branch:

```
$ ufodiff deltajson all commits:2
```

For the last five commits in current branch:

```
$ ufodiff deltajson all commits:5
```

For the last five commits in current branch, only from the Test-Regular.ufo source directory (note: not a filepath to source, only include UFO directory name):

```
$ ufodiff deltajson all commits:5 Test-Regular.ufo
```

Between the current branch and the `development` branch

```
# ufodiff deltajson all branch:development
```

<h3><a href="">Text diff UFO source files</h3>

#### Colored text diff

##### _For terminals with ANSI color code support_

All modified UFO files, last two commits:

```
$ ufodiff diff commits:2
```

All modified UFO files, last five commits:

```
$ ufodiff diff commits:5
```

All modified files, current branch vs. development branch:

```
$ ufodiff diff branch:development
```

#### Uncolored text diff

All modified UFO files, last two commits:

```
$ ufodiff diffnc commits:2
```

All modified UFO files, last five commits:

```
$ ufodiff diffnc commits:5
```

All modified files, current branch vs. development branch:

```
$ ufodiff diffnc branch:development
```

## Usage

`ufodiff` is a command line executable. Application features are accessed via subcommands to the `ufodiff` executable.

Execute `ufodiff` inside the git repository where you develop your typeface. It will recursively test for the repository root from up to 4 levels of repository directory depth. If you are receiving exceptions due to inability to instantiate your git repository object, try bumping your working directory
up a few levels closer to the root. There are otherwise no restrictions to where `ufodiff` is executed inside the repository. The source directory does not need to be the current working directory.

#### View Results in Terminal

By default, data are displayed in your terminal. Use one of the following approaches to either pipe data to another application or write data to a file.

#### Piping Data to Other Applications

On Unix/Linux/OS X platforms, use the `|` idiom to pipe the standard output stream from `ufodiff` to another application for further processing like this:

```
$ ufodiff deltajson all commits:3 | anotherapp --dosomething-with-json
```

#### File Writes

On Unix/Linux/OS X platforms, use the `>` idiom to write the data in the standard output stream to a filepath like this:

```
$ ufodiff delta all commits:1 > myfont_delta.txt
```

### ufodiff Subcommands

#### Subcommand List

- [delta](#delta)
- [deltajson](#deltajson)
- [deltamd](#deltamd)
- [diff](#diff)
- [diffnc](#diffnc)

The commit history for all commands is compared with the `HEAD~N` git idiom. The branch comparisons across all commands are performed with the `test_branch..current_branch` git idiom.

<h3 id="delta"><a href="">delta</a></h3>

`ufo delta` generates file modification, addition, and deletion reports over a user specified number of commits or across git branches. The data are streamed in plain text format through standard output with indicators for the type of file change.

The file change indicators include:

- **[A]** file added
- **[D]** file deleted
- **[M]** file modified

For Markdown formatted data, see the `deltamd` command. For JSON formatted data, see the `deltajson` subcommand.

The syntax is:

```
ufodiff delta [all] [commits:[N] | branch:[name]] <optional UFO filter>
```

where `N` is an integer value that represents the number of commits in the git commit history to examine and `name` is the name of an existing git branch in the repository. These are mutually exclusive arguments.

_Examples_:

```
$ ufodiff delta all commits:3
$ ufodiff delta all commits:5
$ ufodiff delta all commits:3 Test-Regular.ufo
$ ufodiff delta all branch:development
$ ufodiff delta all branch:development Test-Regular.ufo
```

Increase or decrease the integer value after the `commits:` argument to change the depth of the git commit history that you want to examine. Include an existing git branch name following the `branch:` argument to perform a branch vs. branch comparison.

Add one or more optional UFO source base directory names (e.g. Font-Regular.ufo) as last positional arguments in your command to filter the delta analysis by individual source directories.

<h3 id="deltajson"><a href=""> deltajson</a></h3>

`ufo deltajson` generates file modification, addition, and deletion reports over a user specified number of commits or across git branches. The data are streamed in JSON format through standard output.

For plain text formatted data, see the `delta` subcommand. For Markdown formatted data, see the `deltamd` command.

The syntax is:

```
ufodiff deltajson [all] [commits:[N] | branch:[name]] <optional UFO filter>
```

where `N` is an integer value that represents the number of commits in the git commit history to examine and `name` is the name of an existing git branch in the repository. These are mutually exclusive arguments.

_Examples_:

```
$ ufodiff deltajson all commits:3
$ ufodiff deltajson all commits:5
$ ufodiff deltajson all commits:3 Test-Regular.ufo
$ ufodiff deltajson all branch:development
$ ufodiff deltajson all branch:development Test-Regular.ufo
```

JSON data for commit history analyses are formatted as:

```json
{
  "commits": ["25087a1ab", "27fdb2e48", "6edab459e"],
  "added": ["filepath 1", "filepath 2", "filepath 3"],
  "deleted": ["filepath 1", "filepath 2", "filepath 3"],
  "modified": ["filepath 1", "filepath 2", "filepath 3"]
}
```

JSON data for branch vs. branch analyses are formatted as:

```json
{
  "branches": ["branch 1", "branch 2"],
  "added": ["filepath 1", "filepath 2", "filepath 3"],
  "deleted": ["filepath 1", "filepath 2", "filepath 3"],
  "modified": ["filepath 1", "filepath 2", "filepath 3"]
}
```

Increase or decrease the integer value after the `commits:` argument to change the depth of the git commit history that you want to examine. Include an existing git branch name following the `branch:` argument to perform a branch vs. branch comparison.

Add one or more optional UFO source base directory name (e.g. Font-Regular.ufo) as last positional arguments in your command to filter the delta analysis by individual source directories.

<h3 id="deltamd"><a href=""> deltamd</a></h3>

`ufodiff deltamd` generates file modification, addition, and deletion reports over a user specified number of commits or across git branches. The data are streamed in Github flavored Markdown format through standard output.

For plain text formatted data, see the `delta` command. For JSON formatted data, see the `deltajson` command.

The syntax is:

```
ufodiff deltamd [all] [commits:[N] | branch:[name]] <optional UFO filter>
```

where `N` is an integer value that represents the number of commits in the git commit history to examine and `name` is an existing git branch name for a branch vs. branch comparison.

_Examples_:

```
$ ufodiff deltamd all commits:3
$ ufodiff deltamd all commits:5
$ ufodiff deltamd all commits:3 Test-Regular.ufo
```

Increase or decrease the integer value after the `commits:` argument to change the depth of the git commit history that you want to examine. Include an existing git branch name following the `branch:` argument to perform a branch vs. branch comparison.

Add one or more optional UFO source base directory name (e.g. Font-Regular.ufo) as last positional arguments in your command to filter the delta analysis by individual source directories.

<h3 id="diff"><a href=""> diff</a></h3>

`ufodiff diff` provides colored text diffs for all UFO files that were modified across one or more commits in the working branch, or between the HEAD of the working branch and any other branch in the repository.

For uncolored diffs, see the `diffnc` command.

The command syntax is:

```
ufodiff diff [commits:[N] | branch:[name]]
```

where `N` is an integer value that represents the number of commits in the git commit history to examine and `name` is the name of an existing git branch in the repository. These are mutually exclusive arguments.

_Examples_:

```
$ ufodiff diff commits:2
$ ufodiff diff branch:master
```

<h3 id="diffnc"><a href=""> diffnc</a></h3>

`ufodiff diffnc` provides uncolored text diffs for all UFO files that were modified across one or more commits in the working branch, or between the HEAD of the working branch and any other branch in the repository.

For colored diffs intended for use in terminals that support ANSI color codes, see the `diff` command.

The command syntax is:

```
ufodiff diffnc [commits:[N] | branch:[name]]
```

where `N` is an integer value that represents the number of commits in the git commit history to examine and `name` is the name of an existing git branch in the repository. These are mutually exclusive arguments.

_Examples_:

```
$ ufodiff diffnc commits:2
$ ufodiff diffnc branch:master
```

## Issues

Please submit bug reports and feature requests as an [issue report](https://github.com/source-foundry/ufodiff/issues/new) on our Github repository.

## License

[MIT License](https://github.com/source-foundry/ufodiff/blob/master/docs/LICENSE)
