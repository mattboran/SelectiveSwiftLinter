#! /usr/bin/env python3
import os

from selective_linter import GitDiff
from selective_linter import SwiftLint
from selective_linter import LintError


def main():
    # Process diffs and lint
    differ = GitDiff(os.getcwd())
    differ.diff()
    linter = SwiftLint(os.getcwd(), files=differ.staged_files)
    errors = linter.check_errors_against_diff(differ.diff_lines)
    if errors:
        for error in sorted(errors):
            print(LintError(error))
    return 0


if __name__ == "__main__":
    main()
