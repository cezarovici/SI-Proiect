import subprocess
from algorithms.base import CryptoAlgorithm
import tempfile
import os

class RSAAlgorithm(CryptoAlgorithm):
    def __init__(self, public_key: str, private_key: str):
        self.public_key = public_key
        self.private_key = private_key

    def encrypt(self, input_path: str, output_path: str):
        with tempfile.NamedTemporaryFile(delete=False) as pub_file:
            pub_file.write(self.public_key.encode())
            pub_file_path = pub_file.name

        try:
            subprocess.run([
                "openssl", "rsautl", "-encrypt",
                "-inkey", pub_file_path,
                "-pubin",
                "-in", input_path,
                "-out", output_path
            ], check=True)
        finally:
            os.remove(pub_file_path)

    def decrypt(self, input_path: str, output_path: str):
        with tempfile.NamedTemporaryFile(delete=False) as priv_file:
            priv_file.write(self.private_key.encode())
            priv_file_path = priv_file.name

        try:
            subprocess.run([
                "openssl", "rsautl", "-decrypt",
                "-inkey", priv_file_path,
                "-in", input_path,
                "-out", output_path
            ], check=True)
        finally:
            os.remove(priv_file_path)
