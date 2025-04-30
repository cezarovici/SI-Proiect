import os
import subprocess
import time
import psutil
import tempfile
from .encryption_algorithm import EncryptionAlgorithm, EncryptionResult

class RSAAlgorithm(EncryptionAlgorithm):
    def __init__(self):
        super().__init__("RSA")

    def generate_key(self, key_length: int = 2048) -> tuple[str, str]:

        with tempfile.NamedTemporaryFile(delete=False, mode='w+', suffix='.pem') as priv_file, \
             tempfile.NamedTemporaryFile(delete=False, mode='w+', suffix='.pem') as pub_file:

            priv_path = priv_file.name
            pub_path = pub_file.name

        subprocess.run([
            "openssl", "genpkey",
            "-algorithm", "RSA",
            "-out", priv_path,
            "-pkeyopt", f"rsa_keygen_bits:{key_length}"
        ], check=True)

        subprocess.run([
            "openssl", "rsa",
            "-pubout",
            "-in", priv_path,
            "-out", pub_path
        ], check=True)

        with open(priv_path, 'r') as f:
            private_key = f.read()
        with open(pub_path, 'r') as f:
            public_key = f.read()

        os.remove(priv_path)
        os.remove(pub_path)

        return public_key, private_key

    def encrypt_file(self, input_file: str, output_file: str, public_key_str: str) -> EncryptionResult:
        start_time = time.time()
        process = psutil.Process(os.getpid())
        mem_before = process.memory_info().rss

        with tempfile.NamedTemporaryFile(delete=False, mode='w', suffix='.pem') as pubkey_file:
            pubkey_file.write(public_key_str)
            pubkey_path = pubkey_file.name

        subprocess.run([
            "openssl", "pkeyutl",
            "-encrypt",
            "-in", input_file,
            "-out", output_file,
            "-pubin",
            "-inkey", pubkey_path
        ], check=True)

        os.remove(pubkey_path)

        time_taken = time.time() - start_time
        mem_after = process.memory_info().rss
        memory_used = mem_after - mem_before

        return EncryptionResult(
            success=True,
            output_file=output_file,
            time_taken=time_taken,
            memory_used=memory_used,
            algorithm_name=self.algorithm_name,
            key_id="inline"
        )


    def decrypt_file(self, input_file: str, output_file: str, private_key_str: str) -> EncryptionResult:
        start_time = time.time()
        process = psutil.Process(os.getpid())
        mem_before = process.memory_info().rss


        with tempfile.NamedTemporaryFile(delete=False, mode='w', suffix='.pem') as privkey_file:
            privkey_file.write(private_key_str)
            privkey_path = privkey_file.name

        subprocess.run([
            "openssl", "pkeyutl",
            "-decrypt",
            "-in", input_file,
            "-out", output_file,
            "-inkey", privkey_path
        ], check=True)

        os.remove(privkey_path)

        time_taken = time.time() - start_time
        mem_after = process.memory_info().rss
        memory_used = mem_after - mem_before

        return EncryptionResult(
            success=True,
            output_file=output_file,
            time_taken=time_taken,
            memory_used=memory_used,
            algorithm_name=self.algorithm_name,
            key_id="inline"
        )

        