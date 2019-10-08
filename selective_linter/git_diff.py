#!/usr/bin/env python3
import os
import re
import sh
import sys

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
        for line in hunk:
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
        self.parent_branch = "master"
        self.files_changed = []
        self.staged_files = []
        self.diff_lines = []
        self.hunks = []
        self._directory = os.path.abspath(directory)
        self._git = sh.git.bake(_cwd=directory)

    def diff(self, verbose=False):
        self.parent_branch = self._get_parent_branch()
        files_changed = [
            f for f in self._get_files_changed(staged_only=False) if os.path.isfile(f)
        ]
        staged_files = [
            f for f in self._get_files_changed(staged_only=True) if os.path.isfile(f)
        ]
        for filename in files_changed:
            self.hunks += self._get_diff_hunks(filename)
        self.files_changed = files_changed
        self.staged_files = staged_files
        self.diff_lines = self._get_diff_lines()
        if verbose:
            self._print_debug_info()

    def _print_debug_info(self):
        print("Using parent branch: {}".format(self.parent_branch))
        print("Total files changed: {}".format(len(self.files_changed)))
        print("Total files staged: {}".format(len(self.staged_files)))
        print("Total git hunks: {}".format(len(self.hunks)))
        if self.staged_files:
            print("Files staged: {}".format("\n\t".join(sorted(self.staged_files))))
        unstaged_files = sorted(set(self.files_changed).difference(set(self.staged_files)))
        if unstaged_files:
            print("Unstaged files: {}".format("\n\t".join(sorted(unstaged_files))))

    def _get_current_branch(self): 
        branch = self._git('rev-parse', '--abbrev-ref', 'HEAD')
        stdout = branch.stdout.decode('utf-8', 'ignore')
        return re.sub(ANSI_ESCAPE_REGEX, '', stdout.strip())
    
    def _get_parent_branch(self):
        branch = self._git('show-branch', '-a')
        stdout = branch.stdout.decode('utf-8', 'ignore')
        branch_output = re.sub(ANSI_ESCAPE_REGEX, '', stdout)
        commits = branch_output.split('\n')
        current_branch = self._get_current_branch()
        commits_in_ancestor_branches = [
            commit for commit in commits if current_branch not in commit
                and "*" in commit
                and re.compile(r'\++\*').search(commit)
        ]
        if not commits_in_ancestor_branches:
            return current_branch
        return re.search(BRANCH_REGEX, commits_in_ancestor_branches[0]).group(1)

    def _get_files_changed(self, staged_only=False):
        if staged_only:
            files = self._git('--no-pager', 'diff', '--staged', '--name-only')
        else:
            files = self._git('--no-pager', 'diff', self.parent_branch, '--name-only')
        return [self._directory + '/' + filename 
                for filename in files.split('\n')
                if filename and filename.endswith(".swift") and os.path.isfile(filename)]
    
    def _get_diff_hunks(self, filename):
        hunks = []
        diff = self._git('--no-pager', 'diff', self.parent_branch, filename)
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
        