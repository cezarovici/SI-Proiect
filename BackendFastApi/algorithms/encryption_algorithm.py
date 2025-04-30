from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional
import time

@dataclass
class EncryptionResult:

    success: bool
    output_file: Optional[str]
    time_taken: float
    memory_used: int  
    algorithm_name: str
    key_id: Optional[str]

class EncryptionAlgorithm(ABC):
    def __init__(self, algorithm_name: str):
        self.algorithm_name = algorithm_name
    
    @abstractmethod
    def encrypt(self, input_file: str, output_file: str, key: str) -> EncryptionResult:
        pass
    
    @abstractmethod
    def decrypt(self, input_file: str, output_file: str, key: str) -> EncryptionResult:
        pass
    
    @abstractmethod
    def generate_key(self, key_length: int = None) -> str:
        pass