"""Main module."""
import yaml
from pathlib import Path

import re
import os
import sys
import click
import pathlib
import json
import logging
import pathlib

from datetime import datetime
from typing import Any, Dict
from rich.console import Console
from rich.logging import RichHandler

from rich import print as rprint

SHOW_DETAILS = True

DEFAULT_OUTDIR = os.path.join(
    '/tmp/',
    os.path.splitext(os.path.basename(__file__))[0],
    str(datetime.today().strftime('%Y-%m-%d-%H%M%S'))
)

DEFAULT_CONFIG_FILE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    'conf',
    'config.yaml'
)


DEFAULT_LOGGING_FORMAT = "%(levelname)s : %(asctime)s : %(pathname)s : %(lineno)d : %(message)s"

DEFAULT_LOGGING_LEVEL = logging.INFO

DEFAULT_VERBOSE = True

error_console = Console(stderr=True, style="bold red")

console = Console()

ignore_dirpath_lookup = {}

ignore_subdir_lookup = {}

subdir_is_optional_lookup = {}


def check_directories(config_dirnames_lookup, dirpath, dirnames) -> None:
    logging.info(f"Will attempt to search for expected subdirectories in directory '{dirpath}'")
    found_dirname_list = []
    found_dirname_lookup = {}

    missing_dirname_list = []
    missing_dirname_lookup = {}

    found_ctr = 0
    missing_ctr = 0

    pattern_found_ctr_lookup = {}
    pattern_found_ctr = 0

    pattern_missing_ctr_lookup = {}
    pattern_missing_ctr = 0

    # config_dirnames_lookup = config["dirnames"]

    expected_ctr = 0

    exact_match_type_ctr = 0 # tally number of exact match types
    exact_match_found_ctr = 0
    exact_match_missing_ctr = 0
    exact_match_found_list = []
    exact_match_missing_list = []

    min_expected_pattern_ctr = 0
    max_expected_pattern_ctr = 0

    pattern_match_type_ctr = 0 # tally number of pattern match types
    pattern_match_found_ctr = 0
    pattern_match_missing_ctr = 0

    pattern_match_type_lookup = {}

    for config_dirname, config_dirname_lookup in config_dirnames_lookup.items():
        expected_ctr += 1

        # logging.info(f"config_dirname '{config_dirname}'")

        if "exact_match" in config_dirname_lookup and config_dirname_lookup["exact_match"]:
            exact_match_type_ctr += 1
            logging.info(f"Check {expected_ctr}. for subdirectory '{config_dirname}' based on exact match")
            full_subdir = os.path.join(dirpath, config_dirname)
            if config_dirname in dirnames:
                found_dirname_list.append(full_subdir)
                found_dirname_lookup[full_subdir] = True
                found_ctr += 1

                exact_match_found_list.append(full_subdir)
                exact_match_found_ctr += 1
            else:
                if not is_subdir_optional(config_dirname, config_dirname_lookup):
                    missing_dirname_list.append(full_subdir)
                    missing_dirname_lookup[full_subdir] = True
                    missing_ctr += 1

                    exact_match_missing_list.append(full_subdir)
                    exact_match_missing_ctr += 1
            continue

        elif "pattern_match" in config_dirname_lookup:
            pattern_match_type_ctr += 1
            pattern = config_dirname_lookup["pattern_match"]
            logging.info(f"Check {expected_ctr}. for subdirectory like '{config_dirname}' based on regex pattern '{pattern}'")

            compiled_pattern = re.compile(pattern)

            if pattern not in pattern_match_type_lookup:
                pattern_match_type_lookup[pattern] = {}

            if "found_list" not in pattern_match_type_lookup[pattern]:
                pattern_match_type_lookup[pattern]["found_list"] = []

            if "found_ctr" not in pattern_match_type_lookup[pattern]:
                pattern_match_type_lookup[pattern]["found_ctr"] = 0

            if "missing_list" not in pattern_match_type_lookup[pattern]:
                pattern_match_type_lookup[pattern]["missing_list"] = []

            if "missing_ctr" not in pattern_match_type_lookup[pattern]:
                pattern_match_type_lookup[pattern]["missing_ctr"] = 0


            if "exact_count" in config_dirname_lookup:
                pattern_match_type_lookup[pattern]["exact_count"] = config_dirname_lookup["exact_count"]
                # expected_ctr += config_dirname_lookup["exact_count"]
            else:
                if "min_count" in config_dirname_lookup:
                    # min_expected_pattern_ctr += config_dirname_lookup["min_count"]
                    pattern_match_type_lookup[pattern]["min_count"] = config_dirname_lookup["min_count"]

                if "max_count" in config_dirname_lookup:
                    # max_expected_pattern_ctr += config_dirname_lookup["max_count"]
                    pattern_match_type_lookup[pattern]["max_count"] = config_dirname_lookup["max_count"]


            # print(f"checking for pattern match")

            for dirname in dirnames:
                # if dirname in found_dirname_lookup or dirname in missing_dirname_lookup:
                #     continue
                if re.search(compiled_pattern, dirname):
                    full_subdir = os.path.join(dirpath, dirname)
                    found_dirname_list.append(full_subdir)

                    pattern_match_type_lookup[pattern]["found_list"].append(full_subdir)
                    pattern_match_type_lookup[pattern]["found_ctr"] += 1

                    # found_dirname_lookup[full_subdir] = True
                    found_ctr += 1

                    if pattern not in pattern_found_ctr_lookup:
                        pattern_found_ctr_lookup[pattern] = 0
                    pattern_found_ctr_lookup[pattern] += 1
                    pattern_found_ctr += 1

                    # pattern_found_lookup[os.path.join(dirpath, dirname)] = True
                    # pattern_found_ctr += 1
                    # break
            if pattern_match_type_lookup[pattern]["found_ctr"] == 0:

                # Check if the directory was optional
                if os.path.basename(dirpath) not in subdir_is_optional_lookup:
                    logging.info(f"Did not find subdirectory based on regex pattern search but the directory '{dirpath}' is optional")
                    continue

                full_subdir = os.path.join(dirpath, dirname)

                missing_dirname_list.append(full_subdir)
                missing_dirname_lookup[full_subdir] = True
                missing_ctr += 1

                pattern_match_type_lookup[pattern]["missing_list"].append(full_subdir)
                pattern_match_type_lookup[pattern]["missing_ctr"] += 1

                if pattern not in pattern_missing_ctr_lookup:
                    pattern_missing_ctr_lookup[pattern] = 0
                pattern_missing_ctr_lookup[pattern] += 1

                pattern_missing_ctr += 1
                break

    generate_exact_match_report(
        exact_match_type_ctr,
        exact_match_found_ctr,
        exact_match_found_list,
        exact_match_missing_ctr,
        exact_match_missing_list,
        "subdirectories",
        dirpath
    )


    generate_pattern_match_report(
        pattern_match_type_ctr,
        pattern_match_type_lookup,
        "subdirectories",
        dirpath
    )

    # if exact_match_type_ctr > 0:
    #     print(f"\n\nExpected to find '{exact_match_type_ctr}' exact match subdirectories")
    #     if exact_match_found_ctr > 0:
    #         print(f"Found the following '{exact_match_found_ctr}' exact match subdirectories")
    #         for found in exact_match_found_list:
    #             print(found)
    #     if exact_match_missing_ctr > 0:
    #         print(f"Did not find the following '{exact_match_missing_ctr}' exact match subdirectories")
    #         for missing in exact_match_missing_list:
    #             print(missing)

    # if pattern_match_type_ctr > 0:
    #     print(f"\n\nExpected to find at least '{pattern_match_type_ctr}' pattern match subdirectories")
    #     for pattern in pattern_match_type_lookup:
    #         found_ctr = pattern_match_type_lookup[pattern].get("found_ctr", 0)
    #         missing_ctr = pattern_match_type_lookup[pattern].get("missing_ctr", 0)
    #         min_count = pattern_match_type_lookup[pattern]["min_count"]
    #         max_count = pattern_match_type_lookup[pattern]["max_count"]
    #         print(f"For pattern '{pattern}' expected between '{min_count}' and '{max_count}' subdirectories")
    #         if found_ctr > 0:
    #             print(f"Found the following '{found_ctr}' subdirectories")
    #             for found in pattern_match_type_lookup[pattern]["found_list"]:
    #                 print(found)
    #         if missing_ctr > 0:
    #             print(f"Did not find any subdirectories matching this pattern")




