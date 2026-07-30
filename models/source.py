from abc import ABC, abstractmethod


class Source(ABC):
    @abstractmethod
    def get_jobs(self):
        pass