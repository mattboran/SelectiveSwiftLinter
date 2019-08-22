import os

import sh

class Installer:

    def __init__(self, dir):
        self.dir = dir 

    def is_repository(self):
        git_dir = self.dir + '/.git'
        if not os.path.isdir(git_dir):
            print("{} is not a valid git repository!".format(self.dir))
            return False
        return True

    def install(self): 
        pre_hook_dir = self.dir + '/.git/hooks/pre-commit'
        should_confirm = os.path.exists(pre_hook_dir)
        if should_confirm:
            answer = input("Over-write existing pre-commit hook in this repository? (Y/n) ") or "n"
            if answer[0].lower() == "n":
                return
        hook = """
        #!/usr/bin/bash
        if [ "$skipswiftlint" != "true" ]
        then
            python3 -m selective_linter
            exit $?
        else
            exit 0
        fi
        """
        with open(pre_hook_dir, 'w+') as pre_commit_hook:
            pre_commit_hook.write(hook)
        print("Wrote hook to {}".format(pre_hook_dir))