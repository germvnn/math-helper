from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any


class PDFBuilder(ABC):
    """
    The abstract base class that defines the builder
    interface for constructing PDF documents.
    """

    @property
    @abstractmethod
    def product(self) -> None:
        pass

    @abstractmethod
    def insert_title(self, title) -> None:
        """Inserts the title into the PDF."""
        pass

    @abstractmethod
    def insert_exercise(self, exercise) -> None:
        """Inserts an exercise into the PDF."""
        pass

    @abstractmethod
    def insert_solution(self, solution) -> None:
        """Inserts a solution into the PDF."""
        pass

    @abstractmethod
    def insert_header(self, header) -> None:
        """Inserts a header into the PDF."""
        pass


class MathPDFBuilder(PDFBuilder):
    """
    Builder implementation that constructs parts of a MathPDF
    document. It keeps track of the components added to the product
    and provides the resulting product.
    """
    def __init__(self) -> None:
        """Initializes the builder with an empty MathPDF product."""
        self.reset()

    def reset(self) -> None:
        """Resets the builder with a fresh MathPDF product instance."""
        self._product = MathPDF()

    @property
    def product(self) -> MathPDF:
        """Finalizes the building process and returns the finished MathPDF product."""
        product = self._product
        self.reset()
        return product

    def insert_title(self, title) -> None:
        self._product.add(title)

    def insert_exercise(self, exercise) -> None:
        self._product.add(exercise)

    def insert_solution(self, solution) -> None:
        self._product.add(solution)

    def insert_header(self, header) -> None:
        self._product.add(header)


class MathPDF:
    """
    Represents a MathPDF document. The product class of the Builder design pattern.
    It provides methods to add parts to the document and retrieve the final content.
    """

    def __init__(self) -> None:
        """Initializes an empty list of parts for the PDF document."""
        self.parts = []

    def add(self, part: Any) -> None:
        """Adds a new part to the PDF document."""
        self.parts.append(part)

    def list_parts(self) -> None:
        """Lists out all parts of the PDF document."""
        print(f"PDF parts: {', '.join(self.parts)}", end="")


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

    def build_exercises(self, title, exercises, header) -> None:
        """
        Constructs a PDF document with exercises, including
        a title, a series of exercises, and a header.
        """
        self.builder.insert_title(title)
        for exercise in exercises:
            self.builder.insert_exercise(exercise)
        self.builder.insert_header(header)

    def build_solutions(self, title, exercises, header) -> None:
        """
        Constructs a PDF document with solutions, including a title, a series of exercises, and a header.
        """
        self.builder.insert_title(title)
        for exercise in exercises:
            self.builder.insert_exercise(exercise)
        self.builder.insert_header(header)
