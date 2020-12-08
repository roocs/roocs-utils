#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Console script for roocs_utils.inventory package."""
import argparse
import os
import shutil
import sys

from roocs_utils import CONFIG
from roocs_utils.inventory import logging
from roocs_utils.inventory.batch import BatchManager
from roocs_utils.inventory.inventory import to_yaml
from roocs_utils.inventory.task import TaskManager
from roocs_utils.inventory.utils import get_pickle_store

LOGGER = logging.getLogger(__file__)


def _get_arg_parser_run(parser):

    parser.add_argument(
        "-p",
        "--project",
        type=str,
        required=True,
        help="Project to scan datasets for.",
    )

    parser.add_argument(
        "-b",
        "--batches",
        type=str,
        default="all",
        required=False,
        help="Batches to run, default is 'all'. Also accepts comma separated "
        "list of batch numbers and/or ranges specified with a hyphen. E.g: "
        "'1,2,3' or '1-5'.",
    )

    parser.add_argument(
        "-d",
        "--datasets",
        type=str,
        default=None,
        required=False,
        help="Datasets to run. Also accepts comma separated "
        "list of datasets. E.g.: -d cmip6...gn.v20190910,cmip6...v20200202",
    )

    parser.add_argument(
        "-r",
        "--run-mode",
        type=str,
        default="local",
        required=False,
        help="Mode to run in, either 'lotus' (default) or 'local'.",
    )

    return parser


def _range_to_list(range_string, sep):
    start, end = [int(_) for _ in range_string.split(sep)]
    return list(range(start, end + 1))


def parse_args_run(args):
    # Parse batches into a single value
    batches = args.batches
    datasets = args.datasets

    if batches == "all":
        batches = None
    else:
        items = batches.split(",")
        batches = []

        for item in items:
            if "-" in item:
                batches.extend(_range_to_list(item, "-"))
            else:
                batches.append(int(item))

        batches = sorted(list(set(batches)))

    if datasets:
        datasets = datasets.split(",")

    return args.project, batches, datasets, args.run_mode


def run_main(args):
    project, batches, datasets, run_mode = parse_args_run(args)

    tm = TaskManager(project, batches=batches, datasets=datasets, run_mode=run_mode)
    tm.run_tasks()


def _get_arg_parser_project(parser):

    parser.add_argument(
        "-p",
        "--project",
        type=str,
        required=True,
        help="Project name",
    )

    return parser


def parse_args_project(args):
    return args.project


def create_main(args):
    project = parse_args_project(args)
    bm = BatchManager(project)
    bm.create_batches()


def _get_arg_parser_clean(parser):

    parser.add_argument(
        "-p",
        "--project",
        type=str,
        required=True,
        help="Project to clean out directories for.",
    )

    parser.add_argument(
        "-D",
        "--delete-objects",
        action="store_true",
        help="Delete all the objects in the Object Store - DANGER!!!",
    )

    parser.add_argument(
        "-b",
        "--buckets",
        default=[],
        nargs="*",
        help="Identifiers of buckets TO DELETE!",
    )

    return parser


def parse_args_clean(args):
    return args.project, args.delete_objects, args.buckets


def clean_main(args):
    project, delete_objects, buckets_to_delete = parse_args_clean(args)

    if delete_objects:
        resp = input("DO YOU REALLY WANT TO DELETE THE BUCKETS? [Y/N] ")
        if resp != "Y":
            print("Exiting.")
            sys.exit()

    batch_dir = BatchManager(project)._version_dir
    log_dir = os.path.join(CONFIG["log"]["log_base_dir"], project)
    to_delete = [log_dir, batch_dir]

    for dr in to_delete:
        if os.path.isdir(dr):
            LOGGER.warning(f"Deleting: {dr}")
            shutil.rmtree(dr)

    lock_files = [
        f"{value}.lock"
        for key, value in CONFIG[f"project:{project}"].items()
        if key.endswith("_pickle")
    ]

    for lock_file in lock_files:
        if os.path.isfile(lock_file):
            LOGGER.warning(f"Deleting: {lock_file}")
            os.remove(lock_file)

    if buckets_to_delete:
        LOGGER.warning("Starting to delete buckets from Object Store!")
        caringo_store = CaringoStore(creds=get_credentials())

        for bucket in buckets_to_delete:
            LOGGER.warning(f"DELETING BUCKET: {bucket}")
            caringo_store.delete(bucket)


def _get_arg_parser_list(parser):

    parser.add_argument(
        "-p",
        "--project",
        type=str,
        required=True,
        help="Project to list.",
    )

    parser.add_argument(
        "-c",
        "--count-only",
        action="store_true",
        help="Only show the total count of records processed.",
    )

    return parser


def parse_args_list(args):
    return args.project, args.count_only


def list_main(args):
    project, count_only = parse_args_list(args)
    pstore = get_pickle_store("inventory", project)
    records = pstore.read().items()

    if not count_only:
        for dataset_id, content in records:
            print(f"Record: {dataset_id}, {content}")

    print(f"\nTotal records: {len(records)}")


def _get_arg_parser_write(parser):

    parser.add_argument(
        "-p",
        "--project",
        type=str,
        required=True,
        help="Project to write inventory for.",
    )

    parser.add_argument(
        "-v",
        "--version",
        default="files",
        help="Version of inventory to write, either 'files' (default - with file names) "
        "or 'c3s' (without file names).",
    )

    return parser


def parse_args_write(args):
    return args.project, args.version


def write_main(args):
    project, version = parse_args_write(args)
    pstore = get_pickle_store("inventory", project)
    records = pstore.read().items()

    if version == "c3s":
        inv_file = CONFIG[f"project:{project}"]["c3s_inventory_file"]

        for dataset_id, content in records:
            del content["files"]
            to_yaml([content], project, version)

    else:
        inv_file = CONFIG[f"project:{project}"]["full_inventory_file"]

        for dataset_id, content in records:
            to_yaml([content], project, version)

    print(f"Inventory written: {inv_file}")


def show_errors_main(args):
    project = parse_args_project(args)
    error_pstore = get_pickle_store("error", project)

    errors = error_pstore.read().items()

    for dataset_id, error in errors:
        print("\n===================================================")
        print(f"{dataset_id}:")
        print("===================================================\n")
        print("\t" + error)

    print(f"\nFound {len(errors)} errors.")


def main():
    """Console script for roocs_utils.inventory package"""
    main_parser = argparse.ArgumentParser()
    main_parser.set_defaults(func=lambda args: main_parser.print_help())
    subparsers = main_parser.add_subparsers()

    run_parser = subparsers.add_parser("run")
    _get_arg_parser_run(run_parser)
    run_parser.set_defaults(func=run_main)

    create_parser = subparsers.add_parser("create-batches")
    _get_arg_parser_project(create_parser)
    create_parser.set_defaults(func=create_main)

    clean_parser = subparsers.add_parser("clean")
    _get_arg_parser_clean(clean_parser)
    clean_parser.set_defaults(func=clean_main)

    list_parser = subparsers.add_parser("list")
    _get_arg_parser_list(list_parser)
    list_parser.set_defaults(func=list_main)

    write_parser = subparsers.add_parser("write")
    _get_arg_parser_write(write_parser)
    write_parser.set_defaults(func=write_main)

    show_errors_parser = subparsers.add_parser("show-errors")
    _get_arg_parser_project(show_errors_parser)
    show_errors_parser.set_defaults(func=show_errors_main)

    args = main_parser.parse_args()
    args.func(args)


if __name__ == "__main__":

    sys.exit(main())  # pragma: no cover
