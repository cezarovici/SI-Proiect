import subprocess
import os
from .encryption_algorithm import EncryptionAlgorithm, EncryptionResult
import time
import key_manager


class AESAlgorithm(EncryptionAlgorithm):
    def __init__(self):
        super().__init__("AES")
        
    
    def encrypt_file(self, input_file: str, output_file: str, key_id: str) -> EncryptionResult:
        start_time = time.time()

        #TODO
        # obtine cheia din baza de date
        key = key_manager.get

        iv = os.urandom(16)
            
            # 3. Rulează comanda OpenSSL pentru criptare
        subprocess.run([
            'openssl', 'enc', '-aes-256-cbc',
            '-in', input_file,
            '-out', output_file,
            '-K', key.hex(),    
            '-iv', iv.hex()     
        ], check=True)
            
        time_taken = time.time() - start_time
            
        return EncryptionResult(
            success=True,
            output_file=output_file, 
            time_taken=time_taken,
            algorithm_name=self.algorithm_name,
            key_id=key_id
        )
        #date ce trebuiesc in baza de date adaugate apoi

    def decrypt_file(self, input_file: str, output_file: str, key_id: str) -> EncryptionResult:
        pass
    
    def generate_key(self):
        
        key = os.urandom(32)
        key_id = f"aes_key_{int(time.time())}"
        
        #TODO
        #introducerea key si key_id in baza de date

        return key_id