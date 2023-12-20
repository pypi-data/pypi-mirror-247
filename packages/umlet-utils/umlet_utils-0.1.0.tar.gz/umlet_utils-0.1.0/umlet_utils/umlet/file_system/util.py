# -*- coding: utf-8 -*-
import logging
import os
from typing import List

DEFAULT_VERBOSE = False


class Util:
    """Class for working with file system."""

    def __init__(self, **kwargs):
        """Constructor for class for working with file system."""
        self.outdir = kwargs.get("outdir", None)
        self.outfile = kwargs.get("outfile", None)
        self.logfile = kwargs.get("logfile", None)
        self.config = kwargs.get("config", None)
        self.config_file = kwargs.get("config_file", None)

    def get_file_list_from_directory(self, indir: str = None) -> List[str]:
        """Get the list of files in the specified directory.

        :param indir: {str} - the directory to search for files
        :param extension: {str} - the file extension to filter on
        :returns file_list: {list} - the list of files found in the directory
        """
        if not os.path.exists(indir):
            raise Exception(f"'{indir}' does not exist")

        file_list = []
        for dirpath, _, filenames in os.walk(indir):
            if "venv" in dirpath:
                # logging.info(f"Going to ignore files in directory '{dirpath}'")
                continue
            for name in filenames:
                path = os.path.normpath(os.path.join(dirpath, name))
                if os.path.isfile(path):
                    if path.endswith(".py"):
                        file_list.append(path)

        return file_list
