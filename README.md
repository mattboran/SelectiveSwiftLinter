# Selective (Swift) Linter

This is a package to be used as a pre-commit git hook to lint changes in .swift files using [Swiftlint Installed via Homebrew](https://formulae.brew.sh/formula/swiftlint).

### Installation and  Dependencies

To install swiftlint from the terminal use Homebrew:
```sh
$ brew install swiftlint
```
To install this Python3 package

```sh
$ pip3 install selective_linter
```

To install the git hook to a repository, navigate to the root of that repository and run

```sh
$ selective_linter -i
```

This also adds the `.lint_cache` file to your `.gitignore`. 

To deactivate the script run

```sh
$ git config hooks.skipswiftlint true
```