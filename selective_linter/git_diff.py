#!/usr/bin/env python3
import os
import re
import sh

# Constants

ANSI_ESCAPE_REGEX = r'\x1B[@-_][0-?]*[ -/]*[@-~]'
HUNK_HEADER_NEW_REGEX = r'(@@ -[0-9]+,[0-9]+ \+[0-9]+ @@)'
HUNK_HEADER_EXISTING_REGEX = r'(@@ -[0-9]+,[0-9]+ \+[0-9]+,[0-9]+ @@)'
BRANCH_REGEX = r'\[([A-Za-z0-9/-]+)]'


class GitHunk:

    def __init__(self, file, line_header, changes):
        self.file = file
        self.line_numbers = []
        self.lines_changed = []
        matches = re.search(r'\+([0-9]+)', line_header)
        hunk = changes.split('\n')[1:]
        line_number = int(matches.group(0)[1:])
        for line in hunk[1:-1]:
            if line.startswith('-'):
                continue
            else:
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
        self.staged_files = []
        self.diff_lines = []
        self.hunks = []
        self._directory = os.path.abspath(directory)
        self._git = sh.git.bake(_cwd=directory)

    def diff(self, verbose=False):
        staged_files = [
            f for f in self._get_files_changed() if os.path.isfile(f)
        ]
        for filename in staged_files:
            self.hunks += self._get_diff_hunks(filename)
        self.staged_files = staged_files
        self.diff_lines = self._get_diff_lines()
        if verbose:
            self._print_debug_info()

    def _print_debug_info(self):
        print("Total files staged: {}".format(len(self.staged_files)))
        print("Total git hunks: {}".format(len(self.hunks)))
        if self.staged_files:
            print("Files staged: {}".format("\n\t".join(sorted(self.staged_files))))

    def _get_files_changed(self):
        unstaged_files = self._git('--no-pager', 'diff', '--name-only').stdout.decode('utf-8', 'ignore')
        staged_files = self._git('--no-pager', 'diff', '--name-only', 'HEAD').stdout.decode('utf-8', 'ignore')
        files = unstaged_files + staged_files
        return [self._directory + '/' + filename
                for filename in files.split('\n')
                if filename and filename.endswith(".swift") and os.path.isfile(filename)]

    def _get_diff_hunks(self, filename):
        hunks = []
        diff = self._git('--no-pager', 'diff', 'HEAD', filename)
        stdout = diff.stdout.decode('utf-8', 'ignore')
        diff_output = re.sub(ANSI_ESCAPE_REGEX, '', stdout)
        regex = self._regex_for_diff_output(diff_output)
        captures = re.split(regex, diff_output)
        line_numbers = [group for (idx, group) in enumerate(captures[1:]) if idx % 2 == 0] 
        lines_changed = [group for (idx, group) in enumerate(captures[1:]) if idx % 2 == 1]
        for line, changes in zip(line_numbers, lines_changed):
            hunks.append(GitHunk(filename, line, changes))
        return hunks

    def _regex_for_diff_output(self, diff_output):
        if "new file" in diff_output:
            return HUNK_HEADER_NEW_REGEX
        return HUNK_HEADER_EXISTING_REGEX

    def _get_diff_lines(self):
        diff_lines = []
        for hunk in self.hunks:
            diff_lines += hunk.get_file_and_line_numbers()
        return diff_lines
