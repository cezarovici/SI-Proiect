from algorithms.rsa_openSSL import *
from algorithms.encryption_algorithm import EncryptionResult
import os

# Inițializare algoritm RSA
rsa = RSAAlgorithm()

# 1. Generează o pereche de chei (publică, privată)
public_key, private_key = rsa.generate_key()
print("Cheie publică:\n", public_key)
print("Cheie privată:\n", private_key)

# 2. Creează un fișier text de test
with open("original.txt", "w") as f:
    f.write("Mesaj test pentru criptare RSA.")

# 3. Criptare folosind cheia publică (string)
encrypt_result = rsa.encrypt_file("original.txt", "encrypted.bin", public_key)
print(f"\n Criptare: {'Succes' if encrypt_result.success else 'Eșec'}")
print(f"Timp criptare: {encrypt_result.time_taken:.4f}s")
print(f"Memorie folosită: {encrypt_result.memory_used / 1024:.2f} KB")

# 4. Decriptare folosind cheia privată (string)
decrypt_result = rsa.decrypt_file("encrypted.bin", "decrypted.txt", private_key)
print(f"\n Decriptare: {'Succes' if decrypt_result.success else 'Eșec'}")
print(f"Timp decriptare: {decrypt_result.time_taken:.4f}s")
print(f"Memorie folosită: {decrypt_result.memory_used / 1024:.2f} KB")

# 5. Afișează conținutul rezultat
with open("decrypted.txt", "r") as f:
    print("\n Conținut decriptat:", f.read())
