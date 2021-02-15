#!/usr/bin/python3

import os

from common.bash import execute_bash_script
from common.yaml import update_yaml_file

chart_name = os.environ["CHART_NAME"]
chart_version = os.environ["CHART_VERSION"]
feature_branch_name = os.environ["FEATURE_BRANCH_NAME"]

execute_bash_script(
    [
        "git config user.name github-actions",
        "git config user.email github-actions@github.com",
        f"git checkout {feature_branch_name}",
    ]
)

update_yaml_file(
    f"./overlay/development/kon/{chart_name}/{chart_name}.yaml",
    "spec.chart.spec.version",
    chart_version,
)

execute_bash_script(
    [
        "git add .",
        "git commit -m "
        f"'Update {chart_name} Helm chart to version {chart_version}'",
        "git push",
    ]
)
