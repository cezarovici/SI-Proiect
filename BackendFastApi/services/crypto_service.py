# services/crypto_service.py

# Asigurați-vă că aceste importuri corespund numelor exacte ale claselor
# și locației fișierelor în directorul 'algorithms'.
from algorithms.aes_crypto import AESCryptography
from algorithms.aes_openSSL import AESAlgorithm
from algorithms.rsa_crypto import RSACryptography
from algorithms.rsa_openSSL import RSAAlgorithm
# Asigurați-vă că EncryptionResult este importat corect din locația sa
# (probabil algorithms.encryption_algorithm)
from algorithms.encryption_algorithm import EncryptionResult

SUPPORTED_ALGORITHMS = {
    "aes_open": AESAlgorithm,
    "rsa_open": RSAAlgorithm,
    "aes_crypto": AESCryptography,
    "rsa_crypto": RSACryptography,
}

def get_algorithm_instance(name: str):
    """
    Returnează o instanță a clasei de algoritm specificate.
    """
    algorithm_class = SUPPORTED_ALGORITHMS.get(name.lower())
    if algorithm_class:
        return algorithm_class()
    else:
        raise ValueError(f"Algoritmul '{name}' nu este suportat.")


def encrypt(input_path: str, output_path: str, key_data_for_encryption: str, algorithm_name: str) -> EncryptionResult:
    """
    Criptează un fișier folosind algoritmul specificat.
    key_data_for_encryption: Cheia publică pentru RSA, cheia simetrică pentru AES.
    """
    try:
        algo = get_algorithm_instance(algorithm_name)
        return algo.encrypt(input_path, output_path, key_data_for_encryption)
    except FileNotFoundError as fnf_error:
        print(f"[Service] Eroare la criptarea ({algorithm_name}): Fișierul '{fnf_error.filename}' nu a fost găsit.")
        return EncryptionResult(False, None, 0, 0, algorithm_name, "N/A (File Not Found)")
    except ValueError as val_error:
        print(f"[Service] Eroare la criptarea ({algorithm_name}): Problemă cu valorile - {val_error}")
        return EncryptionResult(False, None, 0, 0, algorithm_name, "N/A (Value Error)")
    except Exception as e:
        print(f"[Service] Eroare generală la criptarea ({algorithm_name}): {e}")
        # Puteți adăuga aici și traceback pentru debugging:
        # import traceback
        # print(traceback.format_exc())
        return EncryptionResult(False, None, 0, 0, algorithm_name, "N/A (Exception)")


def decrypt(input_path: str, output_path: str, key_data_for_decryption: str, algorithm_name: str) -> EncryptionResult:
    """
    Decriptează un fișier folosind algoritmul specificat.
    key_data_for_decryption: Cheia privată pentru RSA, cheia simetrică pentru AES.
    """
    try:
        algo = get_algorithm_instance(algorithm_name)
        return algo.decrypt(input_path, output_path, key_data_for_decryption)
    except FileNotFoundError as fnf_error:
        print(f"[Service] Eroare la decriptarea ({algorithm_name}): Fișierul '{fnf_error.filename}' nu a fost găsit.")
        return EncryptionResult(False, None, 0, 0, algorithm_name, "N/A (File Not Found)")
    except ValueError as val_error:
        print(f"[Service] Eroare la decriptarea ({algorithm_name}): Problemă cu valorile - {val_error}")
        return EncryptionResult(False, None, 0, 0, algorithm_name, "N/A (Value Error)")
    except Exception as e:
        print(f"[Service] Eroare generală la decriptarea ({algorithm_name}): {e}")
        # import traceback
        # print(traceback.format_exc())
        return EncryptionResult(False, None, 0, 0, algorithm_name, "N/A (Exception)")