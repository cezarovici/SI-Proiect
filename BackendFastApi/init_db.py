from db import Base, engine, SessionLocal
from models.algorithm_model import Algorithm
from models.key_model import Key
from models.file_model import File  

def create_tables():
    Base.metadata.create_all(bind=engine)
    create_default_algorithms()

def create_default_algorithms():
    session = SessionLocal()
    try:
        existing = session.query(Algorithm).filter(Algorithm.name.in_(["AES", "RSA"])).all()
        existing_names = {alg.name for alg in existing}
        
        if "AES" not in existing_names:
            aes = Algorithm(name="AES", type="symmetric")
            session.add(aes)
        if "RSA" not in existing_names:
            rsa = Algorithm(name="RSA", type="asymmetric")
            session.add(rsa)
        
        session.commit()
    except Exception as e:
        session.rollback()
        print(f"Error creating default algorithms: {e}")
    finally:
        session.close()
