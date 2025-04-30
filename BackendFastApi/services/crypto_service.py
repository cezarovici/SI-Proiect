from algorithms.aes import AESAlgorithm
from algorithms.rsa import RSAAlgorithm

def get_algorithm_instance(name: str):
    if name.lower() == "aes":
        return AESAlgorithm()
    elif name.lower() == "rsa":
        return RSAAlgorithm()
    else:
        raise ValueError("Unsupported algorithm")

def encrypt_file(file_path, output_path, key_path, algorithm_name):
    algo = get_algorithm_instance(algorithm_name)
    # TODO: time it, record perf, call .encrypt()
    algo.encrypt(file_path, output_path, key_path)
