## ufodiff [![Build Status](https://travis-ci.org/source-foundry/ufodiff.svg?branch=master)](https://travis-ci.org/source-foundry/ufodiff) [![Build status](https://ci.appveyor.com/api/projects/status/o2vdn1uf7uxau3o7/branch/master?svg=true)](https://ci.appveyor.com/project/chrissimpkins/ufodiff/branch/master)

ufodiff is a command line source file diff tool for typefaces that are developed with UFO source.

It examines git repositories for changes to files that are part of the UFO source spec.

Currently, UFO version 2 is fully supported and UFO version 3 is partially supported.

## Current Release Status

Unstable development version.  

[Changelog](https://github.com/source-foundry/ufodiff/blob/master/CHANGELOG.md)

## Install

Installation with `pip` is recommended:

`$ pip install ufodiff`


## Usage

`ufodiff` is a command line executable.  Application features are accessed via subcommands to the `ufodiff` executable.  

Execute `ufodiff` inside your git repository.  It will recursively test for the repository root from up to 4 levels of repository directory depth.  If you are receiving exceptions due to inability to instantiate your git repository object, try bumping your working directory
up a few levels closer to the root.  There are otherwise no restrictions to where `ufodiff` is executed in the repository.


#### View Results in Terminal

By default, data are displayed in your terminal.  Use one of the following approaches to either pipe data to another application or write data to a file.


#### Piping Data to Other Applications

Use the `|` idiom to pipe the standard output stream from `ufodiff` to another application for further processing like this:

```
$ ufodiff deltajson all commits:3 | anotherapp --dosomething-with-json
```

#### File Writes

Use the `>` idiom to write the data in the standard output stream to a filepath like this:

```
$ ufodiff delta all commits:1 > myfont_delta.txt
```

### ufodiff Subcommands

#### Subcommand List

- <a href="#delta">delta</a>
- <a href="#deltajson">deltajson</a>
- <a href="#deltamd">deltamd</a>

<h3 id="delta"><a href="">delta</a></h3>

`ufo delta` generates file modification, addition, and deletion reports over a user specified number of commits in text format.  The data are streamed through standard output in a newline delimited fashion with indicators for the type of file change.

The file change indicators include:

- **[A]** file added
- **[D]** file deleted
- **[M]** file modified

For Markdown formatted data, see the `deltamd` command.  For JSON formatted data, see the `deltajson` subcommand.

```
Subcommands:

- delta         --- HEAD vs. user defined previous commits as text output to standard output stream
   - all

Examples:
  ufodiff delta all commits:3 <optional UFO filter>
```

Increase or decrease the integer value after the `commits:` argument to change the depth of the git commit history that you want to examine.

Add one or more optional UFO source base filenames (e.g. Font-Regular.ufo) as last positional arguments in your command to filter the delta analysis by individual source directories.


<h3 id="deltajson"><a href=""> deltajson</a></h3>


`ufo deltajson` generates file modification, addition, and deletion reports over a user specified number of commits in JSON format.  The data are streamed through standard output.

For plain text formatted data, see the `delta` subcommand.  For Markdown formatted data, see the `deltamd` command.

```
Subcommands:

- deltajson     --- HEAD vs. user defined previous commits as json output to standard output stream
   - all

Example:
  ufodiff deltajson all commits:3 <optional UFO filter>
```

JSON data are formatted as follows:

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

Add one or more optional UFO source base filenames (e.g. Font-Regular.ufo) as last positional arguments in your command to filter the delta analysis by individual source directories.


<h3 id="deltamd"><a href=""> deltamd</a></h3>

`ufodiff deltamd` generates file modification, addition, and deletion reports over a user specified number of commits in Github flavored Markdown format.  The data are streamed through standard output.

For plain text formatted data, see the `delta` command.  For JSON formatted data, see the `deltajson` command.

```
Subcommands:

- deltamd       --- HEAD vs. user defined previous commits as Markdown output to standard output stream
   - all

Example:
  ufodiff deltamd all commits:3 <optional UFO filter>
```

Increase or decrease the integer value after the `commits:` argument to change the depth of the git commit history that you want to examine.

Add one or more optional UFO source base filenames (e.g. Font-Regular.ufo) as last positional arguments in your command to filter the delta analysis by individual source directories.


### License

[MIT License](https://github.com/source-foundry/ufodiff/blob/master/docs/LICENSE)