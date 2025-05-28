import os
import time
import psutil
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
from .encryption_algorithm import EncryptionAlgorithm, EncryptionResult
import hashlib 

class AESCryptography(EncryptionAlgorithm):
    def __init__(self):
        super().__init__("AES-Cryptography") 

    def encrypt(self, input_file: str, output_file: str, key_param: str) -> EncryptionResult: 
        start_time = time.time()
        process = psutil.Process(os.getpid())
        mem_before = process.memory_info().rss

        try:
            if isinstance(key_param, str):
                key = hashlib.sha256(key_param.encode('utf-8')).digest() 
            elif isinstance(key_param, bytes) and len(key_param) in [16, 24, 32]:
                key = key_param
            else:
                raise ValueError("Cheia AES trebuie să fie un string sau o secvență de 16, 24, sau 32 de octeți.")

            iv = os.urandom(16) 
            cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
            encryptor = cipher.encryptor()
            padder = padding.PKCS7(algorithms.AES.block_size).padder() 

            with open(input_file, "rb") as f:
                plaintext = f.read()

            padded_data = padder.update(plaintext) + padder.finalize()
            ciphertext = encryptor.update(padded_data) + encryptor.finalize()

            with open(output_file, "wb") as f:
                f.write(iv + ciphertext)

            time_taken = time.time() - start_time
            mem_after = process.memory_info().rss
            memory_used = mem_after - mem_before

            return EncryptionResult(True, output_file, time_taken, memory_used, self.algorithm_name, key_id="derived_from_string")

        except Exception as e:
            print(f"[{self.algorithm_name}] Eroare la criptare: {e}")
            return EncryptionResult(False, None, time.time() - start_time, mem_after - mem_before if 'mem_before' in locals() and 'mem_after' in locals() else 0, self.algorithm_name, key_id=None)

    def decrypt(self, input_file: str, output_file: str, key_param: str) -> EncryptionResult: 
        start_time = time.time()
        process = psutil.Process(os.getpid())
        mem_before = process.memory_info().rss

        try:
            if isinstance(key_param, str):
                key = hashlib.sha256(key_param.encode('utf-8')).digest()
            elif isinstance(key_param, bytes) and len(key_param) in [16, 24, 32]:
                key = key_param
            else:
                raise ValueError("Cheia AES trebuie să fie un string sau o secvență de 16, 24, sau 32 de octeți.")

            with open(input_file, "rb") as f:
                iv = f.read(16) 
                ciphertext = f.read()

            cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
            decryptor = cipher.decryptor()
            unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()

            padded_plaintext = decryptor.update(ciphertext) + decryptor.finalize()
            plaintext = unpadder.update(padded_plaintext) + unpadder.finalize()

            with open(output_file, "wb") as f: 
                f.write(plaintext)

            time_taken = time.time() - start_time
            mem_after = process.memory_info().rss
            memory_used = mem_after - mem_before

            return EncryptionResult(True, output_file, time_taken, memory_used, self.algorithm_name, key_id="derived_from_string")

        except Exception as e:
            print(f"[{self.algorithm_name}] Eroare la decriptare: {e}")
            return EncryptionResult(False, None, time.time() - start_time, mem_after - mem_before if 'mem_before' in locals() and 'mem_after' in locals() else 0, self.algorithm_name, key_id=None)