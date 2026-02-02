# backend/plugins/base.py

from abc import ABC, abstractmethod

class Plugin(ABC):
    name: str = "base"
    severity: str = "low"

    @abstractmethod
    def scan(self, file_path: str):
        """
        Scan a file and return:
        - None if clean
        - dict if suspicious
        """
        pass
