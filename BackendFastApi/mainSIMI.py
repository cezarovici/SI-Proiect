from algorithms.aes_openSSL import AESAlgorithm
from services.crypto_service import encrypt, decrypt

key_data = "parola_mea_sigura"  # înlocuiești cu cheia din DB în proiect
input_path = "test_input.txt"
encrypted_path = "test_encrypted.bin"
decrypted_path = "test_decrypted.txt"

with open(input_path, "w", encoding="utf-8") as f:
    f.write("Acesta este un test de criptare și decriptare.")

print("\n=== Criptare ===")
enc_result = encrypt(input_path, encrypted_path, key_data, "aes")
print(vars(enc_result))

print("\n=== Decriptare ===")
dec_result = decrypt(encrypted_path, decrypted_path, key_data, "aes")
print(vars(dec_result))

if dec_result.success:
    with open(decrypted_path, "r", encoding="utf-8") as f:
        print("\n=== Conținut decriptat ===")
        print(f.read())