def check_files(config_filenames_lookup, dirpath, filenames, is_optional) -> None:
    logging.info(f"Will attempt to search for expected files in subdirectory '{dirpath}'")
    found_filename_list = []
    found_filename_lookup = {}

    missing_filename_list = []
    missing_filename_lookup = {}

    found_ctr = 0
    missing_ctr = 0

    pattern_found_ctr_lookup = {}
    pattern_found_ctr = 0

    pattern_missing_ctr_lookup = {}
    pattern_missing_ctr = 0

    # config_filenames_lookup = config["filenames"]

    expected_ctr = 0

    exact_match_type_ctr = 0 # tally number of exact match types
    exact_match_found_ctr = 0
    exact_match_missing_ctr = 0
    exact_match_found_list = []
    exact_match_missing_list = []

    min_expected_pattern_ctr = 0
    max_expected_pattern_ctr = 0

    pattern_match_type_ctr = 0 # tally number of pattern match types
    pattern_match_found_ctr = 0
    pattern_match_missing_ctr = 0

    pattern_match_type_lookup = {}

    for config_filename, config_filename_lookup in config_filenames_lookup.items():
        expected_ctr += 1

        # logging.info(f"config_filename '{config_filename}'")

        if "exact_match" in config_filename_lookup and config_filename_lookup["exact_match"]:
            exact_match_type_ctr += 1
            logging.info(f"Check {expected_ctr}. for file '{config_filename}' based on exact match")
            full_subdir = os.path.join(dirpath, config_filename)
            if config_filename in filenames:
                found_filename_list.append(full_subdir)
                found_filename_lookup[full_subdir] = True
                found_ctr += 1

                exact_match_found_list.append(full_subdir)
                exact_match_found_ctr += 1
            else:
                missing_filename_list.append(full_subdir)
                missing_filename_lookup[full_subdir] = True
                missing_ctr += 1

                exact_match_missing_list.append(full_subdir)
                exact_match_missing_ctr += 1
            continue

        elif "pattern_match" in config_filename_lookup:
            pattern_match_type_ctr += 1
            pattern = config_filename_lookup["pattern_match"]
            logging.info(f"Check {expected_ctr}. for file like '{config_filename}' based on regex pattern '{pattern}'")

            compiled_pattern = re.compile(pattern)

            if pattern not in pattern_match_type_lookup:
                pattern_match_type_lookup[pattern] = {}

            if "found_list" not in pattern_match_type_lookup[pattern]:
                pattern_match_type_lookup[pattern]["found_list"] = []

            if "found_ctr" not in pattern_match_type_lookup[pattern]:
                pattern_match_type_lookup[pattern]["found_ctr"] = 0

            if "missing_list" not in pattern_match_type_lookup[pattern]:
                pattern_match_type_lookup[pattern]["missing_list"] = []

            if "missing_ctr" not in pattern_match_type_lookup[pattern]:
                pattern_match_type_lookup[pattern]["missing_ctr"] = 0

            if "exact_count" in config_filename_lookup:
                pattern_match_type_lookup[pattern]["exact_count"] = config_filename_lookup["exact_count"]
                # expected_ctr += config_filename_lookup["exact_count"]
            else:
                if "min_count" in config_filename_lookup:
                    # min_expected_pattern_ctr += config_filename_lookup["min_count"]
                    pattern_match_type_lookup[pattern]["min_count"] = config_filename_lookup["min_count"]

                if "max_count" in config_filename_lookup:
                    # max_expected_pattern_ctr += config_filename_lookup["max_count"]
                    pattern_match_type_lookup[pattern]["max_count"] = config_filename_lookup["max_count"]


            # print(f"checking for pattern match")

            for filename in filenames:
                # if filename in found_filename_lookup or filename in missing_filename_lookup:
                #     continue
                if re.search(compiled_pattern, filename):
                    full_subdir = os.path.join(dirpath, filename)
                    found_filename_list.append(full_subdir)

                    pattern_match_type_lookup[pattern]["found_list"].append(full_subdir)
                    pattern_match_type_lookup[pattern]["found_ctr"] += 1

                    # found_filename_lookup[full_subdir] = True
                    found_ctr += 1

                    if pattern not in pattern_found_ctr_lookup:
                        pattern_found_ctr_lookup[pattern] = 0
                    pattern_found_ctr_lookup[pattern] += 1
                    pattern_found_ctr += 1

                    # pattern_found_lookup[os.path.join(dirpath, filename)] = True
                    # pattern_found_ctr += 1
                    # break

            if pattern_match_type_lookup[pattern]["found_ctr"] == 0:

                # Check if the directory was optional
                if is_optional or os.path.basename(dirpath) not in subdir_is_optional_lookup:
                    logging.info(f"Did not find file based on regex pattern search but the directory '{dirpath}' is optional")
                    continue

                full_subdir = os.path.join(dirpath, filename)

                missing_filename_list.append(full_subdir)
                missing_filename_lookup[full_subdir] = True
                missing_ctr += 1

                pattern_match_type_lookup[pattern]["missing_list"].append(full_subdir)
                pattern_match_type_lookup[pattern]["missing_ctr"] += 1

                if pattern not in pattern_missing_ctr_lookup:
                    pattern_missing_ctr_lookup[pattern] = 0
                pattern_missing_ctr_lookup[pattern] += 1

                pattern_missing_ctr += 1
                # break

    if exact_match_type_ctr > 0:
        generate_exact_match_report(
            exact_match_type_ctr,
            exact_match_found_ctr,
            exact_match_found_list,
            exact_match_missing_ctr,
            exact_match_missing_list,
            "files",
            dirpath
        )
    else:
        logging.info(f"Based on the configuration, there were no exact match search types for files to be performed for directory '{dirpath}'")

    if pattern_match_type_ctr > 0:
        generate_pattern_match_report(
            pattern_match_type_ctr,
            pattern_match_type_lookup,
            "files",
            dirpath
        )
    else:
        logging.info(f"Based on the configuration, there were no regex pattern match search types for subdirectories to be performed for directory '{dirpath}'")



