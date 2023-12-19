import hashlib
import json
import logging
import os
from datetime import datetime
from typing import Dict, Optional, Union

from .file_utils import calculate_md5, get_file_creation_date, get_file_list

DEFAULT_VERBOSE = False


class Manager:
    """Class for profiling the data directory."""

    def __init__(self, **kwargs):
        """Constructor for Manager."""
        self.config = kwargs.get("config", None)
        self.config_file = kwargs.get("config_file", None)
        self.indir = kwargs.get("indir", None)
        self.logfile = kwargs.get("logfile", None)
        self.outdir = kwargs.get("outdir", None)
        self.outfile = kwargs.get("outfile", None)
        self.verbose = kwargs.get("verbose", DEFAULT_VERBOSE)

        self.file_list = []
        self._load_subdir_graph()

        logging.info(f"Instantiated Manager in file '{os.path.abspath(__file__)}'")

    def _load_subdir_graph(self) -> None:
        if "directory_graph" not in self.config:
            raise Exception(f"Please check the configuration file '{self.config_file}' - looks like the directory_graph has not been defined")

        lookup = self.config["directory_graph"]
        self.graph = {}
        self._derive_node(lookup, self.indir, 0)

    def _derive_node(self, lookup, parent_dir, depth) -> Dict[str, Dict[str, Union[str, int]]]

        for depth, subdir in enumerate(lookup):
                # Create a graph node
                node = {
                    "parent_dir": parent_dir,
                    "subdir": subdir,
                    "depth": depth,
                    "pattern": lookup[subdir]["pattern"],
                    "ftype": lookup[subdir]["ftype"],
                    "is_file": lookup[subdir]["is_file"]
                }

                if "children" in lookup[subdir]:
                    node["children"] = lookup[subdir]["children"]
                    for child in lookup[subdir]["children"]:
                        self._derive_node()





    def generate_report(self) -> None:
        """Profile data directory and then generate the report file."""
        self._profile_data_directory()
        self._generate_report()


    def _profile_data_directory(self) -> None:
        self.file_list = get_file_list(self.indir)
        for datafile in self.file_list:
            file_type = self._determine_file_type(datafile)

    def _determine_file_type(self, datafile: str) -> str:
        basename = os.path.basename(datafile)
        subdirectories = datafile.split(self.indir)[1]
        subdirs = subdirectories.split("/")
        subdir_count = len(subdirs)
        processed_subdir_lookup = {}
        for i, subdir in enumerate(subdirs):
            if i not in processed_subdir_lookup:
                processed_subdir_lookup[i] = {}
            if i == subdir_count:
                # Found the file
                if subdir != basename:
                    raise Exception(f"subdir '{subdir}' does not match '{basename}' for datafile '{datafile}'")
                if self._is_expected_file(basename):
                    self.found_expected_file_ctr += 1
                    self.found_expected_file_list.append(datafile)
                else:
                    self.found_unexpected_file_ctr += 1
                    self.found_unexpected_file_list.append(datafile)
            else:
                # This must be a subdirectory
                if subdir in processed_subdir_lookup[i]:
                     # Already processed this subdir
                    continue

                processed_subdir_lookup[i] = {}
                processed_subdir_lookup[i][subdir] = True

                if self._is_expected_subdir(subdir, datafile, i):
                    self.found_expected_subdir_ctr += 1
                    self.found_expected_subdir_list.append(os.path.join(self.indir, subdir))
                else:
                    self.found_unexpected_subdir_ctr += 1
                    self.found_unexpected_subdir_list.append(os.path.join(self.indir, subdir))


