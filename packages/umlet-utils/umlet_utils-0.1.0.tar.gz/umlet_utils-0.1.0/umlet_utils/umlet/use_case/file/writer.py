# -*- coding: utf-8 -*-
import logging
import os
from datetime import datetime
from typing import Any, Dict, List

DEFAULT_OUTDIR = os.path.join(
    "/tmp",
    os.path.splitext(os.path.basename(__file__))[0],
    str(datetime.today().strftime("%Y-%m-%d-%H%M%S")),
)

DEFAULT_VERBOSE = False


X_INITIAL_POSITION = 100
Y_INITIAL_POSITION = 500

WIDTH = 200
HEIGHT = 150

CLASSES_WIDTH_MULTIPLIER = 6.9
CLASSES_ONLY_HEIGHT = 50

X_POSITION_INCREMENT = 10
Y_POSITION_INCREMENT = 10

ZOOM_LEVEL = 10

BACKGROUND_COLOR = "green"


class Writer:
    """Class for writing the Umlet .uxf files."""

    def __init__(self, **kwargs):
        """Constructor for class for writing the Umlet .uxf files."""
        self.outdir = kwargs.get("outdir", None)
        self.outfile = kwargs.get("outfile", None)
        self.classes_only_outfile = kwargs.get("classes_only_outfile", None)
        self.logfile = kwargs.get("logfile", None)
        self.indir = kwargs.get("indir", None)
        self.verbose = kwargs.get("verbose", None)
        self.content = []

        self.x = X_INITIAL_POSITION
        self.y = Y_INITIAL_POSITION
        self.w = WIDTH
        self.h = HEIGHT
        self.zoom_level = ZOOM_LEVEL
        self.background_color = BACKGROUND_COLOR

        logging.info(f"Have instantiated Writer in '{os.path.abspath(__file__)}'")

    def write_file(self, cases: List[str], actors: List[str]) -> None:
        """Write the Umlet .uxf file.

        Args:
            cases (list): list of use cases
            actors (list): list of actors
        """
        self.content.append('<diagram program="umletino" version="15.0.0">')
        self.content.append(f"<zoom_level>{self.zoom_level}</zoom_level>")
        self.add_cases(cases)
        self.add_actors(actors)
        self.content.append("</diagram>")
        self._write_outfile()

    def add_cases(self, cases: List[str]) -> None:
        for case in cases:
            self.content.append(
                f"""<element>
                        <id>UMLUseCase</id>
                        <coordinates>
                            <x>{self.x}</x>
                            <y>{self.y}</y>
                            <w>{self.w}</w>
                            <h>{self.h}</h>
                        </coordinates>
                        <panel_attributes>bg={self.background_color}
{case}
                        </panel_attributes>
                        <additional_attributes></additional_attributes>
                    </element>
                    """
            )

            self.x += X_POSITION_INCREMENT
            self.y += Y_POSITION_INCREMENT

    def add_actors(self, actors: List[str]) -> None:
        for actor in actors:
            self.content.append(
                f"""<element>
                        <id>UMLActor</id>
                        <coordinates>
                            <x>{self.x}</x>
                            <y>{self.y}</y>
                            <w>{self.w}</w>
                            <h>{self.h}</h>
                        </coordinates>
                        <panel_attributes>bg={self.background_color}
                        {actor}
                        </panel_attributes>
                        <additional_attributes></additional_attributes>
                    </element>
                    """
            )

            self.x += X_POSITION_INCREMENT
            self.y += Y_POSITION_INCREMENT

    def _write_outfile(self) -> None:
        with open(self.outfile, "w") as of:
            for line in self.content:
                of.write(f"{line}\n")

        logging.info(f"Wrote file '{self.outfile}'")
        print(f"Wrote file '{self.outfile}'")
