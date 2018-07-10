
from abc import ABC, abstractmethod

class MarkovNodeSetAbstract(ABC):
    @abstractmethod
    def markAsDirty(self, node):
        pass

    @abstractmethod
    def markAsClean(self, node):
        pass