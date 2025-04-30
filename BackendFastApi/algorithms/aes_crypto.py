import os
import time
import psutil
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
from .encryption_algorithm import EncryptionAlgorithm, EncryptionResult

class AESCryptography(EncryptionAlgorithm):
    def __init__(self):
        super().__init__("AES")

    def encrypt(self, input_file: str, output_file: str, key: bytes) -> EncryptionResult:
        start_time = time.time()
        process = psutil.Process(os.getpid())
        mem_before = process.memory_info().rss

        try:
            iv = os.urandom(16)
            cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
            encryptor = cipher.encryptor()
            padder = padding.PKCS7(128).padder()

            with open(input_file, "rb") as f:
                plaintext = f.read()

            padded_data = padder.update(plaintext) + padder.finalize()
            ciphertext = encryptor.update(padded_data) + encryptor.finalize()

            with open(output_file, "wb") as f:
                f.write(iv + ciphertext)

            time_taken = time.time() - start_time
            mem_after = process.memory_info().rss
            memory_used = mem_after - mem_before

            return EncryptionResult(True, output_file, time_taken, memory_used, self.algorithm_name, key_id=None)

        except Exception as e:
            print(f"[AES] Eroare la criptare: {e}")
            return EncryptionResult(False, None, 0, 0, self.algorithm_name, key_id=None)

    def decrypt(self, input_file: str, output_file: str, key: bytes) -> EncryptionResult:
        start_time = time.time()
        process = psutil.Process(os.getpid())
        mem_before = process.memory_info().rss

        try:
            with open(input_file, "rb") as f:
                iv = f.read(16)
                ciphertext = f.read()

            cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
            decryptor = cipher.decryptor()
            unpadder = padding.PKCS7(128).unpadder()

            padded_plaintext = decryptor.update(ciphertext) + decryptor.finalize()
            plaintext = unpadder.update(padded_plaintext) + unpadder.finalize()

            with open(output_file, "wb") as f:
                f.write(plaintext)

            time_taken = time.time() - start_time
            mem_after = process.memory_info().rss
            memory_used = mem_after - mem_before

            return EncryptionResult(True, output_file, time_taken, memory_used, self.algorithm_name, key_id=None)

        except Exception as e:
            print(f"[AES] Eroare la decriptare: {e}")
            return EncryptionResult(False, None, 0, 0, self.algorithm_name, key_id=None)
