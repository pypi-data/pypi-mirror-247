from abc import ABC, abstractmethod


class CloudController(ABC):
    @abstractmethod
    def scale(self, node_count: int):
        pass

    def disable_autoscaler(self):
        pass
