# main_test.py
import os
# get_algorithm_instance este acum importat și folosit din crypto_service
from services.crypto_service import encrypt, decrypt, get_algorithm_instance

def main():
    base_key_data_str = "parola_mea_sigura_foarte_lunga_pentru_testare_si_alte_chestii"
    input_path = "test_input.txt"
    original_content_text = "Acesta este un test de criptare și decriptare pentru diverși algoritmi folosind Python și OpenSSL sau biblioteca cryptography."

    # Creare fișier de intrare
    try:
        with open(input_path, "w", encoding="utf-8") as f:
            f.write(original_content_text)
        print(f"Fișierul de intrare '{input_path}' a fost creat cu succes.")
    except IOError as e:
        print(f"EROARE FATALĂ: Nu s-a putut crea fișierul de intrare '{input_path}': {e}")
        return # Oprește execuția dacă fișierul de intrare nu poate fi creat

    algorithms_to_test = [
        "aes_open",
        "rsa_open",
        "aes_crypto",
        "rsa_crypto"
    ]

    all_tests_passed = True

    for algo_name in algorithms_to_test:
        print(f"\n\n{'='*15} Testare Algoritm: {algo_name.upper()} {'='*15}")

        # Generează nume unice pentru fișiere pentru a evita suprascrierile dacă rulează rapid
        timestamp = "_" # Includerea unui timestamp ar fi bună pentru rulări multiple, dar pentru simplitate omitem
        encrypted_path = f"test_encrypted_{algo_name}{timestamp}.bin"
        decrypted_path = f"test_decrypted_{algo_name}{timestamp}.txt"
        
        encryption_key = None
        decryption_key = None
        current_test_passed = False

        try:
            if "aes" in algo_name.lower():
                encryption_key = base_key_data_str
                decryption_key = base_key_data_str
                print(f"  Se folosește cheia AES (string): '{base_key_data_str[:20]}...' (va fi procesată de algoritm)")
            elif "rsa" in algo_name.lower():
                print("  Se generează perechea de chei RSA...")
                rsa_instance = get_algorithm_instance(algo_name) # Folosim funcția din service
                if hasattr(rsa_instance, 'generate_key'):
                    # Presupunem că generate_key returnează (public_key, private_key)
                    public_key, private_key = rsa_instance.generate_key()
                    encryption_key = public_key
                    decryption_key = private_key
                    print(f"    Cheie Publică {algo_name.upper()} generată (fragment): {public_key[:70].replace(os.linesep, ' ')}...")
                    print(f"    Cheie Privată {algo_name.upper()} generată (fragment): {private_key[:70].replace(os.linesep, ' ')}...")
                else:
                    print(f"  EROARE: {algo_name} (instanța {type(rsa_instance).__name__}) nu are metoda generate_key().")
                    all_tests_passed = False
                    continue # Treci la următorul algoritm
            else:
                print(f"  EROARE: Tip de algoritm necunoscut '{algo_name}'.")
                all_tests_passed = False
                continue


            if encryption_key is None:
                print(f"  EROARE: Cheia de criptare nu a fost setată pentru {algo_name}.")
                all_tests_passed = False
                continue
                
            print(f"\n  --- Criptare cu {algo_name} ---")
            enc_result = encrypt(input_path, encrypted_path, encryption_key, algo_name)
            print(f"    Rezultat Criptare: {vars(enc_result)}")

            if not enc_result.success:
                print(f"    CRIPTarea cu {algo_name} a EȘUAT.")
                all_tests_passed = False
                if enc_result.output_file and os.path.exists(enc_result.output_file):
                    try:
                        os.remove(enc_result.output_file)
                        print(f"    Fișierul criptat incomplet {enc_result.output_file} a fost șters.")
                    except OSError as e_rem_enc:
                        print(f"    Nu s-a putut șterge {enc_result.output_file}: {e_rem_enc}")
                continue # Treci la următorul algoritm

            if decryption_key is None:
                print(f"  EROARE: Cheia de decriptare nu a fost setată pentru {algo_name}.")
                all_tests_passed = False
                continue

            print(f"\n  --- Decriptare cu {algo_name} ---")
            dec_result = decrypt(encrypted_path, decrypted_path, decryption_key, algo_name)
            print(f"    Rezultat Decriptare: {vars(dec_result)}")

            if dec_result.success and dec_result.output_file:
                if not os.path.exists(dec_result.output_file):
                    print(f"    EROARE: Fișierul decriptat {dec_result.output_file} nu a fost creat de algoritm.")
                    all_tests_passed = False
                    continue

                try:
                    with open(dec_result.output_file, "r", encoding="utf-8") as f:
                        decrypted_content = f.read()
                    print("\n    --- Conținut Decriptat ---")
                    print(f"    '{decrypted_content}'")
                    
                    if original_content_text == decrypted_content:
                        print(f"\n    VERIFICARE {algo_name.upper()}: OK! Conținutul original și cel decriptat coincid.")
                        current_test_passed = True
                    else:
                        print(f"\n    VERIFICARE {algo_name.upper()}: EROARE! Conținutul original și cel decriptat NU coincid.")
                        print(f"      Original (lungime {len(original_content_text)}):\n      '{original_content_text}'")
                        print(f"      Decriptat (lungime {len(decrypted_content)}):\n      '{decrypted_content}'")
                        all_tests_passed = False

                except FileNotFoundError:
                    print(f"    EROARE: Fișierul decriptat {dec_result.output_file} nu a fost găsit (deși decriptarea a raportat succes).")
                    all_tests_passed = False
                except UnicodeDecodeError:
                    print(f"    EROARE la citirea fișierului decriptat {dec_result.output_file}: Eroare de decodare Unicode.")
                    all_tests_passed = False
                except Exception as e_read:
                    print(f"    EROARE la citirea/verificarea fișierului decriptat ({dec_result.output_file}): {e_read}")
                    all_tests_passed = False
            else:
                print(f"    DECRIPTarea cu {algo_name} a EȘUAT sau fișierul de ieșire lipsește.")
                all_tests_passed = False

        except Exception as e_outer:
            print(f"  EROARE MAJORĂ în timpul testării algoritmului {algo_name}: {e_outer}")
            # import traceback
            # print(traceback.format_exc())
            all_tests_passed = False
        
        finally:
            # Șterge fișierele generate pentru testul curent, indiferent de rezultat
            # Comentați dacă doriți să le păstrați pentru inspecție
            files_to_clean = [encrypted_path, decrypted_path]
            for file_path in files_to_clean:
                if os.path.exists(file_path):
                    try:
                        os.remove(file_path)
                        # print(f"    Fișierul de test '{file_path}' a fost șters.")
                    except OSError as e_clean:
                        print(f"    Atenție: Nu s-a putut șterge fișierul de test '{file_path}': {e_clean}")
            if current_test_passed:
                print(f"  STATUS {algo_name.upper()}: SUCCES")
            else:
                print(f"  STATUS {algo_name.upper()}: EȘEC")


    print("\n\n" + "="*30)
    if all_tests_passed:
        print("REZUMAT: Toate testele au trecut cu succes!")
    else:
        print("REZUMAT: Unul sau mai multe teste au eșuat.")
    print("="*30)

    # Șterge fișierul de intrare la final
    # Comentați dacă doriți să-l păstrați
    if os.path.exists(input_path):
        try:
            os.remove(input_path)
            print(f"Fișierul de intrare '{input_path}' a fost șters.")
        except OSError as e_final_clean:
            print(f"Atenție: Nu s-a putut șterge fișierul de intrare '{input_path}': {e_final_clean}")


if __name__ == "__main__":
    # Asigurați-vă că aveți pachetele necesare instalate:
    # pip install psutil cryptography
    # De asemenea, OpenSSL trebuie să fie instalat și în PATH pentru algoritmii *_open.
    main()