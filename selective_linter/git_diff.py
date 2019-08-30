#!/usr/bin/env python3
import os
import re
import sh
import sys

# Constants

ANSI_ESCAPE_REGEX = r'\x1B[@-_][0-?]*[ -/]*[@-~]'
HUNK_HEADER_NEW_REGEX = r'(@@ -[0-9]+,[0-9]+ \+[0-9]+ @@)'
HUNK_HEADER_EXISTING_REGEX = r'(@@ -[0-9]+,[0-9]+ \+[0-9]+,[0-9]+ @@)'

class GitHunk:

    def __init__(self, file, line_header, changes):
        self.file = file
        self.line_numbers = []
        self.lines_changed = []
        matches = re.search(r'\+([0-9]+)', line_header)
        line_number = int(matches.group(0)[1:])
        hunk = changes.split('\n')[1:]
        for line in hunk:
            if line.startswith('-'): 
                continue
            elif line.startswith('+'): 
                line = line[1:]
                self.line_numbers.append(line_number)
                self.lines_changed.append(line)
            line_number += 1

    def get_file_and_line_numbers(self):
        lines = []
        for line_number in self.line_numbers:
            lines.append("{}:{}".format(self.file, line_number))
        return lines

    def encode(self):
        return self.__str__().encode("utf-8")

    def __str__(self):
        lines_changed = ""
        for line_number, line in zip(self.line_numbers, self.lines_changed):
            lines_changed += "{}:{}: {}\n".format(self.file, line_number, line)
        return lines_changed


class GitDiff:

    def __init__(self, directory):
        self.files_changed = []
        self.diff_lines = []
        self.hunks = []
        self._directory = os.path.abspath(directory)
        self._git = sh.git.bake(_cwd=directory)

    def diff(self):
        files_changed = self._get_files_changed()
        self.files_changed = [f for f in files_changed if os.path.isfile(f)]
        for i, filename in enumerate(self.files_changed):
            print("Diffing file {}: {}".format(i, filename))
            self.hunks += self._get_diff_hunks(filename)
        self.diff_lines = self._get_diff_lines()
        
    def _get_files_changed(self):
        files = self._git('--no-pager', 'diff', '--cached', '--name-only')
        files_changed = [self._directory + '/' + filename 
        for filename in files.split('\n') if filename and filename.endswith(".swift")]
        return files_changed
    
    def _get_diff_hunks(self, filename):
        hunks = []
        diff = self._git('--no-pager', 'diff', '--cached', filename)
        stdout = diff.stdout.decode("utf-8", "ignore")
        diff_output = re.sub(ANSI_ESCAPE_REGEX, '', stdout)
        regex = self._regex_for_diff_output(diff_output)
        captures = re.split(regex, diff_output)
        line_numbers = [group for (idx, group) in enumerate(captures[1:]) if idx % 2 == 0] 
        lines_changed = [group for (idx, group) in enumerate(captures[1:]) if idx % 2 == 1]
        for line, changes in zip(line_numbers, lines_changed):
            hunk = GitHunk(filename, line, changes)
            hunks.append(hunk)
        return hunks

    def _regex_for_diff_output(self, diff_output):
        if 'new file' in diff_output:
             return HUNK_HEADER_NEW_REGEX
        return HUNK_HEADER_EXISTING_REGEX

    def _get_diff_lines(self):
        diff_lines = []
        for hunk in self.hunks:
            diff_lines += hunk.get_file_and_line_numbers()
        return diff_lines
        