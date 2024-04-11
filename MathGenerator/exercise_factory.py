import logging
from abc import ABC, abstractmethod

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ExerciseFactory(ABC):

    def __init__(self):
        logger.info(f'Instance of {self.__class__.__name__} has been created.')
        super().__init__()

    @abstractmethod
    def generate(self, level):
        pass

    @abstractmethod
    def solve(self):
        pass
