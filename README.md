## ufodiff

ufodiff is a source file diff tool for typefaces developed with UFO source.

### Current Status

Unstable development version

### Install

`pip install ufodiff`


### Usage

```
Subcommands:

- delta         --- text output to standard output stream
   - all
- deltajson     --- json output to standard output stream
   - all

Examples:
  ufodiff delta all commits:3 <optional UFO filter>
  ufodiff deltajson all commits:3 <optional UFO filter>
```

Increase or decrease integer value after the `commit:` argument to modify evaluation to that number of previous commits in the git repository.

Add one or more optional UFO source filepaths (e.g. Font-Regular.ufo) as last positional arguments in your command to filter the delta analysis by individual source directories.
