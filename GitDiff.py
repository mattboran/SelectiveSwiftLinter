import sh
import os
import sys

class GitDiff:
    def __init__(self, directory):
        self.directory = os.path.abspath(directory)
        self.git = sh.git.bake(_cwd=directory)

    def get_files_changed(self):
        files = self.git('--no-pager', 'diff', '--name-only', 'HEAD')
        self.files_changed = [self.directory + '/' + file for file in files.split('\n') if file]
        return self.files_changed

    def get_diff_lines(self):
        for i, file in enumerate(self.files_changed):
            diff = self.git('--no-pager', 'diff', 'HEAD', file)
            return diff
