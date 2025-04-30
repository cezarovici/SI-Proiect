from algorithms.base import CryptoAlgorithm
import subprocess

class AESAlgorithm(CryptoAlgorithm):
    def encrypt(self, input_path: str, output_path: str, key_path: str):
        subprocess.run([
            "openssl", "enc", "-aes-256-cbc",
            "-in", input_path,
            "-out", output_path,
            "-pass", f"file:{key_path}"
        ])

    def decrypt(self, input_path: str, output_path: str, key_path: str):
        subprocess.run([
            "openssl", "enc", "-d", "-aes-256-cbc",
            "-in", input_path,
            "-out", output_path,
            "-pass", f"file:{key_path}"
        ])
