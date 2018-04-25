## Changelog

### v0.5.2

- eliminated support for Python v2.6
- updated gitpython dependency to version 2.1.9

### v0.5.1

- updated gitpython dependency to version 2.1.7

### v0.5.0

- added support for full UFO v3 spec to all commands
- fixed bug in the branch diff reports, now comparison branch relative to current branch (comparison..current) as indicated in the documentation
- updated/cleaned diff report strings

### v0.4.1

- fix for Markdown text error (branch list item formatting)

### v0.4.0

- added support for branch vs. branch analysis to the `delta`, `deltajson`, and `deltamd` commands
- updated `delta`, `deltajson`, and `deltamd` argument validations
- bugfix for the git diff performed with the `diff` and `diffnc` commands (`branch...branch` to `branch..branch`)


### v0.3.0

- `diff` subcommand added to support colored text diffs between UFO spec source files
- `diffnc` subcommand added to support uncolored text diffs between UFO spec source files
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
