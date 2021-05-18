#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Console script for roocs_utils.catalog_maker package."""
import argparse
import os
import shutil
import sys

from roocs_utils import CONFIG
from roocs_utils.catalog_maker import logging
from roocs_utils.catalog_maker.batch import BatchManager
from roocs_utils.catalog_maker.catalog import to_csv
from roocs_utils.catalog_maker.catalog import update_catalog
from roocs_utils.catalog_maker.database import DataBaseHandler
from roocs_utils.catalog_maker.task import TaskManager
from roocs_utils.project_utils import derive_ds_id

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
        help="Project to clean out records for.",
    )

    return parser


def parse_args_clean(args):
    return args.project


def clean_main(args):
    project = parse_args_clean(args)

    rh = DataBaseHandler(table_name=f"{project.replace('-', '_')}_catalog_results")
    rh.delete_all_results()

    print(f"All records in the {project} catalog's abcunit database have been deleted.")


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

    rh = DataBaseHandler(table_name=f"{project.replace('-', '_')}_catalog_results")
    fpaths = rh.get_successful_runs()

    datasets = rh.get_successful_datasets()

    if not count_only:
        for fpath in fpaths:
            content = rh.get_content(fpath)
            print(f"Record: {fpath}, {content}")

    print(f"\nTotal successful files scanned: {rh.count_successes()}")
    print(f"\nTotal successful datasets scanned: {len(datasets)}")

    print(f"\nTotal results (including errors): {rh.count_results()}")
    print(f"\nTotal datasets (including errors): {len(rh.get_all_datasets())}")


def _get_arg_parser_write(parser):

    parser.add_argument(
        "-p",
        "--project",
        type=str,
        required=True,
        help="Project to write catalog for.",
    )

    return parser


def parse_args_write(args):
    return args.project


def write_main(args):
    project = parse_args_write(args)

    rh = DataBaseHandler(table_name=f"{project.replace('-', '_')}_catalog_results")

    entries = rh.get_all_content()

    path, last_updated = to_csv(entries, project)

    cat_dir = CONFIG[f"project:{project}"]["catalog_dir"]
    cat_path = update_catalog(project, path, last_updated, cat_dir)
    print(f"Intake Catalog updated: {cat_path}")


def show_errors_main(args):
    project, count_only = parse_args_list(args)

    rh = DataBaseHandler(table_name=f"{project.replace('-', '_')}_catalog_results")
    failures_lists = list(rh.get_failed_runs().values())
    failures_fpaths = [item for sublist in failures_lists for item in sublist]

    errors = dict()

    if not count_only:
        for fpath in failures_fpaths:
            errors[fpath] = rh.get_error_traceback(fpath)

        for fpath, error in errors.items():
            ds_id = derive_ds_id(fpath)
            print("\n===================================================")
            print(f"{ds_id}")
            print(f"{fpath}")
            print("===================================================\n")
            print("\t" + error)

    print(f"\nTotal failed files: {rh.count_failures()}")
    print(f"\nTotal failed datasets: {len(rh.get_failed_datasets())}")

    print(
        f"\nFailed datasets that have been partially scanned: {rh.get_successful_datasets() & rh.get_failed_datasets()}"
    )


def main():
    """Console script for roocs_utils.catalog_maker package"""
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
    _get_arg_parser_list(show_errors_parser)
    show_errors_parser.set_defaults(func=show_errors_main)

    args = main_parser.parse_args()
    args.func(args)


if __name__ == "__main__":

    sys.exit(main())  # pragma: no cover
