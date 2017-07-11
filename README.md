<img src="https://github.com/source-foundry/ufodiff/blob/images/images/ufodiff-logo-crunch.png?raw=true">

## [![Build Status](https://travis-ci.org/source-foundry/ufodiff.svg?branch=master)](https://travis-ci.org/source-foundry/ufodiff) [![Build status](https://ci.appveyor.com/api/projects/status/o2vdn1uf7uxau3o7/branch/master?svg=true)](https://ci.appveyor.com/project/chrissimpkins/ufodiff/branch/master) [![codecov](https://codecov.io/gh/source-foundry/ufodiff/branch/master/graph/badge.svg)](https://codecov.io/gh/source-foundry/ufodiff)

ufodiff is a command line UFO source file modification and diff tool for collaborative typeface development projects.

It examines git repositories for changes to files that are part of the UFO source spec only (i.e. all file changes in the repository external to the UFO source code are not considered by the tool).  It supports reporting of UFO source file additions, deletions, and modifications as well as colored and uncolored text diffs for UFO source files.  Output is streamed through the standard output stream and can be piped to other applications.

UFO version 2 is fully supported in the current release.  UFO version 3 is partially supported and [full support is planned](https://github.com/source-foundry/ufodiff/issues/1).

## Contents

- [Current Release Status](#current-release-status)
- [Install Instructions](#install)
- [Quickstart Examples](#quickstart-examples)
- [Usage](#usage)
- [Subcommand Documentation](#ufodiff-subcommands)
   - [delta](#delta)
   - [deltajson](#deltajson)
   - [deltamd](#deltamd)
   - [diff](#diff)
   - [diffnc](#diffnc)
- [Issue Reporting](#issues)
- [License](#license)

## Current Release Status

Stable development version.  

[Changelog](https://github.com/source-foundry/ufodiff/blob/master/CHANGELOG.md)

## Install

Installation with `pip` is recommended:

`$ pip install ufodiff`


Upgrade a previous installation with:

`$ pip install --upgrade ufodiff`


## Quickstart Examples

### List UFO source file additions, deletions, and modifications

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


### Text diff UFO source files

#### Colored text diff output
##### _For terminals with ANSI color code support_

All modified UFO files, last two commits:

```
$ ufodiff diff commits:2
```

All modified UFO files, last five commits:

```
$ ufodiff diff commits:5
```

All modified files, master (current) vs. development branch:

```
$ ufodiff diff branch:development
```

#### Uncolored text diff output

All modified UFO files, last two commits:

```
$ ufodiff diffnc commits:2
```

All modified UFO files, last five commits:

```
$ ufodiff diffnc commits:5
```

All modified files, master (current) vs. development branch:

```
$ ufodiff diffnc branch:development
```


## Usage

`ufodiff` is a command line executable.  Application features are accessed via subcommands to the `ufodiff` executable.  

Execute `ufodiff` inside the git repository where you develop your typeface.  It will recursively test for the repository root from up to 4 levels of repository directory depth.  If you are receiving exceptions due to inability to instantiate your git repository object, try bumping your working directory
up a few levels closer to the root.  There are otherwise no restrictions to where `ufodiff` is executed inside the repository.  The source directory does not need to be the current working directory.


#### View Results in Terminal

By default, data are displayed in your terminal.  Use one of the following approaches to either pipe data to another application or write data to a file.


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

<h3 id="delta"><a href="">delta</a></h3>

`ufo delta` generates file modification, addition, and deletion reports over a user specified number of commits in text format.  The data are streamed through standard output in a newline delimited fashion with indicators for the type of file change.

The file change indicators include:

- **[A]** file added
- **[D]** file deleted
- **[M]** file modified

For Markdown formatted data, see the `deltamd` command.  For JSON formatted data, see the `deltajson` subcommand.

The syntax is:

```
ufodiff delta [all] [commits:N] <optional UFO filter>
```

where `N` is an integer value that represents the number of commits in the git commit history to examine.

Examples:

```
$ ufodiff delta all commits:3
$ ufodiff delta all commits:5
$ ufodiff delta all commits:3 Test-Regular.ufo
```

Increase or decrease the integer value after the `commits:` argument to change the depth of the git commit history that you want to examine.

Add one or more optional UFO source base directory name (e.g. Font-Regular.ufo) as last positional arguments in your command to filter the delta analysis by individual source directories.


<h3 id="deltajson"><a href=""> deltajson</a></h3>


`ufo deltajson` generates file modification, addition, and deletion reports over a user specified number of commits in JSON format.  The data are streamed through standard output.

For plain text formatted data, see the `delta` subcommand.  For Markdown formatted data, see the `deltamd` command.

The syntax is: 

```
ufodiff deltajson [all] [commits:N] <optional UFO filter>
```

where `N` is an integer value that represents the number of commits in the git commit history to examine.

Examples:

```
$ ufodiff deltajson all commits:3
$ ufodiff deltajson all commits:5
$ ufodiff deltajson all commits:3 Test-Regular.ufo
```

JSON data are formatted as:

```json
{
    "commits": [
      "25087a1ab",
      "27fdb2e48",
      "6edab459e"
    ],
    "added": [
      "filepath 1",
      "filepath 2",
      "filepath 3"
    ],
    "deleted": [
      "filepath 1",
      "filepath 2",
      "filepath 3"
    ],
    "modified": [
      "filepath 1",
      "filepath 2",
      "filepath 3"
    ]
}
```

Increase or decrease the integer value after the `commits:` argument to change the depth of the git commit history that you want to examine.

Add one or more optional UFO source base directory name (e.g. Font-Regular.ufo) as last positional arguments in your command to filter the delta analysis by individual source directories.


<h3 id="deltamd"><a href=""> deltamd</a></h3>

`ufodiff deltamd` generates file modification, addition, and deletion reports over a user specified number of commits in Github flavored Markdown format.  The data are streamed through standard output.

For plain text formatted data, see the `delta` command.  For JSON formatted data, see the `deltajson` command.

The syntax is: 

```
ufodiff deltamd [all] [commits:N] <optional UFO filter>
```

where `N` is an integer value that represents the number of commits in the git commit history to examine.

Examples:

```
$ ufodiff deltamd all commits:3
$ ufodiff deltamd all commits:5
$ ufodiff deltamd all commits:3 Test-Regular.ufo
```

Increase or decrease the integer value after the `commits:` argument to change the depth of the git commit history that you want to examine.

Add one or more optional UFO source base directory name (e.g. Font-Regular.ufo) as last positional arguments in your command to filter the delta analysis by individual source directories.


<h3 id="diff"><a href=""> diff</a></h3>

`ufodiff diff` provides colored text diffs for all UFO files that were modified across one or more commits in the working branch, or between the HEAD of the working branch and any other branch in the repository.

For uncolored diffs, see the `diffnc` command.

The command syntax is:

```
ufodiff diff [commits:N | branch:X]
```

where `N` is an integer value that represents the number of commits in the git commit history to examine and `X` is the name of an existing branch in the git repository.  These are mutually exclusive arguments.

Examples:

```
$ ufodiff diff commits:2
$ ufodiff diff branch:master

```


<h3 id="diffnc"><a href=""> diffnc</a></h3>

`ufodiff diffnc` provides uncolored text diffs for all UFO files that were modified across one or more commits in the working branch, or between the HEAD of the working branch and any other branch in the repository.

For colored diffs intended for use in terminals that support ANSI color codes, see the `diff` command.

The command syntax is:

```
ufodiff diffnc [commits:N | branch:X]
```

where `N` is an integer value that represents the number of commits in the git commit history to examine and `X` is the name of an existing branch in the git repository.  These are mutually exclusive arguments.

Examples:

```
$ ufodiff diffnc commits:2
$ ufodiff diffnc branch:master

```

## Issues

Please submit bug reports and feature requests as an [issue report](https://github.com/source-foundry/ufodiff/issues/new) on our Github repository.


## License

[MIT License](https://github.com/source-foundry/ufodiff/blob/master/docs/LICENSE)