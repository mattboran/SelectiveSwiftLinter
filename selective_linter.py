#!/usr/bin/env python3
import argparse
import os

from git_diff import GitDiff, GitHunk
from linter import SwiftLint

parser = argparse.ArgumentParser(description="Call SwiftLint only on the lines changed in git HEAD.")
parser.add_argument('--dir', 
                    action="store", 
                    type=str,
                    default=os.getcwd())

def run():
    args = parser.parse_args()
    differ = GitDiff(args.dir)
    differ.get_files_changed()
    hunks = differ.get_diff_hunks()
    for hunk in hunks:
        print(hunk)
    linter = SwiftLint(differ.files_changed)
    linter.lint()
    errors = linter.check_errors_against_diff(differ.diff_lines)
    if not errors:
        print("No errors were found")
        return 0
    else:
        print("Errors were found!")
        for error in errors:
            print(error)
        return 1
    

if __name__ == "__main__":
    run()