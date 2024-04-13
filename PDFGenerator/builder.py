from __future__ import annotations
from abc import ABC, abstractmethod
from datetime import datetime
import os

from pylatex import (Document, NoEscape,
                     StandAloneGraphic, LineBreak,
                     Section, PageStyle,
                     Head, MiniPage, Foot, LargeText)
from pylatex.utils import bold

from PDFGenerator import constants as const


class PDFBuilder(ABC):
    """
    The abstract base class that defines the builder
    interface for constructing PDF documents.
    """

    @abstractmethod
    def insert_header(self, title: str) -> None:
        """Inserts the title into the PDF."""
        pass

    @abstractmethod
    def insert_exercise(self, numerator: int, exercise: str) -> None:
        """Inserts an exercise into the PDF."""
        pass

    @abstractmethod
    def insert_solution(self, numerator: int, exercise: str, solution) -> None:
        """Inserts a solution into the PDF."""
        pass

    @abstractmethod
    def generate(self, filename):
        """Generate PDF file"""
        pass


class MathPDFBuilder(PDFBuilder):
    """
    Builder implementation that constructs parts of a MathPDF
    document. It keeps track of the components added to the product
    and provides the resulting product.
    """
    geometry_settings = {"margin": "0.7in"}
    # Add document header
    header = PageStyle("header")

    def __init__(self) -> None:
        """Initializes the PDF file with template."""
        self.doc = Document(geometry_options=self.geometry_settings)
        with self.header.create(Head("L")):
            self.header.append(LargeText("Date: "))
            self.header.append(LargeText(datetime.now().strftime("%d.%b.%Y")))
            self.header.append(LineBreak())
            self.header.append(LargeText("Hour: "))
            self.header.append(LargeText(datetime.now().strftime("%H:%M")))
        # Create right header
        with self.header.create(Head("R")):
            logo_path = os.path.join(os.path.dirname(__file__), 'logo.png').replace('\\', "/")
            with self.header.create(MiniPage(width="\\textwidth", pos='r', align='r')):
                self.header.append(
                    StandAloneGraphic(image_options="width=60px", filename=logo_path))
        # Create left footer
        with self.header.create(Foot("L")):
            self.header.append(const.AUTHOR_NAME)
            self.header.append(LineBreak())
            self.header.append(const.PROJECT_NAME)
        # Create right footer
        with self.header.create(Foot("R")):
            self.header.append(const.GITHUB_PROFILE)
            self.header.append(LineBreak())
            self.header.append(const.GITHUB_PROJECT_REPOSITORY)

        self.doc.preamble.append(self.header)
        self.doc.change_document_style("header")

    def insert_header(self, title) -> None:
        with self.doc.create(MiniPage(align='c')):
            self.doc.append(LargeText(bold(title)))

    def insert_exercise(self, numerator: int, exercise: str) -> None:
        with self.doc.create(Section(NoEscape(rf"{numerator}.~~~{exercise} = ?"), numbering=False)):
            pass

    def insert_solution(self, numerator: int, exercise: str, solution) -> None:
        with self.doc.create(Section(NoEscape(rf"{numerator}.~~~{exercise} = {solution}"), numbering=False)):
            pass

    def generate(self, filename, filepath: str = const.DEFAULT_PATH) -> None:
        self.doc.generate_pdf(filepath=f"{filepath}/{filename}",
                              compiler='pdflatex',
                              clean_tex=True)
        self.__init__()


class Director:
    """
    Directs the construction process of a PDF document. It defines the order in which to
    execute the building steps and works with a builder instance to carry out these steps.
    """
    def __init__(self) -> None:
        """Initializes the director with no builder assigned."""
        self._builder = None

    @property
    def builder(self) -> PDFBuilder:
        """Sets the builder instance for the director to use."""
        return self._builder

    @builder.setter
    def builder(self, builder: PDFBuilder) -> None:
        self._builder = builder

    def build_exercises(self, title: str, exercises: list, filename: str) -> None:
        """
        Constructs a PDF document with exercises, including
        a title, a series of exercises, and a header.
        """
        self.builder.insert_header(title=title)
        for i, exercise in enumerate(exercises, 1):
            self.builder.insert_exercise(numerator=i, exercise=exercise)
        self.builder.generate(filename)

    def build_solutions(self, title, exercises: dict, filename: str) -> None:
        """
        Constructs a PDF document with solutions, including a title, a series of exercises, and a header.
        """
        self.builder.insert_header(title=title)
        for i, (exercise, solution) in enumerate(exercises.items(), 1):
            self.builder.insert_solution(numerator=i, exercise=exercise, solution=solution)
        self.builder.generate(filename)


if __name__ == "__main__":
    director = Director()
    builder = MathPDFBuilder()
    director.builder = builder
    examples = ['0.1 + 0.1', '0.06 + 0.08',
                '0.1 + 0.03', '0.09 + 0.06',
                '0.1 + 0.09', '0.08 + 0.07',
                '0.08 + 0.09', '0.09 + 0.06',
                '0.07 + 0.1', '0.09 + 0.08']
    examples_solutions = {'0.1 + 0.1': 0.2, '0.06 + 0.08': 0.14,
                          '0.1 + 0.03': 0.13, '0.09 + 0.06': 0.15,
                          '0.1 + 0.09': 0.19, '0.08 + 0.07': 0.15,
                          '0.08 + 0.09': 0.17, '0.07 + 0.1': 0.17,
                          '0.09 + 0.08': 0.17}

    director.build_exercises(title="Exercises", exercises=examples, filename="exercises")
    director.build_solutions(title="Solutions", exercises=examples_solutions, filename="solutions")
