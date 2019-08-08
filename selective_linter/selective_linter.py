#!/usr/bin/env python3
import argparse
import os

from git_diff import GitDiff, GitHunk
from linter import SwiftLint
from output import LintError, ChangeVerifier

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
    cache = ChangeVerifier(differ.hunks)
    print("")
    if not errors:
        cache.clear_cache()
        return 0
    else:
        if cache.has_unchanged_cache():
            cache.clear_cache()
            print("\nBypassing errors.")
            return 0
        cache.write_cache()
        for error in errors:
            print(LintError(error))
        print("\nErrors found. Please fix errors and retry or make no changes and re-commit to bypass.")
        return 1

if __name__ == "__main__":
    run()