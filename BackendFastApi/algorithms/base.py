class CryptoAlgorithm:
    def encrypt(self, input_path: str, output_path: str, key: str):
        raise NotImplementedError

    def decrypt(self, input_path: str, output_path: str, key: str):
        raise NotImplementedError
