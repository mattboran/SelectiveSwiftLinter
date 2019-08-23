#!/usr/bin/env python3
import argparse
import os

parser = argparse.ArgumentParser(description="Call SwiftLint only on the lines changed in git HEAD.")
parser.add_argument('--dir', 
                    action='store', 
                    type=str,
                    default=os.getcwd())
parser.add_argument('--install',
                    action='store_true')
parser.set_defaults(install=False)

running_as_script = False

def run():
    if not running_as_script:
        from selective_linter.git_diff import GitDiff
        from selective_linter.linter import SwiftLint
        from selective_linter.output import LintError, ChangeVerifier
        from selective_linter.installer import Installer
    args = parser.parse_args()
    if args.install:
        installer = Installer(args.dir)
        if installer.is_repository():
            installer.install()
        return 0
    differ = GitDiff(args.dir)
    differ.diff()
    linter = SwiftLint(dir=args.dir, files=differ.files_changed)
    errors = linter.check_errors_against_diff(differ.diff_lines)
    cache = ChangeVerifier(differ.hunks)
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
    from git_diff import GitDiff, GitHunk
    from linter import SwiftLint
    from output import LintError, ChangeVerifier
    from installer import Installer
    running_as_script = True
    run()
