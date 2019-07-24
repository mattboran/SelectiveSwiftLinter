#!/usr/bin/env python3
import sh
import os
import re
import sys

class GitHunk:
    def __init__(self, file, line_header, changes):
        self.file = file
        self.line_numbers = []
        self.lines_changed = []
        line_number = int(re.search(r'\+([0-9]+)', line_header).group(0)[1:])
        hunk = changes.split('\n')[1:]
        for line in hunk:
            if line.startswith('-'): continue
            elif line.startswith('+'): 
                line = line[1:]
                self.line_numbers.append(line_number)
                self.lines_changed.append(line)
            line_number += 1

    def get_file_and_line_numbers(self):
        lines = ""
        for line_number in self.line_numbers:
            lines += "{}:{}\n".format(self.file, line_number)
        return lines

    def __str__(self):
        lines_changed = ""
        for line_number, line in zip(self.line_numbers, self.lines_changed):
            lines_changed += "{}:{}: {}\n".format(self.file, line_number, line)
        return lines_changed
    
class GitDiff:
    def __init__(self, directory):
        self.directory = os.path.abspath(directory)
        self.git = sh.git.bake(_cwd=directory)
        self.hunks = []

    def get_files_changed(self):
        files = self.git('--no-pager', 'diff', '--name-only', 'HEAD')
        self.files_changed = [self.directory + '/' + file for file in files.split('\n') if file]
        return self.files_changed

    def get_diff_hunks(self):
        import pdb
        hunk_header_regex = r'(@@ -[0-9]+,[0-9]+ \+[0-9]+,[0-9]+ @@)'
        ansi_escape_regex = r'\x1B[@-_][0-?]*[ -/]*[@-~]'
        hunks = []
        for i, file in enumerate(self.files_changed):
            diff = self.git('--no-pager', 'diff', 'HEAD', file)
            stdout = diff.stdout.decode("utf-8", "ignore")
            diff_output = re.sub(ansi_escape_regex, '', stdout)
            captures = re.split(hunk_header_regex, diff_output)
            line_numbers = [group for (idx, group) in enumerate(captures[1:]) if idx % 2 == 0] 
            lines_changed = [group for (idx, group) in enumerate(captures[1:]) if idx % 2 == 1]
            for line, changes in zip(line_numbers, lines_changed):
                hunks.append(GitHunk(file, line, changes))
        self.hunks = hunks
        return hunks