#!/usr/bin/env python
import argparse
import glob
import os
import re
import time

from roocs_utils import CONFIG
from roocs_utils.inventory.inventory import _get_project_list
from roocs_utils.inventory.inventory import build_dict
from roocs_utils.inventory.inventory import to_yaml

output_dir = "/gws/smf/j04/cp4cds1/c3s_34e/inventory"
# output_dir = "/home/users/esmith88/roocs/inventory"
VERSION = re.compile(r"^v\d{8}$")
LIMIT = 1000000000


def arg_parse():
    parser = argparse.ArgumentParser()

    project_choices = _get_project_list()

    parser.add_argument(
        "-pr",
        "--project",
        type=str,
        choices=project_choices,
        required=True,
        help=f"Project, must be one of: {project_choices}",
    )
    parser.add_argument("-m", "--model", type=str, required=True)

    return parser.parse_args()


def write_inventory(project, model_inst, d, paths):

    base = d["base_dir"]
    header = {"project": project, "base_dir": base}

    records = [header] + [
        build_dict(_, d, base, project, model_inst) for _ in sorted(paths)
    ]
    name = f"{project}_{model_inst}"

    to_yaml(name, records)


def write_all(project, model_path):
    d = CONFIG[f"project:{project}"]

    start_dir = model_path
    model_inst = "_".join(model_path.split("/")[-3:-1])

    paths = []

    success_paths = glob.glob(f"{output_dir}/logs/success/{project}_{model_inst}_*.txt")
    recorded = []
    for path in success_paths:
        n = path.split("/")[-1].split(".")[0].split("_")[-1]
        recorded.append(n)

    if len(recorded) > 0:
        recorded = int(max(recorded))
    else:
        recorded = 0

    for item, _1, _2 in os.walk(start_dir):

        if VERSION.match(os.path.basename(item)):
            paths.append(item)

        if os.path.exists(
            f"{output_dir}/logs/success/{project}_{model_inst}-final.txt"
        ):
            print(
                f"[INFO] Already completed for {project}/{model_inst}. Success file found."
            )
            return

        if len(paths) <= recorded:
            continue

        if len(paths) > LIMIT:
            error_output_path = f"{output_dir}/logs/errors"

            # make output directory
            if not os.path.exists(error_output_path):
                os.makedirs(error_output_path)

            with open(
                os.path.join(error_output_path, f"{project}_{model_inst}.txt"), "a"
            ) as f:
                f.write(f"\n[ERROR] Reached dataset limit")

            break

        if len(paths) > 0 and len(paths) % 100 == 0:
            write_inventory(project, model_inst, d, paths[recorded:])
            print(f"[INFO] Written so far: {len(paths)}")

            recorded += 100

            success_output_path = f"{output_dir}/logs/success"

            # make output directory
            if not os.path.exists(success_output_path):
                os.makedirs(success_output_path)

            open(
                os.path.join(
                    success_output_path, f"{project}_{model_inst}_{len(paths)}.txt"
                ),
                "w",
            )

    time.sleep(1)
    write_inventory(project, model_inst, d, paths[recorded:])

    success_output_path = f"{output_dir}/logs/success"

    # make output directory
    if not os.path.exists(success_output_path):
        os.makedirs(success_output_path)

    open(os.path.join(success_output_path, f"{project}_{model_inst}-final.txt"), "w")


if __name__ == "__main__":

    args = arg_parse()
    write_all(args.project, args.model)
