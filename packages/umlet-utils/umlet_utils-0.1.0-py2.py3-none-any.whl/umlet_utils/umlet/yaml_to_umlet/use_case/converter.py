# -*- coding: utf-8 -*-
import logging
import os
import pathlib
from datetime import datetime

import yaml

from ....umlet.use_case.file.writer import Writer

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
        self.infile = kwargs.get("infile", None)

        self.writer = Writer(**kwargs)

        logging.info(f"Have instantiated Converter in '{os.path.abspath(__file__)}'")

    def run(self) -> None:
        """Will retrieve list of use cases and actors from the config file and write the Umlet .uxf file."""
        config = yaml.safe_load(pathlib.Path(self.infile).read_text())

        if "use_cases" not in config:
            raise Exception(f"Did not find 'use_cases' section in file '{self.infile}'")
        if "actors" not in config:
            raise Exception(f"Did not find 'actors' section in file '{self.infile}'")
        self.writer.write_file(cases=config["use_cases"], actors=config["actors"])
