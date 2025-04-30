import subprocess
import os
from .encryption_algorithm import EncryptionAlgorithm, EncryptionResult
import time
import psutil
import hashlib

class AESAlgorithm(EncryptionAlgorithm):
    def __init__(self):
        super().__init__("AES")
    
    def encrypt(self, input_file: str, output_file: str, key: str) -> EncryptionResult:
        start_time = time.time()
        process = psutil.Process(os.getpid())
        mem_before = process.memory_info().rss

        iv = os.urandom(16)
        temp_enc_file = "temp_encrypted"

        if isinstance(key, str):
            key_bytes = hashlib.sha256(key.encode()).digest()
        else:
            key_bytes = key

        subprocess.run([
            'openssl', 'enc', '-aes-256-cbc',
            '-in', input_file,
            '-out', temp_enc_file,
            '-K', key_bytes.hex(),
            '-iv', iv.hex()
        ], check=True)

        with open(output_file, 'wb') as f_out:
            f_out.write(iv)
            with open(temp_enc_file, 'rb') as f_temp:
                f_out.write(f_temp.read())

        os.remove(temp_enc_file)

        time_taken = time.time() - start_time
        mem_after = process.memory_info().rss
        memory_used = mem_after - mem_before

        return EncryptionResult(True, output_file, time_taken, memory_used, self.algorithm_name, key)
        

    def decrypt(self, input_file: str, output_file: str, key: str) -> EncryptionResult:
        start_time = time.time()
        process = psutil.Process(os.getpid())
        mem_before = process.memory_info().rss

        temp_enc_file = "temp_decrypt"
        with open(input_file, 'rb') as f_in:
            iv = f_in.read(16)
            with open(temp_enc_file, 'wb') as f_temp:
                f_temp.write(f_in.read())

        if isinstance(key, str):
            key_bytes = hashlib.sha256(key.encode()).digest()
        else:
            key_bytes = key

        subprocess.run([
            'openssl', 'enc', '-d', '-aes-256-cbc',
            '-in', temp_enc_file,
            '-out', output_file,
            '-K', key_bytes.hex(),
            '-iv', iv.hex()
        ], check=True)

        os.remove(temp_enc_file)

        time_taken = time.time() - start_time
        mem_after = process.memory_info().rss
        memory_used = mem_after - mem_before

        return EncryptionResult(True, output_file, time_taken, memory_used, self.algorithm_name, key)

    

    #-------------------------------------------------------------------------------------
    def generate_key(self, key_length: int = 256) -> str:
        if key_length not in [128, 192, 256]:
            raise ValueError("Lungime cheie AES invalida. 128, 192, 256")
        
        key = os.urandom(key_length // 8)
        key_id = f"aes_key_{int(time.time())}"
        self.keys[key_id] = key  # Stochează temporar cheia
        
        return key_id