def generate_exact_match_report(
        exact_match_type_ctr,
        exact_match_found_ctr,
        exact_match_found_list,
        exact_match_missing_ctr,
        exact_match_missing_list,
        type,
        dirpath
    ) -> None:
    logging.info(f"Here is the exact match report for '{type}' in directory '{dirpath}'")
    if exact_match_type_ctr == 0:
        # rprint("[bold red]There were no exact match types for '{type}' in subdirectory '{dirpath}'[/]")
        logging.info("[bold red]There were no exact match types for '{type}' in subdirectory '{dirpath}'[/]")
        return

    logging.info(f"\n\nExpected to find '{exact_match_type_ctr}' exact match '{type}' in subdirectory '{dirpath}'")

    if exact_match_found_ctr > 0:
        logging.info(f"Found the following '{exact_match_found_ctr}' exact match '{type}' in subdirectory '{dirpath}'")
        for i, found in enumerate(exact_match_found_list, start=1):
            logging.info(f"{i}. {found}")

    if exact_match_missing_ctr > 0:
        rprint(f"[bold red]Did not find the following '{exact_match_missing_ctr}' exact match '{type}' in subdirectory '{dirpath}'[/]")
        logging.error(f"Did not find the following '{exact_match_missing_ctr}' exact match '{type}' in subdirectory '{dirpath}'")
        for i, missing in enumerate(exact_match_missing_list, start=1):
            rprint(f"[bold red]{i}. {missing}[/]")
            logging.error(f"{i}. {missing}")


