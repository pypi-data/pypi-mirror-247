# -*- coding: utf-8 -*-
import logging
import os

from typing import Tuple
from datetime import datetime

DEFAULT_OUTDIR = os.path.join(
    "/tmp",
    os.path.splitext(os.path.basename(__file__))[0],
    str(datetime.today().strftime("%Y-%m-%d-%H%M%S")),
)

DEFAULT_VERBOSE = False


class Parser:
    """Class for parsing Python .py files."""

    def __init__(self, **kwargs):
        """Constructor for class for parsing Python .py files."""

        self.infile = kwargs.get("infile", None)

        self.is_parsed = False
        self.private_attributes_list = []
        self.uniq_private_attributes_lookup = {}
        self.class_name = None
        self.methods_list = []
        self.imports_list = []
        self.constants_list = []

        logging.info(f"Have instantiated Parser in '{os.path.abspath(__file__)}'")

    def get_private_attributes_list(self) -> None:
        """Retrieve the list of private attributes declared in the constructor
        of the class.

        Returns:
            list: list of private attributes
        """
        if not self.is_parsed:
            self._parse_file()
        return self.private_attributes_list

    def get_class_name(self) -> None:
        """Retrieve the name of the class.

        Returns:
            str: name of the class
        """
        if not self.is_parsed:
            self._parse_file()
        return self.class_name

    def get_methods_list(self) -> None:
        """Retrieve the list of method names defined in the class.

        Returns:
            list: list of method names
        """
        if not self.is_parsed:
            self._parse_file()
        return self.methods_list

    def get_imports_list(self) -> None:
        """Retrieve the list of import statements for the class.

        Returns:
            list: list of import statements
        """
        if not self.is_parsed:
            self._parse_file()
        return self.imports_list

    def get_constants_list(self) -> None:
        """Retrieve the list of import statements for the class.

        Returns:
            list: list of import statements
        """
        if not self.is_parsed:
            self._parse_file()
        return self.constants_list

    def _parse_file(self) -> None:
        logging.info(f"Will read file '{self.infile}'")
        line_ctr = 0

        class_found = False
        found_constructor = False
        processed_constructor = False

        with open(self.infile, "r") as f:
            for line in f:
                line_ctr += 1
                line = line.strip()
                if line == "":
                    continue

                if not class_found:
                    if line.startswith("import "):
                        self.imports_list.append(line.strip())
                    elif line.startswith("from ") and " import " in line:
                        self.imports_list.append(line.strip())
                    elif "=" in line:
                        constant = line.split("=")[0].strip()
                        self.constants_list.append(constant)

                if line.startswith("class "):
                    class_found = True
                    class_name = line.replace("class ", "")
                    if "(" in class_name:
                        parts = class_name.split("(")
                        class_name = parts[0]
                    if "src" in self.infile:
                        parts = self.infile.split("src/")
                        prefix = parts[1].replace("/", "::")
                        if prefix.endswith(".py"):
                            prefix = prefix.rstrip(".py")
                        full_class_name = f"{prefix}::{class_name}"
                    else:
                        full_class_name = class_name
                    self.class_name = full_class_name
                elif line.startswith("def __init__(self"):
                    found_constructor = True

                elif found_constructor and not processed_constructor:
                    if line.startswith("self."):
                        private_attribute = (
                            line.split("=")[0].replace("self.", "").strip()
                        )
                        logging.info(
                            f"derived private attribute '{private_attribute}' from line '{line}'"
                        )
                        if private_attribute not in self.uniq_private_attributes_lookup:
                            self.private_attributes_list.append(private_attribute)
                            self.uniq_private_attributes_lookup[
                                private_attribute
                            ] = True

                    elif line.startswith("def "):
                        processed_constructor = True
                        found_constructor = False

                        method, method_signature = self._parse_method(line)
                        # method = line.lstrip("def ").split("(")[0]
                        logging.info(f"derived method '{method}' from line '{line}'")
                        self.methods_list.append(method_signature)

                elif line.startswith("def ") and processed_constructor:
                    method, method_signature = self._parse_method(line)
                    logging.info(f"derived method '{method}' from line '{line}'")
                    self.methods_list.append(method_signature)

        if line_ctr > 0:
            logging.info(f"Read '{line_ctr}' lines from file '{self.infile}'")
        else:
            logging.info(f"Did not read any lines from file '{self.infile}'")
        self.is_parsed = True

    def _parse_method(self, line: str) -> Tuple[str, str]:
        """Parse the method to derive the method name and method signature.

        Args:
            line (str): the line to parse
        Returns:
            str: the method name
            str: the method signature
        """
        method_name = line.strip().split("(")[0].lstrip("def ")
        method_signature = line.strip().lstrip("def ")

        if "(self, " in method_signature:
            method_signature = method_signature.replace("(self, ", "(")
        elif "(self " in method_signature:
            method_signature = method_signature.replace("(self ", "(")

        method_signature = method_signature.rstrip(":") # remove trailing colon
        return method_name, method_signature
