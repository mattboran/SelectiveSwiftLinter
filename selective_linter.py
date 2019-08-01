#!/usr/bin/env python3
import argparse
import os

from git_diff import GitDiff, GitHunk
from linter import SwiftLint
from output_formatter import LintError

parser = argparse.ArgumentParser(description="Call SwiftLint only on the lines changed in git HEAD.")
parser.add_argument('--dir', 
                    action="store", 
                    type=str,
                    default=os.getcwd())

def run():
    args = parser.parse_args()
    differ = GitDiff(args.dir)
    differ.diff()
    linter = SwiftLint(dir=args.dir, files=differ.files_changed)
    errors = linter.check_errors_against_diff(differ.diff_lines)
    print("")
    if not errors:
        return 0
    else:
        for error in errors:
            print(LintError(error))
        return 1

if __name__ == "__main__":
    run()
