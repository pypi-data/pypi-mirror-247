from abc import ABC, abstractmethod


class FirstockAPI(ABC):
    @abstractmethod
    def firstockPositionBook(self, userId):
        """
        :return:
        """
        pass
