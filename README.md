## ufodiff

ufodiff is a source file diff tool for typefaces developed with UFO source.

### Current Release Status

Unstable development version.

[Changelog](https://github.com/source-foundry/ufodiff/blob/master/CHANGELOG.md)

### Install

`pip install ufodiff`


### Usage

Execute the `ufodiff` command inside your git repository.  It will recursively test for the repository root from up to 4 levels of repository directory depth.  For now, don't bury your UFO code deep in the repository if you intend to test.

```
Subcommands:

- delta         --- HEAD vs. user defined previous commits as text output to standard output stream
   - all
- deltajson     --- HEAD vs. user defined previous commits as json output to standard output stream
   - all

Examples:
  ufodiff delta all commits:3 <optional UFO filter>
  ufodiff deltajson all commits:3 <optional UFO filter>
```

Increase or decrease integer value after the `commit:` argument to modify evaluation to that number of previous commits in the git repository.

Add one or more optional UFO source base filenames (e.g. Font-Regular.ufo) as last positional arguments in your command to filter the delta analysis by individual source directories.
