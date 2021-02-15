#!/usr/bin/python3

import os

from common.bash import execute_bash_script
from common.yaml import update_yaml_file, get_yaml_file_field_value

feature_branch_name = os.environ["FEATURE_BRANCH"]
chart_names = ["alpi", "hasura", "hasura-metadata", "nami", "zoru"]
chart_version_yaml_field_path = "spec.chart.spec.version"

execute_bash_script(
    [
        "git config user.name github-actions",
        "git config user.email github-actions@github.com",
        f"git checkout {feature_branch_name}",
    ]
)

chart_versions = []
for chart_name in chart_names:
    chart_version = get_yaml_file_field_value(
        f"./overlay/development/kon/{chart_name}/{chart_name}.yaml",
        chart_version_yaml_field_path,
    )
    chart_versions.append(chart_version)

execute_bash_script(
    [
        "git checkout main",
    ]
)

for i, chart_name in enumerate(chart_names):
    update_yaml_file(
        f"./overlay/development/kon/{chart_name}/{chart_name}.yaml",
        chart_version_yaml_field_path,
        chart_versions[i],
    )

promotion_message = ",".join(
    list(
        map(
            lambda chart_name, chart_version: f"{chart_name}-{chart_version}",
            chart_names,
            chart_version,
        )
    )
)
execute_bash_script(
    [
        "git add .",
        "git commit -m 'Promote Helm packages {promotion_message}'",
        "git push",
    ]
)

execute_bash_script([f"git push origin --delete {feature_branch_name}"])
