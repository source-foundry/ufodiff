## Changelog

### v1.0.2

- fix: deprecated string literal escapes refactored to raw strings. ufo.py module (deprecated as of Py3.6)
- reformat import statements based with default isort formatting
- refactor all Python source to achieve line lengths < 90
- add flake8 lint testing
- update gitpython dependency to v3.1.8

### v1.0.1

- update gitpython dependency to v3.1.5 - decreases package size by removing tests from distribution
- update gitdb dependency to v4.0.5
- update smmap dependency to v3.0.4
- add dependabot configuration file

### v1.0.0

- v1 release
- eliminate Py2.7 support
- remove unnecessary import statement in `subcommands.diff` module
- black source formatting
- update Python dependencies
- broaden pinned depdendency definitions in requirements.txt file
- use requirements.txt dependency versions in CI testing
- add macOS CI testing

### v0.5.4

- updated gitpython dependency to version 2.1.11

### v0.5.3

- updated gitpython dependency to version 2.1.10
- added license to Python wheel distributions
- removed Travis CI testing, added Semaphore CI testing

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
