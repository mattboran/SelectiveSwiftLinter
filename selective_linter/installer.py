import os

import sh

HOOK = """
#!/usr/bin/bash
skipswiftlint=$(git config --bool hooks.skipswiftlint)
if [ "$skipswiftlint" != "true" ]
then
    python3 -m selective_linter
    retVal=$?
    if [ $retVal != 0 ]
    then
    cat <<\EOF

You can disable this check by using:

    git config hooks.skipswiftlint true
EOF
fi
    exit $retVal
else
    exit 0
fi
"""
        
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
        with open(pre_hook_dir, 'w+') as pre_commit_hook:
            pre_commit_hook.write(HOOK)
        print("Wrote hook to {}".format(pre_hook_dir))
        sh.chmod('744', pre_hook_dir)
        print("Made hook executable")