def generate_pattern_match_report(pattern_match_type_ctr, pattern_match_type_lookup, type, dirpath) -> None:
    logging.info(f"Here is the pattern match report for '{type}' in directory '{dirpath}'")

    if pattern_match_type_ctr == 0:
        # rprint(f"[bold red]There were no pattern match types for '{type}' in subdirectory in subdirectory '{dirpath}'[/]")
        logging.info(f"There were no regex pattern match searches for '{type}' in subdirectory in subdirectory '{dirpath}'")
        return

    logging.info(f"\n\nExpect to find at least '{pattern_match_type_ctr}' file matches based on regex pattern search in subdirectory '{dirpath}'")

    for pattern in pattern_match_type_lookup:

        found_ctr = pattern_match_type_lookup[pattern].get("found_ctr", 0)
        missing_ctr = pattern_match_type_lookup[pattern].get("missing_ctr", 0)

        if "exact_count" in pattern_match_type_lookup[pattern]:
            exact_count = pattern_match_type_lookup[pattern]["exact_count"]
            logging.info(f"For pattern '{pattern}' expected exactly '{exact_count}' '{type}' in subdirectory '{dirpath}'")
        elif "min_count" in pattern_match_type_lookup[pattern]:
            min_count = pattern_match_type_lookup[pattern]["min_count"]
            max_count = pattern_match_type_lookup[pattern]["max_count"]
            logging.info(f"For pattern '{pattern}' expected between '{min_count}' and '{max_count}' '{type}' in subdirectory '{dirpath}'")

        if found_ctr > 0:
            logging.info(f"Found the following '{found_ctr}' '{type}' in subdirectory '{dirpath}'")
            for found in pattern_match_type_lookup[pattern]["found_list"]:
                logging.info(found)

        if missing_ctr > 0:
            rprint(f"[bold red]Did not find any '{type}' matching pattern '{pattern}' in subdirectory '{dirpath}'[/]")
            logging.error(f"Did not find any '{type}' matching pattern '{pattern}' in subdirectory '{dirpath}'")


    # if min_expected_pattern_ctr == 0:
    #     print(f"\n\nTotal number of expected subdirectories for '{dirpath}' is '{expected_ctr}'")
    # else:
    #     min_expected_pattern_ctr += expected_ctr - pattern_match_type_ctr
    #     max_expected_pattern_ctr += expected_ctr - pattern_match_type_ctr
    #     print(f"\n\nTotal number of expected subdirectories for '{dirpath}' is betweeen '{min_expected_pattern_ctr}' and '{max_expected_pattern_ctr}'")


    # if found_ctr > 0:
    #     print(f"Found the following '{found_ctr}' subdirectories:")
    #     for found in found_dirname_lookup:
    #         print(found)

    # if missing_ctr > 0:
    #     print(f"Did not find the following '{missing_ctr}' expected subdirectories:")
    #     for missing in missing_dirname_lookup:
    #         print(missing)

    # if pattern_found_ctr > 0:
    #     print(f"The following '{pattern_found_ctr}' pattern-based matches were made:")
    #     for pattern, count in pattern_found_ctr_lookup.items():
    #         print(f"Found the following '{count}' subdirectories with this pattern '{pattern}'")

    # if pattern_missing_ctr > 0:
    #     print(f"The following '{pattern_missing_ctr}' pattern-based matches were not made:")
    #     for pattern, count in pattern_missing_ctr_lookup.items():
    #         print(f"Did not find '{count}' subdirectories with this pattern '{pattern}'")


