## Changelog

### 0.3.0

- `diff` subcommand added to support colored text diffs between UFO spec source files
- `diffnc` subcommand added to support uncolored text diffs between UFO spec source files
- extensive code refactoring
- fixed argument description errors in the in-app `--help` documentation

### v0.2.4

- bug fix for commit SHA1 digest parsing on Windows
- refactored DeltaFilePathDict class

### v0.2.3

- bug fix for Python 3 string comparison issue in ufodiff.utilities.ufo module

### v0.2.2

- PyPI documentation update

### v0.2.1

- added `deltamd` subcommand to support output of Markdown formatted delta file reports
- added short SHA1 digests for the commit history under analysis
- Commit SHA1 digests added to `delta` subcommand as header of standard output string
- Commit SHA1 digests added to `deltajson` subcommand JSON string with key `commits`


### v0.2.0

- initial release with support for the following subcommands:
    - `ufodiff delta all`
    - `ufodiff deltajson all`
