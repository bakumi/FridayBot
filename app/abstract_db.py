from abc import ABC, abstractmethod



class AbstractDB(ABC):
    @abstractmethod
    def add_missing_columns(self):
        pass



    @abstractmethod
    def add_info(self):
        pass



    @abstractmethod
    def get_info(self):
        pass



    @abstractmethod
    def update_info(self):
        pass