def check_files_v1(config_filenames_lookup, dirpath, filenames) -> None:

    found_filename_list = []
    found_filename_lookup = {}

    missing_filename_list = []
    missing_filename_lookup = {}

    found_ctr = 0
    missing_ctr = 0

    pattern_found_ctr_lookup = {}
    pattern_found_ctr = 0

    pattern_missing_ctr_lookup = {}
    pattern_missing_ctr = 0

    # config_filenames_lookup = config["filenames"]

    expected_ctr = 0
    for config_filename, config_filename_lookup in config_filenames_lookup.items():
        expected_ctr += 1

        # print(f"config_filename '{config_filename}'")

        if "exact_match" in config_filename_lookup and config_filename_lookup["exact_match"]:
            logging.info(f"checking for exact match")
            full_subdir = os.path.join(dirpath, config_filename)
            if config_filename in filenames:
                found_filename_list.append(full_subdir)
                found_filename_lookup[full_subdir] = True
                found_ctr += 1
            else:
                missing_filename_list.append(full_subdir)
                missing_filename_lookup[full_subdir] = True
                missing_ctr += 1
            continue

        elif "pattern_match" in config_filename_lookup:

            logging.info(f"checking for pattern match")

            for filename in filenames:
                if filename in found_filename_lookup or filename in missing_filename_lookup:
                    continue
                pattern = re.compile(config_filename_lookup["pattern_match"])
                if re.search(pattern, filename):
                    full_subdir = os.path.join(dirpath, filename)
                    found_filename_list.append(full_subdir)
                    found_filename_lookup[full_subdir] = True
                    found_ctr += 1

                    if pattern not in pattern_found_ctr_lookup:
                        pattern_found_ctr_lookup[pattern] = 0
                    pattern_found_ctr_lookup[pattern] += 1
                    pattern_found_ctr += 1

                    # pattern_found_lookup[os.path.join(dirpath, filename)] = True
                    # pattern_found_ctr += 1
                    break
            else:
                full_subdir = os.path.join(dirpath, filename)

                missing_filename_list.append(full_subdir)
                missing_filename_lookup[full_subdir] = True
                missing_ctr += 1

                if pattern not in pattern_missing_ctr_lookup:
                    pattern_missing_ctr_lookup[pattern] = 0
                pattern_missing_ctr_lookup[pattern] += 1

                pattern_missing_ctr += 1
                break

    print(f"\n\nTotal number of expected files for '{dirpath}' is '{expected_ctr}'")

    if found_ctr > 0:
        print(f"Found the following '{found_ctr}' files:")
        for found in found_filename_lookup:
            print(found)

    if missing_ctr > 0:
        print(f"Did not find the following '{missing_ctr}' expected files:")
        for missing in missing_filename_lookup:
            print(missing)

    if pattern_found_ctr > 0:
        print(f"The following '{pattern_found_ctr}' pattern-based matches were made:")
        for pattern, count in pattern_found_ctr_lookup.items():
            print(f"Found the following '{count}' files with this pattern '{pattern}'")

    if pattern_missing_ctr > 0:
        print(f"The following '{pattern_missing_ctr}' pattern-based matches were not made:")
        for pattern, count in pattern_missing_ctr_lookup.items():
            print(f"Did not find '{count}' files with this pattern '{pattern}'")


def profile_data_directory(config: Dict[str, Any], indir: str = None, extension: str = None) -> list:
    """Get the list of files in the specified directory
    :param indir: {str} - the directory to search for files
    :param extension: {str} - the file extension to filter on
    :returns file_list: {list} - the list of files found in the directory
    """
    indir = indir.rstrip("/")
    if extension is None:
        logging.info(f"Going to search for files in directory '{indir}'")
    else:
        logging.info(f"Going to search for files with extension '{extension}' in directory '{indir}'")

    file_list = []
    resources_dir = os.path.join(indir, "resources")
    # resources_dir = os.path.join(indir, "resources", ".git")

    # found_filename_list = []
    # found_filename_lookup = {}
    # missing_filename_list = []
    # missing_filename_lookup = {}

    dir_lookup = {}
    for dirpath, dirnames, filenames in os.walk(indir):

        if dirpath.startswith(resources_dir):
            # print(f"Going to skip subdirectory '{dirpath}'")
            continue

        dirpath = dirpath.rstrip("/")
        dir_lookup[dirpath] = {"dirnames": dirnames, "filenames": filenames}

        if False:
            logging.info(f"dirpath: {dirpath}")
            logging.info(f"dirnames: {dirnames}")
            logging.info(f"filenames: {filenames}")
            logging.info("****************************")

    config_dirnames = config["graph"]["dirnames"]
    config_filenames = config["graph"]["filenames"]
    is_optional = False

    process_directory(
        indir,
        config_dirnames,
        config_filenames,
        dir_lookup,
        is_optional,
        config
    )

    if False:
        if indir == dirpath:
            # Initial condition: we start at the top-level directory.
            check_directories(config_dirnames, dirpath, dirnames)
            check_files(config_filenames, dirpath, filenames)
        else:
            # For each directory, process each subdirectory
            for config_dirname in config_dirnames:
                config_dirpath = os.path.join()
                # check_directories(config["dirnames"], dirpath, dirnames)
                # check_files(config["filenames"], dirpath, filenames

def get_object_count(lookup) -> int:
    ctr = 0
    if lookup is not None:
        for item in lookup:
            ctr += 1
    return ctr


def ignore_dir(dirpath: str) -> bool:
    if dirpath in ignore_dirpath_lookup:
        logging.info(f"Will ignore dirpath '{dirpath}'")
        return True
    elif os.path.basename(dirpath) in ignore_subdir_lookup:
        logging.info(f"Will ignore subdirectory '{os.path.basename(dirpath)}' in dirpath '{dirpath}'")
        return True
    return False


