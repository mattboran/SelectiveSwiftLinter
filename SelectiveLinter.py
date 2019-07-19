#!/usr/bin/env python3
import argparse
import os

import GitDiff

parser = argparse.ArgumentParser(description="Call SwiftLint only on the lines changed in git HEAD.")
parser.add_argument('--dir', 
                    action="store", 
                    type=str,
                    default=os.getcwd())

def run():
    args = parser.parse_args()
    differ = GitDiff.GitDiff(args.dir)
    differ.get_files_changed()
    changes = differ.get_diff_lines()
    print(len(changes))
    print(changes)


if __name__ == "__main__":
    run()