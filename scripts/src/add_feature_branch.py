#!/usr/bin/python3

import os
from distutils.dir_util import copy_tree
from os.path import join
import shutil

from common.bash import execute_bash_script
from common.yaml import update_yaml_file

feature_branch_name = os.environ["FEATURE_BRANCH"]
kustomization_names = ["alpi", "common", "hasura", "hasura-metadata", "nami", "zoru"]

execute_bash_script(
    [
        "git config user.name github-actions",
        "git config user.email github-actions@github.com",
        f"git checkout -B {feature_branch_name}",
    ]
)

for kustomization_name in kustomization_names:
    update_yaml_file(
        f"./overlay/development/kon/{kustomization_name}/kustomization.yaml",
        "namespace",
        feature_branch_name,
    )

execute_bash_script(
    [
        "git add .",
        "git commit -m "
        + f"'Setup namespace for {feature_branch_name} feature branch'",
        f"git push -f --set-upstream origin {feature_branch_name}",
    ]
)

execute_bash_script(
    [
        "git checkout main",
    ]
)

feature_branch_folder = join("./cluster/development/kon", feature_branch_name)
if os.path.exists(feature_branch_folder):
    shutil.rmtree(feature_branch_folder)
os.mkdir(feature_branch_folder)
copy_tree("./cluster/development/kon/main", feature_branch_folder)

update_yaml_file(
    join(feature_branch_folder, "source/kustomization.yaml"),
    "namePrefix",
    f"{feature_branch_name}-",
)
update_yaml_file(
    join(feature_branch_folder, "source/git_repository.yaml"),
    "spec.ref.branch",
    feature_branch_name,
)

for kustomization_name in kustomization_names:
    update_yaml_file(
        join(feature_branch_folder, f"app/{kustomization_name}_sync.yaml"),
        "spec.sourceRef.name",
        f"{feature_branch_name}-branch",
    )
update_yaml_file(
    join(feature_branch_folder, "app/kustomization.yaml"),
    "namespace",
    feature_branch_name,
)

execute_bash_script(
    [
        "git add .",
        "git commit -m "
        + f"'Add development environment for feature branch {feature_branch_name}'",
        "git push",
    ]
)
