import string
import hashlib
import logging
import os
import platform

from datetime import datetime


def calculate_md5(file_path: str) -> str:
    """Calculate the md5 checksum for the specified file.

    Args:
        file_path (str): the file for which the md5 checksum will be calculated

    Returns:
        str: the calculated md5 checksum
    """
    md5_hash = hashlib.md5()
    logging.info(f"Will attempt to calculate the MD5 checksum for file '{file_path}'")

    with open(file_path, "rb") as file:
        # Read the file in chunks to efficiently handle large files
        for chunk in iter(lambda: file.read(4096), b""):
            md5_hash.update(chunk)

    return md5_hash.hexdigest()


def get_file_creation_date(file_path: str) -> datetime:
    """Determine the creation date for the specified file.

    Args:
        file_path (str): the absolute path of the file

    Returns:
        datetime: the date the file was created according to the operating system
    """
    if platform.system() == "Windows":
        # On Windows, use creation time
        creation_time = os.path.getctime(file_path)
    else:
        # On Unix-based systems, use birth time (creation time)
        # Note: Not all file systems support birth time, and it might not be available on some systems.
        stat_info = os.stat(file_path)
        creation_time = stat_info.st_mtime

    # Convert the timestamp to a readable date
    creation_date = f"{datetime.fromtimestamp(creation_time)}"

    return creation_date

def get_file_list(indir: str = None, extension: str = None) -> list:
    """Get the list of files in the specified directory
    :param indir: {str} - the directory to search for files
    :param extension: {str} - the file extension to filter on
    :returns file_list: {list} - the list of files found in the directory
    """
    if extension is None:
        logging.info(f"Going to search for files in directory '{indir}'")
    else:
        logging.info(f"Going to search for files with extension '{extension}' in directory '{indir}'")

    file_list = []
    for dirpath, dirnames, filenames in os.walk(indir):
        if 'venv' in dirpath:
            logging.info(f"Going to ignore files in directory '{dirpath}'")
            continue
        for name in filenames:
            path = os.path.normpath(os.path.join(dirpath, name))
            if os.path.isfile(path):
                if extension is not None:
                    if os.path.endswith('.{extension}'):
                        file_list.append(path)
                else:
                    file_list.append(path)

    return file_list


def get_file_size(file_path: str) -> int:
    # Check if the file exists
    if os.path.exists(file_path):
        # Get the file size in bytes
        file_size = os.path.getsize(file_path)
        return file_size
    else:
        raise Exception(f"The file '{file_path}' does not exist.")


def get_line_count(file_path: str) -> int:
    # if is_binary_file(file_path):
    #     print(f"Unable to get line count for binary file '{file_path}'")
    #     return None
    try:
        with open(file_path, 'r') as file:
            line_count = sum(1 for line in file)
        return line_count
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def is_binary_file(file_path: str, block_size: int = 1024) -> bool:
    try:
        with open(file_path, 'rb') as file:
            block = file.read(block_size)
            if not block:  # Empty file
                return False

            # Check for the presence of null bytes (indicative of binary files)
            if b'\x00' in block:
                return True

            # Check for a significant number of non-printable ASCII characters
            text_characters = set(string.printable)
            if not all(byte in text_characters or byte == b'\n' for byte in block):
                return True

            return False  # File is likely text

    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

