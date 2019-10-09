#!/usr/bin/env python3
import hashlib
import os

from colorama import Fore, Style


class Warning:

    UNSTAGED_WARNING = (Fore.YELLOW + "\nYou have lint errors in unstaged files! "
        "Run selective_linter -u to see those errors too" + Fore.RESET)
    BYPASS_WARNING = Fore.YELLOW + "Committing warnings or errors." + Fore.RESET


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
        where = self.file + ":" + self.line
        if "warning" in self.error_type:
            error_type = LintError._warning(self.description)
        elif "error" in self.error_type:
            error_type = LintError._error(self.description)
        return where + '\n' + error_type + self.code

    @staticmethod
    def _warning(warning):
        return Fore.YELLOW + "(warning)" + warning + ":" + Fore.RESET

    @staticmethod
    def _error(error):
        return Fore.RED + "(error)" + error + ":" + Fore.RESET


class ChangeVerifier:

    CACHE_NAME = '.lint_cache'

    def __init__(self, hunks):
        hashes = [hashlib.md5(hunk.encode()).hexdigest() for hunk in hunks]
        self.long_hash = "".join(hashes)
    
    def has_unchanged_cache(self):
        if not os.path.isfile(self.CACHE_NAME):
            return False
        long_hash = None
        with open(self.CACHE_NAME, 'r') as file:
            long_hash = file.read()
        return self.long_hash == long_hash

    def write_cache(self): 
        with open(self.CACHE_NAME, 'w+') as file:
            file.write(self.long_hash)

    def clear_cache(self):
        if os.path.isfile(self.CACHE_NAME):
            os.remove(self.CACHE_NAME)