from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
import os
import time
import psutil # Adăugați acest import
from .encryption_algorithm import EncryptionAlgorithm, EncryptionResult


class RSACryptography(EncryptionAlgorithm):
    def __init__(self):
        super().__init__("RSA-Cryptography")

    def generate_key(self, key_length: int = 2048):
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=key_length
        )
        public_key = private_key.public_key()

        private_bytes = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        )

        public_bytes = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )

        # Asigurăm ordinea (public, private)
        return public_bytes.decode(), private_bytes.decode()

    # Redenumit din encrypt_file în encrypt și ajustat pentru a măsura memoria
    def encrypt(self, input_file: str, output_file: str, public_key_str: str) -> EncryptionResult:
        start_time = time.time()
        process = psutil.Process(os.getpid())
        mem_before = process.memory_info().rss
        try:
            public_key = serialization.load_pem_public_key(public_key_str.encode())
            with open(input_file, "rb") as f:
                plaintext = f.read()

            # Verificați dimensiunea datelor pentru RSA
            # RSA poate cripta direct doar date limitate ca dimensiune (key_size - padding)
            # Pentru fișiere mai mari, se utilizează de obicei criptarea hibridă
            # Aici presupunem că fișierul de intrare este suficient de mic
            max_data_size = (public_key.key_size // 8) - (2 * hashes.SHA256.digest_size) - 2
            if len(plaintext) > max_data_size:
                # Alternativ, se poate implementa criptarea hibridă aici
                raise ValueError(f"Input data is too large for RSA direct encryption. Max size: {max_data_size} bytes.")


            ciphertext = public_key.encrypt(
                plaintext,
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )

            with open(output_file, "wb") as f:
                f.write(ciphertext)
            
            time_taken = time.time() - start_time
            mem_after = process.memory_info().rss
            memory_used = mem_after - mem_before

            return EncryptionResult(
                success=True,
                output_file=output_file,
                time_taken=time_taken,
                memory_used=memory_used, # Actualizat
                algorithm_name=self.algorithm_name,
                key_id="in_memory"
            )

        except Exception as e:
            print(f"[{self.algorithm_name}] Eroare la criptare: {e}")
            return EncryptionResult(False, None, time.time() - start_time, mem_after - mem_before if 'mem_before' in locals() and 'mem_after' in locals() else 0, self.algorithm_name, "in_memory")

    # Redenumit din decrypt_file în decrypt și ajustat pentru a măsura memoria
    def decrypt(self, input_file: str, output_file: str, private_key_str: str) -> EncryptionResult:
        start_time = time.time()
        process = psutil.Process(os.getpid())
        mem_before = process.memory_info().rss
        try:
            private_key = serialization.load_pem_private_key(private_key_str.encode(), password=None)
            with open(input_file, "rb") as f:
                ciphertext = f.read()

            plaintext = private_key.decrypt(
                ciphertext,
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )

            with open(output_file, "wb") as f:
                f.write(plaintext)

            time_taken = time.time() - start_time
            mem_after = process.memory_info().rss
            memory_used = mem_after - mem_before

            return EncryptionResult(
                success=True,
                output_file=output_file,
                time_taken=time_taken,
                memory_used=memory_used, # Actualizat
                algorithm_name=self.algorithm_name,
                key_id="in_memory"
            )

        except Exception as e:
            print(f"[{self.algorithm_name}] Eroare la decriptare: {e}")
            return EncryptionResult(False, None, time.time() - start_time, mem_after - mem_before if 'mem_before' in locals() and 'mem_after' in locals() else 0, self.algorithm_name, "in_memory")