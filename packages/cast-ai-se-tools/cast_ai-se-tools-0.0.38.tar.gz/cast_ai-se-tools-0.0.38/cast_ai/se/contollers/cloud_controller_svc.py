from abc import ABC, abstractmethod


class CloudController(ABC):
    @abstractmethod
    def scale(self, node_count: int):
        pass

    def disable_autoscaler(self):
        pass

    def get_node_count(self) -> int:
        pass
