#!/usr/bin/python3

import os
from shutil import rmtree
from os.path import join

from common.bash import execute_bash_script

feature_branch_name = os.environ["FEATURE_BRANCH"]

feature_branch_folder = join("./cluster/development/kon", feature_branch_name)
rmtree(feature_branch_folder)

execute_bash_script(
    [
        "git config user.name github-actions",
        "git config user.email github-actions@github.com",
        "git add .",
        "git commit -m "
        f"'Remove generated feature branch {feature_branch_name}'",
        "git push",
    ]
)
