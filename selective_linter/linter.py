#!/usr/bin/env python3
import os
import sh

class SwiftLint:
    def __init__(self, dir=None, files=[]):
        self.linter = sh.swiftlint.lint.bake() # pylint: disable=no-member
        self.files = files
        self.lint_errors = {}
        rootdir = dir or os.getcwd()
        os.chdir(os.path.abspath(rootdir))
        self._lint()

    def _lint(self):
        lint_errors = {}
        for filename in self.files:
            lint_errors[filename] = []
            lint_results = self.linter(filename)
            results = lint_results.stdout.decode("utf-8", "ignore")
            if results:
                # import pdb; pdb.set_trace()
                results = results.split('\n')
                lint_errors[filename] += results
        self.lint_errors = lint_errors

    def check_errors_against_diff(self, diff_lines):
        errors = set()
        for line in diff_lines:
            filename = line.split(':')[0]
            line_number = line.split(':')[1]
            potential_errors = self.lint_errors[filename]
            for error in potential_errors:
                location = ":".join([filename, line_number])
                if location in error:
                    errors.add(error)
        return errors