def process_files_in_directory(dirpath, config_filenames, dir_lookup, is_optional) -> None:
    logging.info(f"Will attempt to process files in directory '{dirpath}'")

    relevant_count = get_object_count(config_filenames)
    if relevant_count == 0:
        logging.info(f"According to the configuration, not expecting any relevant files in subdirectory '{dirpath}' so will not check for any")
        return

    # According to the configuration, this subdirectory has relevant files
    logging.info(f"According to the configuration, expecting to find at least '{relevant_count}' relevant files in subdirectory '{dirpath}'")

    # According to the configuration, this subdirectory has files
    if dirpath not in dir_lookup or "filenames" not in dir_lookup[dirpath] or len(dir_lookup[dirpath]["filenames"]) == 0:
        if is_optional:
            logging.info(f"According to the configuration, subdirectory '{dirpath}' is optional")
            return
        else:
            rprint(f"[bold red]ERROR: According to the configuration, expected to find at least '{relevant_count}' relevant files in subdirectory '{dirpath}' but this program did not find any[/]")
            logging.error(f"ERROR: According to the configuration, expected to find at least '{relevant_count}' relevant files in subdirectory '{dirpath}' but this program did not find any")
            sys.exit(1)

    # This program found files in the current data subdirectory (dirpath)
    check_files(
        config_filenames,
        dirpath,
        dir_lookup[dirpath]["filenames"],
        is_optional
    )

def is_subdir_optional(dirpath, config_dirname_lookup) -> bool:
    dirname = os.path.basename(dirpath)
    if config_dirname_lookup is None:
        logging.warning(f"Cannot determine if directory '{dirpath}' is optional because the config_dirname_lookup is not defined")
        return False
        # raise Exception(f"config_dirnames is not defined while processing dirpath '{dirpath}'")
    if "optional" in config_dirname_lookup and config_dirname_lookup["optional"]:
        global subdir_is_optional_lookup
        subdir_is_optional_lookup[dirname] = True
        logging.info(f"According to the configuration, the directory '{dirpath}' is optional")
        return True
    logging.info(f"According to the configuration, the directory '{dirpath}' is NOT optional")
    return False

# def is_subdir_optional(dirpath, config_dirnames) -> bool:
#     dirname = os.path.basename(dirpath)
#     if config_dirnames is None:
#         logging.warning(f"Cannot determine if directory '{dirpath}' is optional because the config_dirnames is not defined")
#         return False
#         # raise Exception(f"config_dirnames is not defined while processing dirpath '{dirpath}'")
#     if dirname in config_dirnames and "optional" in config_dirnames[dirname] and config_dirnames[dirname]["optional"]:
#         logging.info(f"According to the configuration, the directory '{dirpath}' is optional")
#         return True
#     logging.info(f"According to the configuration, the directory '{dirpath}' is NOT optional")
#     return False



