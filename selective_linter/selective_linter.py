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
parser.add_argument('-i', '--install',
                    action='store_true')
parser.set_defaults(install=False)

running_as_script = False


def main():
    # Imports for running locally and running as module
    if running_as_script:
        from git_diff import GitDiff, GitHunk
        from linter import SwiftLint
        from output import LintError, ChangeVerifier, Warning
        from installer import Installer
    else:
        from selective_linter.git_diff import GitDiff
        from selective_linter.linter import SwiftLint
        from selective_linter.output import LintError, ChangeVerifier, Warning
        from selective_linter.installer import Installer

    # Parse command line arguments and install if necessary
    args = parser.parse_args()
    if args.install:
        installer = Installer(args.dir)
        if installer.is_repository():
            installer.install()
            return 0
        else: 
            print("Failed to install to directory")
            return 1

    # Process diffs and lint
    differ = GitDiff(args.dir)
    differ.diff(verbose=running_as_script)
    linter = SwiftLint(dir=args.dir, files=differ.staged_files)
    errors = linter.check_errors_against_diff(differ.diff_lines)
    exit_code = 0
    cache = ChangeVerifier(differ.hunks)
    if errors:
        # If the user made the same commit twice, bypass this check
        # The cache is cleared by the pre commit hook
        if cache.has_unchanged_cache():
            print(Warning.BYPASS_WARNING)
            return exit_code
        cache.write_cache()
        for error in sorted(errors):
            print(LintError(error))
        print("\nErrors found. Please fix errors and retry or make no changes and re-commit to bypass.")
        exit_code = 1
    return exit_code


if __name__ == "__main__":
    running_as_script = True
    main()
