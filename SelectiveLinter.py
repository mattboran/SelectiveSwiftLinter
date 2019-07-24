#!/usr/bin/env python3
import argparse
import os

from GitDiff import GitDiff, GitHunk

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

if __name__ == "__main__":
    run()