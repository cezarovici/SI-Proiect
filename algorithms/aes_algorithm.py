import subprocess
import os
from .encryption_algorithm import EncryptionAlgorithm, EncryptionResult
import time
import psutil

class AESAlgorithm(EncryptionAlgorithm):
    def __init__(self):
        super().__init__("AES")
    
    def encrypt_file(self, input_file: str, output_file: str, key: str) -> EncryptionResult:
        start_time = time.time()
        process = psutil.Process(os.getpid())
        mem_before = process.memory_info().rss
        try:
            if not key:
                return EncryptionResult(False, None, 0, 0, self.algorithm_name, key)

            iv = os.urandom(16)
            temp_enc_file = "temp_encrypted"

            subprocess.run([
                'openssl', 'enc', '-aes-256-cbc',
                '-in', input_file,
                '-out', temp_enc_file,
                '-K', key.hex(),
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

        except subprocess.CalledProcessError as e:
            print(f"Eroare criptare: {e}")
            return EncryptionResult(False, None, 0, 0, self.algorithm_name, key)
        except Exception as e:
            print(f"eroare generala: {e}")
            return EncryptionResult(False, None, 0, 0, self.algorithm_name, key)
        

    def decrypt_file(self, input_file: str, output_file: str, key: str) -> EncryptionResult:
        start_time = time.time()
        process = psutil.Process(os.getpid())
        mem_before = process.memory_info().rss

        try:
            if not key:
                return EncryptionResult(False, None, 0, 0, self.algorithm_name, key)

            temp_enc_file = "temp_decrypt"
            with open(input_file, 'rb') as f_in:
                iv = f_in.read(16)
                with open(temp_enc_file, 'wb') as f_temp:
                    f_temp.write(f_in.read())

            subprocess.run([
                'openssl', 'enc', '-d', '-aes-256-cbc',
                '-in', temp_enc_file,
                '-out', output_file,
                '-K', key.hex(),
                '-iv', iv.hex()
            ], check=True)

            os.remove(temp_enc_file)

            time_taken = time.time() - start_time
            mem_after = process.memory_info().rss
            memory_used = mem_after - mem_before

            return EncryptionResult(True, output_file, time_taken, memory_used, self.algorithm_name, key)

        except Exception as e:
            print(f"eroare decriptare: {e}")
            return EncryptionResult(False, None, 0, 0, self.algorithm_name, key)
    

    #-------------------------------------------------------------------------------------
    #def generate_key(self, key_length: int = 256) -> str:
    #    if key_length not in [128, 192, 256]:
    #        raise ValueError("Lungime cheie AES invalida. 128, 192, 256")
    #    
    #    key = os.urandom(key_length // 8)
    #    key_id = f"aes_key_{int(time.time())}"
    #    self.keys[key_id] = key  # Stochează temporar cheia
    #    
    #    return key_id