from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
import os
import time
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

        return private_bytes.decode(), public_bytes.decode()

    def encrypt_file(self, input_file: str, output_file: str, public_key_str: str) -> EncryptionResult:
        start_time = time.time()
        try:
            public_key = serialization.load_pem_public_key(public_key_str.encode())
            with open(input_file, "rb") as f:
                plaintext = f.read()

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

            return EncryptionResult(
                success=True,
                output_file=output_file,
                time_taken=time.time() - start_time,
                memory_used=0,
                algorithm_name=self.algorithm_name,
                key_id="in_memory"
            )

        except Exception as e:
            print(f"[Cryptography RSA] Eroare la criptare: {e}")
            return EncryptionResult(False, None, 0, 0, self.algorithm_name, "in_memory")

    def decrypt_file(self, input_file: str, output_file: str, private_key_str: str) -> EncryptionResult:
        start_time = time.time()
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

            return EncryptionResult(
                success=True,
                output_file=output_file,
                time_taken=time.time() - start_time,
                memory_used=0,
                algorithm_name=self.algorithm_name,
                key_id="in_memory"
            )

        except Exception as e:
            print(f"[Cryptography RSA] Eroare la decriptare: {e}")
            return EncryptionResult(False, None, 0, 0, self.algorithm_name, "in_memory")