def process_directory(dirpath, config_dirnames, config_filenames, dir_lookup, is_optional, config) -> None:
    if ignore_dir(dirpath):
        return

    # print(f"dir_lookup: {dir_lookup}")
    logging.info(f"Processing dirpath '{dirpath}'")
    logging.info(f"config_dirnames: {config_dirnames}")
    logging.info(f"config_filenames: {config_filenames}")

    # if os.path.basename(dirpath) == "individual_cnv_compiler_methods":
    #     sys.exit(1)
    process_files_in_directory(
        dirpath,
        config_filenames,
        dir_lookup,
        is_optional
    )

    relevant_count = get_object_count(config_dirnames)

    if relevant_count == 0:
        # According to the configuration, this subdirectory should not have any relevant subdirectories
        logging.info(f"According to the configuration, not expecting to find any subdirectories in subdirectory '{dirpath}' so will not check for any")
        return

    # According to the configuration, this subdirectory has relevant subdirectories
    logging.info(f"According to the configuration, expecting to find at least '{relevant_count}' relevant subdirectories in subdirectory '{dirpath}'")

    if "dirnames" not in dir_lookup[dirpath] or len(dir_lookup[dirpath]["dirnames"]) == 0:
        logging.error(f"ERROR: dir_lookup[{dirpath}]: {dir_lookup[dirpath]}")
        rprint(f"[bold red]ERROR: According to the configuration, expected to at least '{relevant_count}' relevant subdirectories in subdirectory '{dirpath}' but this program did not find any![/]")
        sys.exit(1)

    # This program found subdirectories in the current data subdirectory (dirpath)
    # The check_directories will verify that the relevant subdirectories according
    # to the configuration are accounted for.  It will search based on exact match
    # and pattern match accordingly.
    check_directories(
        config_dirnames,
        dirpath,
        dir_lookup[dirpath]["dirnames"]
    )

    # Since we are iterating, want to ensure that we only perform
    # the exact_match check only one time for each subdirectory
    exact_match_subdir_checked_lookup = {}

    # Since we are iterating, want to ensure that we only perform
    # the pattern_match check only one time
    pattern_match_subdir_checked_lookup = {}

    # Now iterate over the expected subdirectories (i.e.: the ones specified in the
    # configuration file for this subdirectory) and check whether each matches
    # the criteria (either exact_match or pattern_match) and then perform the
    # recursive call to this process_directory function for that qualified subdirectory.
    for config_dirname, config_dirname_lookup in config_dirnames.items():
        logging.info(f"About to recursively process config_dirname '{config_dirname}' subdirectory to '{dirpath}'")

        if "exact_match" in config_dirname_lookup and config_dirname_lookup["exact_match"]:
            # Expect to only perform an exact_match check for this subdirectory.

            if config_dirname in exact_match_subdir_checked_lookup:
                # Already performed the exact_match for this subdirectory
                continue

            # Register that this config_dirname is now considered checked
            # so that we don't recheck it again.
            exact_match_subdir_checked_lookup[config_dirname] = True

            # Derive the absolute path for this subdirectory
            subdirpath = os.path.join(dirpath, config_dirname)

            # Derive the dirnames and filenames of this current subdirectory.
            # subdir_config_dirnames = get_subdir_config_dirnames(config_dirnames, config_dirname)
            subdir_config_dirnames = get_subdir_config_dirnames(config_dirname_lookup)
            subdir_config_filenames = get_subdir_config_filenames(config_dirname_lookup)
            # subdir_config_filenames = get_subdir_config_filenames(config_dirnames, config_dirname)
            # subdir_config_filenames = get_subdir_config_filenames(config_filenames, config_dirname)

            # subdir_config_dirnames = config.get("dirnames", None) # Because a subdirectory might have subdirectories
            # subdir_config_filenames = config.get("filenames", None) # Because a subdirectory might have files
            # print(f">>> subdirpath '{subdirpath}' subdir_config_dirnames {subdir_config_dirnames} subdir_config_filenames {subdir_config_filenames}")

            subdir_config = {
                "dirnames": subdir_config_dirnames,
                "filenames": subdir_config_filenames
            }

            # Check whether this config_dirname is optional.
            # If it is and this program does not find an instance of this subdirectory,
            # then processing should continue.
            # If it is required and this program does not find an instance of this subdirectory,
            # then processing should be aborted.
            is_optional = is_subdir_optional(subdirpath, config_dirname_lookup)
            # if config_dirname == 'CNV_images':
            #     print(f"{config_dirname} {is_optional} {config_dirname_lookup}")
            #     sys.exit(1)

            process_directory(
                subdirpath,
                subdir_config_dirnames,
                subdir_config_filenames,
                dir_lookup,
                is_optional,
                subdir_config
            )

        elif "pattern_match" in config_dirname_lookup:
            # Perform regex pattern match instead
            pattern = config_dirname_lookup["pattern_match"]
            compiled_pattern = re.compile(pattern)
            for dirname in dir_lookup[dirpath]["dirnames"]:
                if re.search(compiled_pattern, dirname):
                    # The regex pattern match was successful so
                    # use the actual subdirectory that this program
                    # found in order to derive the absolute path.
                    subdirpath = os.path.join(dirpath, dirname)

                    # subdir_config_dirnames = config.get("dirnames", None) # Because a subdirectory might have subdirectories
                    # subdir_config_filenames = config.get("filenames", None) # Because a subdirectory might have files

                    # Derive the dirnames and filenames of this current subdirectory.
                    # subdir_config_dirnames = get_subdir_config_dirnames(config_dirnames, config_dirname)
                    # subdir_config_filenames = get_subdir_config_filenames(config_filenames, config_dirname)

                    subdir_config_dirnames = get_subdir_config_dirnames(config_dirname_lookup)
                    subdir_config_filenames = get_subdir_config_filenames(config_dirname_lookup)

                    subdir_config = {
                        "dirnames": subdir_config_dirnames,
                        "filenames": subdir_config_filenames
                    }

                    # Check whether this config_dirname is optional.
                    # If it is and this program does not find an instance of this subdirectory,
                    # then processing should continue.
                    # If it is required and this program does not find an instance of this subdirectory,
                    # then processing should be aborted.
                    is_optional = is_subdir_optional(subdirpath, config_dirname_lookup)

                    process_directory(
                        subdirpath,
                        subdir_config_dirnames,
                        subdir_config_filenames,
                        dir_lookup,
                        is_optional,
                        subdir_config
                    )

    # for subdir in dir_lookup[dirpath]["dirnames"]:
    #     subdir_config = config["dirnames"][subdir]
    #     subdirpath = os.path.join(dirpath, subdir)
    #     subdir_config_dirnames = subdir_config.get("dirnames", None) # Because a subdirectory might have subdirectories
    #     subdir_config_filenames = subdir_config.get("filenames", None) # Because a subdirectory might have files

    #     process_directory(
    #         subdirpath,
    #         subdir_config_dirnames,
    #         subdir_config_filenames,
    #         dir_lookup,
    #         subdir_config
    #     )

    # if ".git" in dirpath:
    #     continue

    # sys.exit(1)
    # continue
    # if 'venv' in dirpath:
    #     logging.info(f"Going to ignore files in directory '{dirpath}'")
    #     continue
    # for name in filenames:
    #     path = os.path.normpath(os.path.join(dirpath, name))
    #     if os.path.isfile(path):
    #         if extension is not None:
    #             if os.path.endswith('.{extension}'):
    #                 file_list.append(path)
    #         else:
    #             file_list.append(path)

def get_subdir_config_dirnames(config_dirname_lookup) -> Dict[str, Any]:
    if config_dirname_lookup is not None and "dirnames" in config_dirname_lookup and len(config_dirname_lookup["dirnames"]) > 0:
        return config_dirname_lookup["dirnames"]
    return None

