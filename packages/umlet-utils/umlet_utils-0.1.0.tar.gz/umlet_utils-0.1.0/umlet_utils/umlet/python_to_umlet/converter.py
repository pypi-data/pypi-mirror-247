# -*- coding: utf-8 -*-
import logging
import os
from datetime import datetime

from ..file.writer import Writer
from ..file_system.util import Util
from ..python.file.parser import Parser

DEFAULT_OUTDIR = os.path.join(
    "/tmp",
    os.path.splitext(os.path.basename(__file__))[0],
    str(datetime.today().strftime("%Y-%m-%d-%H%M%S")),
)

DEFAULT_VERBOSE = False


class Converter:
    """Class for converting Python files into Umlet class diagram .uxf file."""

    def __init__(self, **kwargs):
        """Class constructor."""
        self.outdir = kwargs.get("outdir", None)
        self.outfile = kwargs.get("outfile", None)
        self.classes_only_outfile = kwargs.get("classes_only_outfile", None)
        self.logfile = kwargs.get("logfile", None)
        self.indir = kwargs.get("indir", None)

        self.util = Util(**kwargs)
        self.writer = Writer(**kwargs)

        logging.info(f"Have instantiated Converter in '{os.path.abspath(__file__)}'")

    def run(self) -> None:
        """Will retrieve the Python files from the specified directory, parse
        each file and then write the Umlet .uxf file."""
        file_list = self.util.get_file_list_from_directory(self.indir)

        file_objects = []

        for python_file in file_list:
            logging.info(f"Processing Python file '{python_file}'")

            parser = Parser(infile=python_file)
            class_name = parser.get_class_name()
            if class_name is None:
                continue

            lookup = {
                "class_name": class_name,
                "private_attributes_list": parser.get_private_attributes_list(),
                "methods_list": parser.get_methods_list(),
                "imports_list": parser.get_imports_list(),
                "constants_list": parser.get_constants_list(),
            }

            file_objects.append(lookup)

        self.writer.write_file(file_objects)
