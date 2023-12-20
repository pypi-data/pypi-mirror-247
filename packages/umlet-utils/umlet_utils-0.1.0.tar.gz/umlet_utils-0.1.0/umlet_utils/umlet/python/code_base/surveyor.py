# -*- coding: utf-8 -*-
import logging
import os
from datetime import datetime
from typing import Any, Dict, Union

from ....umlet.file_system.util import Util
from ....umlet.python.file.parser import Parser

DEFAULT_OUTDIR = os.path.join(
    "/tmp",
    os.path.splitext(os.path.basename(__file__))[0],
    str(datetime.today().strftime("%Y-%m-%d-%H%M%S")),
)

DEFAULT_VERBOSE = False


class Surveyor:
    """Class for converting Python files into Umlet class diagram .uxf file."""

    def __init__(self, **kwargs: Dict[str, str]):
        """Class constructor."""
        self.outdir = kwargs.get("outdir", None)
        self.outfile = kwargs.get("outfile", None)
        self.logfile = kwargs.get("logfile", None)
        self.indir = kwargs.get("indir", None)
        self.verbose = kwargs.get("verbose", DEFAULT_VERBOSE)

        self.util = Util(**kwargs)

        self.class_ctr = 0
        self.file_ctr = 0
        self.method_ctr = 0
        self.imports_set = set()
        self.constants_set = set()


        logging.info(f"Have instantiated Surveyor in '{os.path.abspath(__file__)}'")

    def run(self) -> None:
        """Will retrieve the Python files from the specified directory, parse
        each file and then write the report .txt file."""
        file_list = self.util.get_file_list_from_directory(self.indir)

        file_objects = []

        for python_file in file_list:
            logging.info(f"Processing Python file '{python_file}'")
            self.file_ctr += 1

            parser = Parser(infile=python_file)
            class_name = parser.get_class_name()
            if class_name is None:
                continue

            self.class_ctr += 1
            methods = parser.get_methods_list()
            self.method_ctr += len(methods)

            imports = parser.get_imports_list()
            for i in imports:
                self.imports_set.add(i)

            constants = parser.get_constants_list()
            for c in constants:
                self.constants_set.add(c)

            lookup = {
                "filename": python_file,
                "class_name": class_name,
                "private_attributes_list": parser.get_private_attributes_list(),
                "methods_list": methods,
                "imports_list": imports,
                "constants_list": constants,
            }

            file_objects.append(lookup)

        self._write_report_file(file_objects)


    def _write_report_file(self, file_objects: Union[Dict[str, Any], None] = None) -> None:

        with open(self.outfile, 'w') as of:
            of.write(f"## method-created: {os.path.abspath(__file__)}\n")
            of.write(f"## date-created: {str(datetime.today().strftime('%Y-%m-%d-%H%M%S'))}\n")
            of.write(f"## created-by: {os.environ.get('USER')}\n")
            of.write(f"## indir: {self.indir}\n")
            of.write(f"## logfile: {self.logfile}\n")
            of.write("\n\n========================================\n\n")
            of.write("\t\tSummary\n")
            of.write("\n\n========================================\n\n")

            of.write(f"Number of files: {self.file_ctr}\n")
            of.write(f"Number of classes: {self.class_ctr}\n")
            of.write(f"Number of methods: {self.method_ctr}\n")
            of.write(f"Number of unique imports: {len(self.imports_set)}\n")
            of.write(f"Number of unique constants: {len(self.constants_set)}\n")

            for fo in file_objects:
                of.write("\n========================================\n")

                of.write(f"For file '{fo['filename']}'\n")

                of.write(f"\nFound the following '{len(fo['imports_list'])}' imports:\n")
                for i, im in enumerate(fo['imports_list'], start=1):
                    of.write(f"{i}. {im}\n")

                of.write(f"\nFound the following '{len(fo['constants_list'])}' constants:\n")
                for i, c in enumerate(fo['constants_list'], start=1):
                    of.write(f"{i}. {c}\n")


                of.write(f"\nFound class '{fo['class_name']}'\n")

                of.write(f"\nFound the following '{len(fo['private_attributes_list'])}' private attributes:\n")
                for i, pa in enumerate(fo['private_attributes_list'], start=1):
                    of.write(f"{i}. {pa}\n")

                of.write(f"\nFound the following '{len(fo['methods_list'])}' methods:\n")
                for i, m in enumerate(fo['methods_list'], start=1):
                    of.write(f"{i}. {m}\n")



        logging.info(f"Wrote file '{self.outfile}'")
        if self.verbose:
            print(f"Wrote file '{self.outfile}'")
