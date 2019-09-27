#!/usr/bin/env python3
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
parser.add_argument('-u', '--unstaged',
                    action='store_true')
parser.set_defaults(unstaged=False)

running_as_script = False


def run():
    # Imports for running locally and running as module
    if running_as_script:
        from git_diff import GitDiff, GitHunk
        from linter import SwiftLint
        from output import LintError, ChangeVerifier, Warning
        from installer import Installer
    else:
        from selective_linter.git_diff import GitDiff
        from selective_linter.linter import SwiftLint
        from selective_linter.output import LintError, ChangeVerifier
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
    differ.diff(verbose=running_as_script or args.unstaged)
    linter = SwiftLint(dir=args.dir, files=differ.files_changed)
    errors = linter.check_errors_against_diff(differ.diff_lines)
    staged_errors = set([
        error for error in errors if error.split(":")[0] in differ.staged_files
    ])
    unstaged_errors = errors.difference(staged_errors)
    exit_code = 0
    cache = ChangeVerifier(differ.hunks)
    if errors:
        # If the user made the same commit twice, clear the cache and bypass this check
        if cache.has_unchanged_cache():
            cache.clear_cache()
            if staged_errors:
                print(Warning.BYPASS_WARNING)
            else: 
                print(Warning.UNSTAGED_WARNING)
            return exit_code
        cache.write_cache()
        if staged_errors:
            for error in sorted(staged_errors):
                print(LintError(error))
            print("\nErrors found. Please fix errors and retry or make no changes and re-commit to bypass.")
            exit_code = 1
        else:
            if args.unstaged:
                print("Unstaged errors: ")
                for error in sorted(unstaged_errors):
                    print(LintError(error))
            else:
                print(Warning.UNSTAGED_WARNING)
    else:
        cache.clear_cache()
    return exit_code


if __name__ == "__main__":
    running_as_script = True
    run()
