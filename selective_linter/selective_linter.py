import os

from selective_linter import GitDiff
from selective_linter import SwiftLint
from selective_linter import LintError
from selective_linter import Differ


def main():
    # Process diffs and lint
    differ = GitDiff(os.getcwd())
    differ.diff()
    d = Differ()
    linter = SwiftLint(os.getcwd(), files=differ.staged_files)
    errors = linter.check_errors_against_diff(differ.diff_lines)
    if errors:
        for error in sorted(errors):
            print(LintError(error))
    return 0
