#!/usr/bin/env python3
from colorama import Fore, Style

class LintError:
    def __init__(self, error):
        split_error = error.split(":")
        self.file = split_error[0]
        self.line = split_error[1]
        self.character = split_error[2]
        self.error_type = split_error[3]
        self.description = split_error[4]
        aux_length = len(":".join(split_error[:5]))
        self.code = error[aux_length:]

    def __str__(self):
        where = self.file + ":" + self.line
        if "warning" in self.error_type:
            error_type = Fore.YELLOW + "(warning)" + self.description + Fore.RESET
        elif "error" in self.error_type:
            error_type = Fore.RED + "(error)" + self.description + Fore.RESET
        return where + '\n' + error_type + self.code
