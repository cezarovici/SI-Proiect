from algorithms.aes_openSSL import *
from algorithms.rsa_openSSL import *
from algorithms.encryption_algorithm import EncryptionResult

def get_algorithm_instance(name: str):
    if name.lower() == "aes":
        return AESAlgorithm()
    elif name.lower() == "rsa":
        return RSAAlgorithm()
    else:
        raise ValueError("Unsupported algorithm")


def encrypt_file(input_path, output_path, key_data, algorithm_name) -> EncryptionResult:
    algo = get_algorithm_instance(algorithm_name)
    try:
        return algo.encrypt(input_path, output_path, key_data)
    except Exception as e:
        print(f"[Service] Eroare criptare: {e}")
        return EncryptionResult(False, None, 0, 0, algorithm_name, "N/A")


def decrypt_file(input_path, output_path, key_data, algorithm_name) -> EncryptionResult:
    algo = get_algorithm_instance(algorithm_name)
    try:
        return algo.decrypt(input_path, output_path, key_data)
    except Exception as e:
        print(f"[Service] Eroare decriptare: {e}")
        return EncryptionResult(False, None, 0, 0, algorithm_name, "N/A")
