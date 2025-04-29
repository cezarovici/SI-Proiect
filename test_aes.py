from algorithms.aes_algorithm import AESAlgorithm
from algorithms.encryption_algorithm import EncryptionResult

def create_test_file(filename, content):
    with open(filename, 'w') as f:
        f.write(content)
    print(f"Fișier de test creat: {filename}")

def test_aes():
    
    aes = AESAlgorithm()
    
    key_id = aes.generate_key(256)
    print(f"Cheie generată - ID: {key_id}")
    
    # Creează fișier de test
    input_file = "test_input.txt"
    encrypted_file = "test_encrypted.enc"
    decrypted_file = "test_decrypted.txt"
    create_test_file(input_file, "Acesta este un mesaj secret pentru test AES!")
    
    # Test criptare
    print("\nCriptare fișier...")
    enc_result = aes.encrypt_file(input_file, encrypted_file, key_id)
    print(f"Rezultat criptare: {'Succes' if enc_result.success else 'Eșuat'}")
    print(f"Timp criptare: {enc_result.time_taken:.4f} secunde")
    
    # Test decriptare
    print("\nDecriptare fișier...")
    dec_result = aes.decrypt_file(encrypted_file, decrypted_file, key_id)
    print(f"Rezultat decriptare: {'Succes' if dec_result.success else 'Eșuat'}")
    print(f"Timp decriptare: {dec_result.time_taken:.4f} secunde")
    
    # Verifică conținutul
    print("\nConținut original vs decriptat:")
    with open(input_file, 'r') as f:
        print(f"Original:  {f.read()}")
    with open(decrypted_file, 'r') as f:
        print(f"Decriptat: {f.read()}")

if __name__ == "__main__":
    test_aes()
