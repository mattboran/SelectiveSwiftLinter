#!/usr/bin/env python3


class LintError:

    def __init__(self, error):
        split_error = error.split(":")
        self.file = split_error[0]
        self.line = split_error[1]
        self.character = split_error[2]
        self.error_type = split_error[3]
        self.description = split_error[4]
        aux_length = len(":".join(split_error[:5])) + 1
        self.code = error[aux_length:]

    def __str__(self):
        return self.file + ":" + self.line + ": warning:" + self.description
