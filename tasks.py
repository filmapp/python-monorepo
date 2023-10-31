import os
import tomllib
from collections import defaultdict
from typing import DefaultDict, Dict, List, Mapping

import yaml
from typer import Typer

app = Typer()


def _get_poetry_deps() -> Mapping[str, List[str]]:
    with open("pyproject.toml", "rb") as f:
        pp = tomllib.load(f)

    deps: DefaultDict[str, List[str]] = defaultdict(list)
    for group, group_value in pp["tool"]["poetry"]["group"].items():
        for _, dep_value in group_value["dependencies"].items():
            if not isinstance(dep_value, Dict):
                continue
            path: str | None = dep_value.get("path")
            if path is None:
                continue
            deps[group].append(path)
    return deps


def _get_workflow_trigger() -> Mapping[str, List[str]]:
    ret: Dict[str, List[str]] = {}
    for path in os.listdir(".github/workflows"):
        if not path.endswith(".yml"):
            continue
        with open(os.path.join(".github/workflows", path), "r") as f:
            wf = yaml.load(f, Loader=yaml.BaseLoader)
        pr = wf["on"].get("push")
        if not isinstance(pr, dict):
            continue
        paths = [p[:-3] for p in pr["paths"]]  # Remove suffix "/**"
        workflow_name = os.path.splitext(path)[0]
        ret[workflow_name] = paths
    return ret


@app.command()
def check_gh_workflow_triggers() -> None:
    deps = _get_poetry_deps()
    wfs = _get_workflow_trigger()

    no_wf_groups = set(deps.keys()) - set(wfs.keys())
    deps_not_in_path: Dict[str, List[str]] = {}
    for group, dep_paths in deps.items():
        if group in no_wf_groups:
            continue
        grp = set(dep_paths) - set(wfs[group])
        if deps.get("dev"):
            dev = set(deps["get"]) - set(wfs[group])
        else:
            dev = set()
        dps = list(grp.union(dev))
        if dps:
            deps_not_in_path[group] = list(dps)

    no_wf_groups -= {"dev", "train"}
    if not no_wf_groups and not deps_not_in_path:
        print("all good")
        return

    if no_wf_groups:
        print(f"groups having no github actions workflow: {list(no_wf_groups)}")
    if deps_not_in_path:
        print(
            f"dependencies not in workflow's event trigger push paths: {deps_not_in_path}"
        )
    exit(1)


if __name__ == "__main__":
    app()