# def get_subdir_config_dirnames(config_dirnames, config_dirname) -> Dict[str, Any]:
#     subdir_config_dirnames = None
#     if config_dirnames is not None:
#         if config_dirname in config_dirnames:
#             if "dirnames" in config_dirnames[config_dirname] and len(config_dirnames[config_dirname]["dirnames"]) > 0:
#                 subdir_config_dirnames = config_dirnames[config_dirname]["dirnames"]
#     return subdir_config_dirnames

def get_subdir_config_filenames(config_dirname_lookup) -> Dict[str, Any]:
    if config_dirname_lookup is not None and "filenames" in config_dirname_lookup and len(config_dirname_lookup["filenames"]) > 0:
        return config_dirname_lookup["filenames"]
    return None


# def get_subdir_config_filenames(config_filenames, config_dirname) -> Dict[str, Any]:
#     logging.info(f"Will attempt to derive the filenames for subdirectory '{config_dirname}'")
#     subdir_config_filenames = None
#     if config_filenames is not None:
#         if config_dirname in config_filenames:
#             if "filenames" in config_filenames[config_dirname] and len(config_filenames[config_dirname]["filenames"]) > 0:
#                 subdir_config_filenames = config_filenames[config_dirname]["filenames"]
#         else:
#             logging.info(f"{config_dirname} does not exist in the config_filenames lookup or there are no filenames according to the configuration")
#             logging.error(f"config_filenames: {config_filenames}")
#     else:
#         logging.info("config_filesnames lookup is not defined")
#     return subdir_config_filenames


def check_infile_status(infile: str = None, extension: str = None) -> bool:
    """Check if the file exists, if it is a regular file and whether it has content.

    Args:
        infile (str): the file to be checked

    Raises:
        None
    """

    error_ctr = 0

    if infile is None or infile == '':
        error_console.print(f"'{infile}' is not defined")
        error_ctr += 1
    else:
        if not os.path.exists(infile):
            error_ctr += 1
            error_console.print(f"'{infile}' does not exist")
        else:
            if not os.path.isfile(infile):
                error_ctr += 1
                error_console.print(f"'{infile}' is not a regular file")
            if os.stat(infile).st_size == 0:
                error_console.print(f"'{infile}' has no content")
                error_ctr += 1
            if extension is not None and not infile.endswith(extension):
                error_console.print(f"'{infile}' does not have filename extension '{extension}'")
                error_ctr += 1

    if error_ctr > 0:
        error_console.print(f"Detected problems with input file '{infile}'")
        sys.exit(1)




@click.command()
@click.option('--config_file', type=click.Path(exists=True), help=f"The configuration file for this project - default is '{DEFAULT_CONFIG_FILE}'")
@click.option('--indir', help="The primary input file")
@click.option('--logfile', help="The log file")
@click.option('--outdir', help="The default is the current working directory - default is '{DEFAULT_OUTDIR}'")
@click.option('--outfile', help="The output final report file")
@click.option('--verbose', is_flag=True, help=f"Will print more info to STDOUT - default is '{DEFAULT_VERBOSE}'")
def main(config_file: str, indir: str, logfile: str, outdir: str, outfile: str, verbose: bool):
    """Profile the batch directory"""
    error_ctr = 0

    indir = "/mnt/pure3/Analysis/gav4/R00005960L1_22FTK2LT3"
    if indir is None:
        error_console.print("--indir was not specified")
        error_ctr += 1

    if error_ctr > 0:
        sys.exit(1)


    if config_file is None:
        config_file = DEFAULT_CONFIG_FILE
        console.print(f"[yellow]--config_file was not specified and therefore was set to '{config_file}'[/]")


    if outdir is None:
        outdir = DEFAULT_OUTDIR
        console.print(f"[yellow]--outdir was not specified and therefore was set to '{outdir}'[/]")


    if not os.path.exists(outdir):
        pathlib.Path(outdir).mkdir(parents=True, exist_ok=True)

        console.print(f"[yellow]Created output directory '{outdir}'[/]")

    if logfile is None:
        logfile = os.path.join(
            outdir,
            os.path.splitext(os.path.basename(__file__))[0] + '.log'
        )
        console.print(f"[yellow]--logfile was not specified and therefore was set to '{logfile}'[/]")


    logging.basicConfig(
        filename=logfile,
        format=DEFAULT_LOGGING_FORMAT,
        level=DEFAULT_LOGGING_LEVEL,
    )

    check_infile_status(config_file, "yaml")

    logging.info(f"Will load contents of config file 'config_file'")
    config = yaml.safe_load(Path(config_file).read_text())

    global ignore_dirpath_lookup
    ignore_dirpath_lookup = config["ignore_dirpath_lookup"]

    global ignore_subdir_lookup
    ignore_subdir_lookup = config["ignore_subdir_lookup"]

    profile_data_directory(config, indir)

    print(f"The log file is '{logfile}'")
    console.print(f"[bold green]Execution of '{os.path.abspath(__file__)}' completed[/]")


if __name__ == "__main__":
    main()

