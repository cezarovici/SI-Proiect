from .aes_algorithm import AESAlgorithm
from .rsa_algorithm import RSAAlgorithm  

class AlgorithmFactory:
    @staticmethod
    def create_algorithm(algorithm_name: str):
        algorithm_name = algorithm_name.lower()
        if algorithm_name == "aes":
            return AESAlgorithm()
        elif algorithm_name == "rsa":
            return RSAAlgorithm() 
        else:
            raise ValueError(f"Algoritm necunoscut: {algorithm_name}")