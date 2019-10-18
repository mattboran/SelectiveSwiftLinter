#! /usr/bin/env python3
import argparse
import os

parser = argparse.ArgumentParser(description="""
    Call SwiftLint only on the lines changed relative to the base branch.
    """)
parser.add_argument('-d', '--dir', 
                    action='store', 
                    type=str,
                    default=os.getcwd())
running_as_script = False


def main():
    # Imports for running locally and running as module
    if running_as_script:
        from git_diff import GitDiff # pylint: disable=import-error
        from linter import SwiftLint # pylint: disable=import-error
        from output import LintError # pylint: disable=import-error
    else:
        from selective_linter.git_diff import GitDiff
        from selective_linter.linter import SwiftLint
        from selective_linter.output import LintError

    args = parser.parse_args()
    
    # Process diffs and lint
    differ = GitDiff(args.dir)
    differ.diff(verbose=running_as_script)
    linter = SwiftLint(dir=args.dir, files=differ.staged_files)
    errors = linter.check_errors_against_diff(differ.diff_lines)
    if errors:
        for error in sorted(errors):
            print(LintError(error))
    return 0


if __name__ == "__main__":
    running_as_script = True
    main()
