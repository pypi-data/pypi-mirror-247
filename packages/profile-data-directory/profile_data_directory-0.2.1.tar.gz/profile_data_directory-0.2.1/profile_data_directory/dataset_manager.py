import pathlib
import shutil
import json
import logging
import os

from datetime import datetime
from typing import Dict

from .file_utils import calculate_md5, get_file_creation_date, get_file_size

DEFAULT_VERBOSE = False


class DatasetManager:
    """Class for copying files in a dataset."""

    def __init__(self, **kwargs):
        """Constructor for DatasetManager."""
        self.config = kwargs.get("config", None)
        self.config_file = kwargs.get("config_file", None)
        self.logfile = kwargs.get("logfile", None)
        self.verbose = kwargs.get("verbose", DEFAULT_VERBOSE)

        logging.info(f"Instantiated Manager in file '{os.path.abspath(__file__)}'")

    def _get_qualified_file_extension_lookup(self) -> Dict[str, bool]:
        if "file_extension_list" not in self.config:
            raise Exception(f"Did not find 'file_extension_list' in the configuration file '{self.config_file}'")
        extension_list = self.config["file_extension_list"]
        if extension_list is None or len(extension_list) == 0:
            raise Exception(f"The 'file_extension_list' was not defined in the configuration file '{self.config_file}'")

        lookup = {}
        for i, extension in enumerate(extension_list, start=1):
            lookup[extension] = True
        logging.info(f"Loaded '{i}' qualified extensions in the lookup")
        return lookup


    def _get_file_list(self, indir: str = None, extension_lookup: Dict[str, bool] = None) -> list:
        """Get the list of files in the specified directory.

        Args:
            indir (str): the directory to search for files
            extension_lookup (dict): key is extension e.g.: vcf and value is bool e.g.: True

        Returns:
            list: list of qualified files
        """
        file_list = []

        file_ctr = 0
        qualified_ctr = 0
        unqualified_ctr = 0

        logging.info(f"Will search for qualified files in directory '{indir}'")

        for dirpath, dirnames, filenames in os.walk(indir):
            for name in filenames:
                path = os.path.normpath(os.path.join(dirpath, name))
                if os.path.isfile(path):
                    file_ctr += 1
                    extension = os.path.splitext(path)[1].lstrip(".")
                    logging.info(f"Found file '{path}' with extension '{extension}'")
                    if extension in extension_lookup:
                        qualified_ctr += 1
                        file_list.append(path)
                    else:
                        unqualified_ctr += 1

        logging.info(f"Found '{file_ctr}' files")
        logging.info(f"Found '{qualified_ctr}' qualified files")
        logging.info(f"Found '{unqualified_ctr}' unqualified files")

        return file_list


    def copy_dataset_files(self, source: str, destination: str) -> None:
        # Example:
        # source = "/data/projects/project-1/"
        # Step 1: find all files
        # source_file = "/data/project-1/A/file1.txt"
        # destination = "/data/repositories/"
        # Step 2: derive the source basename
        # source_basename = "project-1"
        # Step 3: create the destination mkdir -p "/data/repositories/project-1"
        # Step 4: for each source_file derive destination_subdir
        #
        #
        #
        # destination_subdir = "/data/repositories/project-1/A"
        # destination_file = "/data/repositories/project-1/A/file1.txt"
        # Step 5: copy the file cp(source_file, destination_file)

        source_basedir = os.path.basename(source)
        target_destination_dir = os.path.join(destination, source_basedir)

        if not os.path.exists(target_destination_dir):
            pathlib.Path(target_destination_dir).mkdir(parents=True, exist_ok=True)
            logging.info(f"Created destination directory '{target_destination_dir}'")


        file_extension_lookup = self._get_qualified_file_extension_lookup()

        file_list = self._get_file_list(source, file_extension_lookup)

        ctr = 0

        for source_file in file_list:
            ctr += 1

            relative_path = source_file.split(source_basedir)[1].lstrip("/")

            logging.info(f"Processing source file '{source_file}' with relative path '{relative_path}'")

            destination_file = os.path.join(target_destination_dir, relative_path)
            destination_subdir = os.path.dirname(destination_file)

            logging.info(f"destination file '{destination_file}' with subdirectory '{destination_subdir}'")

            if not os.path.exists(destination_subdir):
                pathlib.Path(destination_subdir).mkdir(parents=True, exist_ok=True)
                logging.info(f"Created destination directory '{destination_subdir}'")

            shutil.copy(source_file, destination_file)
            logging.info(f"Copied '{source_file}' to '{destination_file}'")

            self._create_provenance_file(source_file, destination_file)

        logging.info(f"Copied '{ctr}' files from source '{source}' to destination '{target_destination_dir}'")

    def _create_provenance_file(self, source_file: str, destination_file: str) -> None:
        checksum = calculate_md5(source_file)
        create_date = get_file_creation_date(source_file)
        size = get_file_size(source_file)
        outfile = f"{destination_file}.provenance.json"
        date_transferred = f"{str(datetime.today().strftime('%Y-%m-%d-%H:%M:%S'))}"

        lookup = {
            "method-transferred": os.path.abspath(__file__),
            "date-transferred": date_transferred,
            "source_file": source_file,
            "md5checksum": checksum,
            "date-created": create_date,
            "file-size": size
        }
        # print(lookup)

        with open(outfile, 'w') as write_file:
            json.dump(lookup, write_file, indent=4, sort_keys=True)
        logging.info(f"Wrote provenance metadata JSON file '{outfile}'")




