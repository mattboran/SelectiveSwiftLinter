# Selective (Swift) Linter

This is a package to be used to lint changes in .swift files using [Swiftlint Installed via Homebrew](https://formulae.brew.sh/formula/swiftlint). It's meant to be used as a run script in Xcode.

### Installation and  Dependencies

To install swiftlint from the terminal use Homebrew:
```sh
$ brew install swiftlint
```
To install this Python3 package

```sh
$ pip3 install selective_linter
```

To update existing installation do

```sh
$ pip3 install --upgrade selective_linter
```

To install this into an Xcode project, add the following run script build phase in project settings:

Shell: `/usr/bin/env bash`
```sh
if [ "${CONFIGURATION}" == "Debug" ]; then
    if which selective_linter >/dev/null; then
      selective_linter
    fi
fi
```