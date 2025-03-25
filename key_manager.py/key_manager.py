class KeyManager:
    def __init__(self, db_connection):
        self.db = db_connection
    
    def store_key(self, key_id, key_data, algorithm):
        # stocare in DB
        pass
    
    def get_key(self, key_id) -> bytes:
        # obtinere cheie din DB
        pass
    
    def store_key_pair(self, key_id: str, private_key: bytes, public_key: bytes):
        # pentru RSA
        pass
    
    def get_public_key(self, key_id: str) -> bytes:
        #pentru RSA
        pass
    
    def get_private_key(self, key_id: str) -> bytes:
        # pentru RSA
        pass