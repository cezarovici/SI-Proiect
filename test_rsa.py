import os
from algorithms.rsa_algorithm import RSAAlgorithm

# Fișiere de test
input_file = "rsa_test_input.txt"
encrypted_file = "rsa_encrypted.bin"
decrypted_file = "rsa_decrypted.txt"

# Mesaj test
original_message = "Acesta este un mesaj secret pentru test RSA!"

# Scrie mesajul în fișierul de intrare
with open(input_file, "w", encoding="utf-8") as f:
    f.write(original_message)

# Inițializare algoritm RSA
rsa = RSAAlgorithm()

# Generare chei RSA
key_id = rsa.generate_key()
print(f"Cheie generată: {key_id}")

# Criptare
print("\nCriptare fișier...")
encrypt_result = rsa.encrypt_file(input_file, encrypted_file, key_id)
print(f"Rezultat criptare: {'Succes' if encrypt_result.success else 'Eșuat'}")
print(f"Timp criptare: {encrypt_result.time_taken:.4f} secunde")
print(f"Memorie utilizată: {encrypt_result.memory_used} bytes")

# Decriptare
print("\nDecriptare fișier...")
decrypt_result = rsa.decrypt_file(encrypted_file, decrypted_file, key_id)
print(f"Rezultat decriptare: {'Succes' if decrypt_result.success else 'Eșuat'}")
print(f"Timp decriptare: {decrypt_result.time_taken:.4f} secunde")
print(f"Memorie utilizată: {decrypt_result.memory_used} bytes")

# Comparare fișiere
with open(decrypted_file, "r", encoding="utf-8") as f:
    decrypted_message = f.read()

print("\nConținut original vs decriptat:")
print("Original: ", original_message)
print("Decriptat:", decrypted_message)

# Curățare fișiere (opțional)
# os.remove(input_file)
# os.remove(encrypted_file)
# os.remove(decrypted_file)
