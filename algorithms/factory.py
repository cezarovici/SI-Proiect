from .aes_algorithm import AESAlgorithm

class AlgorithmFactory:
    @staticmethod
    def create_algorithm(algorithm_name: str):
        if algorithm_name.lower() == "aes":
            return AESAlgorithm()
        elif algorithm_name.lower() == "rsa":
            pass
        else:
            raise ValueError(f"Navem asa algoritm")