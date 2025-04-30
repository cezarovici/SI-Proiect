import os
import subprocess
import time
import psutil
from .encryption_algorithm import EncryptionAlgorithm, EncryptionResult

class RSAAlgorithm(EncryptionAlgorithm):
    def __init__(self):
        super().__init__("RSA")
        self.key_dir = "rsa_keys"
        os.makedirs(self.key_dir, exist_ok=True)

    def generate_key(self, key_length: int = 2048) -> str:
        key_id = f"rsa_key_{int(time.time())}"
        privkey_path = os.path.join(self.key_dir, f"{key_id}_private.pem")
        pubkey_path = os.path.join(self.key_dir, f"{key_id}_public.pem")

        subprocess.run([
            "openssl", "genpkey",
            "-algorithm", "RSA",
            "-out", privkey_path,
            "-pkeyopt", f"rsa_keygen_bits:{key_length}"
        ], check=True)

        subprocess.run([
            "openssl", "rsa",
            "-pubout",
            "-in", privkey_path,
            "-out", pubkey_path
        ], check=True)

        print(f"[RSA] Chei generate: {key_id}")
        return key_id

    def encrypt_file(self, input_file: str, output_file: str, key_id: str) -> EncryptionResult:
        start_time = time.time()
        process = psutil.Process(os.getpid())
        mem_before = process.memory_info().rss

        try:
            pubkey_path = os.path.join(self.key_dir, f"{key_id}_public.pem")
            subprocess.run([
                "openssl", "pkeyutl",
                "-encrypt",
                "-in", input_file,
                "-out", output_file,
                "-pubin",
                "-inkey", pubkey_path
            ], check=True)

            time_taken = time.time() - start_time
            mem_after = process.memory_info().rss
            memory_used = mem_after - mem_before

            return EncryptionResult(
                success=True,
                output_file=output_file,
                time_taken=time_taken,
                memory_used=memory_used,
                algorithm_name=self.algorithm_name,
                key_id=key_id
            )

        except subprocess.CalledProcessError as e:
            print(f"[RSA] Eroare la criptare: {e}")
            return EncryptionResult(False, None, 0, 0, self.algorithm_name, key_id)

    def decrypt_file(self, input_file: str, output_file: str, key_id: str) -> EncryptionResult:
        start_time = time.time()
        process = psutil.Process(os.getpid())
        mem_before = process.memory_info().rss

        try:
            privkey_path = os.path.join(self.key_dir, f"{key_id}_private.pem")
            subprocess.run([
                "openssl", "pkeyutl",
                "-decrypt",
                "-in", input_file,
                "-out", output_file,
                "-inkey", privkey_path
            ], check=True)

            time_taken = time.time() - start_time
            mem_after = process.memory_info().rss
            memory_used = mem_after - mem_before

            return EncryptionResult(
                success=True,
                output_file=output_file,
                time_taken=time_taken,
                memory_used=memory_used,
                algorithm_name=self.algorithm_name,
                key_id=key_id
            )

        except subprocess.CalledProcessError as e:
            print(f"[RSA] Eroare la decriptare: {e}")
            return EncryptionResult(False, None, 0, 0, self.algorithm_name, key_id)
