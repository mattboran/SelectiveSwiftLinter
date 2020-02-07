#!/usr/bin/env python3
import os
import sh


class SwiftLint:

    def __init__(self, dir=None, files=[]):
        self.linter = sh.swiftlint.lint.bake()
        self.files = files
        rootdir = dir or os.getcwd()
        os.chdir(os.path.abspath(rootdir))
        self.log = ""
        self.lint_errors = self._lint()

    def check_errors_against_diff(self, diff_lines):
        errors = set()
        for file in self.files:
            relevant_lines = [line for line in diff_lines if line.startswith(file)]
            possible_errors = self.lint_errors.get(file) or []
            for error in possible_errors:
                line_and_file = ":".join(error.split(":")[:2])
                if line_and_file in relevant_lines:
                    errors.add(error)
        return errors

    def _lint(self):
        lint_errors = {}
        for filename in self.files:
            try:
                lint_results = self.linter(filename)
                results = lint_results.stdout.decode('utf-8', 'ignore')
            except sh.ErrorReturnCode_2 as e:
                results = e.stdout.decode('utf-8', 'ignore')
                self.log = e.stderr.decode('utf-8', 'ignore')
            if results:
                lint_errors[filename] = [result for result in results.split('\n') if result]
        return lint_errors
