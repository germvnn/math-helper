from __future__ import annotations
from abc import ABC, abstractmethod
from datetime import datetime
import os

from pylatex import (Document, StandAloneGraphic, LineBreak,
                     Section, PageStyle, Head, MiniPage,
                     Foot, LargeText, Figure, NoEscape)
from pylatex.utils import bold

from PDFGenerator import constants as const
from PDFGenerator import utils


class PDFBuilder(ABC):
    """
    The abstract base class that defines the builder
    interface for constructing PDF documents.
    """

    geometry_settings = {"margin": "0.7in"}
    header = PageStyle("header")

    def __init__(self):
        self._setup_document()

    def _setup_document(self):
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
            # Replace backslashes due to LaTeX Syntax
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

    def insert_title(self, title: str) -> None:
        """Inserts the title into the PDF."""
        with self.doc.create(MiniPage(align='c')):
            self.doc.append(LargeText(bold(title)))

    @abstractmethod
    def insert_exercise(self, numerator: int, exercise: str) -> None:
        """Inserts an exercise into the PDF."""
        pass

    @abstractmethod
    def insert_solution(self, numerator: int, exercise: str, solution) -> None:
        """Inserts a solution into the PDF."""
        pass

    def generate(self, filename,
                 filepath: str = os.path.join(
                     # Replace backslashes due to LaTeX Syntax
                     os.path.dirname(os.path.dirname(__file__)), 'PDFs').replace('\\', "/")
                 ) -> None:
        self.doc.generate_pdf(filepath=f"{filepath}/{filename}",
                              compiler='pdflatex',
                              clean_tex=True)
        self._setup_document()
        utils.Plot.remove()


class ArithmeticPDFBuilder(PDFBuilder):
    """
    Builder implementation that constructs parts of a MathPDF
    document. It keeps track of the components added to the product
    and provides the resulting product.
    """

    def insert_exercise(self, numerator: int, exercise: str) -> None:

        with self.doc.create(
                Section(utils.exercise_string(numerator=numerator,
                                              exercise=exercise,
                                              end_line="= ?"), numbering=False)
        ):
            pass

    def insert_solution(self, numerator: int, exercise: str, solution) -> None:
        with self.doc.create(Section(utils.solution_string(numerator=numerator,
                                                           exercise=exercise,
                                                           comparison_operator="=",
                                                           solution=solution), numbering=False)):
            pass


class QuadraticPDFBuilder(PDFBuilder):

    def insert_exercise(self, numerator: int, exercise: str) -> None:
        with self.doc.create(
            Section(utils.quadratic_exercise_string(numerator=numerator,exercise=exercise), numbering=False)
        ):
            pass

    def insert_solution(self, numerator: int, exercise: str, solution) -> None:
        with self.doc.create(
                Section(utils.quadratic_exercise_string(numerator=numerator,
                                                        exercise=exercise), numbering=False)
        ):
            self.doc.append(utils.quadratic_solution_string(roots=solution['roots'],
                                                            delta=solution['delta']))
            img_path = os.path.join(os.path.dirname(__file__), f'plot{numerator}.png')
            utils.Plot.quadratic(numerator=numerator,
                                 exercise=exercise,
                                 solution=solution)
            with self.doc.create(Figure(position="h!")) as plot:
                plot.add_image(img_path, width=NoEscape(r'0.57\textwidth'))


class LinearPDFBuilder(PDFBuilder):

    def insert_exercise(self, numerator: int, exercise: str) -> None:
        with self.doc.create(
            Section(utils.linear_exercise_string(numerator=numerator, exercise=exercise), numbering=False)
        ):
            pass

    def insert_solution(self, numerator: int, exercise: str, solution) -> None:
        pass


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
        self.builder.insert_title(title=title)
        for i, exercise in enumerate(exercises, 1):
            self.builder.insert_exercise(numerator=i, exercise=exercise)
        self.builder.generate(filename)

    def build_solutions(self, title, exercises: dict, filename: str) -> None:
        """
        Constructs a PDF document with solutions, including a title, a series of exercises, and a header.
        """
        self.builder.insert_title(title=title)
        for i, (exercise, solution) in enumerate(exercises.items(), 1):
            self.builder.insert_solution(numerator=i, exercise=exercise, solution=solution)
        self.builder.generate(filename)

    def build_exam(self):
        pass


if __name__ == "__main__":
    director = Director()
    builder = LinearPDFBuilder()
    director.builder = builder

    linear = ['3x + 1 <= 2x - 2', '2x - 3 >= 3x', '3x - 1 < 3',
              '-2x - 3 > -x + 2', '3x - 1 = -x + 3', '-2x = 3x - 2',
              '2x = 2x']

    director.build_exercises(title="Exercises", exercises=linear, filename="exercises")
    # director.build_solutions(title="Solutions", exercises=examples_solutions, filename="solutions")
