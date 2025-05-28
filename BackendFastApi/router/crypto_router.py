
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import get_db
from crud import file_crud, key_crud, algorithm_crud, performance_crud
from services import crypto_service
from schemas.crypto_schemas import EncryptRequest, DecryptRequest
import os

router = APIRouter(prefix="/crypto", tags=["Cryptography Operations"])

@router.post("/encrypt")
def encrypt_file_endpoint(request: EncryptRequest, db: Session = Depends(get_db)):
    file_obj = file_crud.get_file_by_id(db, request.file_id)
    if not file_obj:
        raise HTTPException(status_code=404, detail="File not found")

    key_obj = key_crud.get_key_by_id(db, file_obj.key_id)
    if not key_obj:
        raise HTTPException(status_code=404, detail="Key not found for file")

    algo_obj = algorithm_crud.get_algorithm_by_id(db, file_obj.algorithm_id)
    if not algo_obj:
        raise HTTPException(status_code=404, detail="Algorithm not found for file")


    if not request.implementation.lower().startswith(algo_obj.name.lower()):
         raise HTTPException(status_code=400, detail=f"Implementation '{request.implementation}' does not match file algorithm '{algo_obj.name}'")

    key_data = ""
    if algo_obj.type == "symmetric": 

        key_data = key_obj.key_value or key_obj.key_name
    elif algo_obj.type == "asymmetric": 
        key_data = key_obj.public_key

    if not key_data:
        raise HTTPException(status_code=400, detail="Encryption key data not found or invalid")

    os.makedirs(os.path.dirname(file_obj.encrypted_path), exist_ok=True)

    enc_result = crypto_service.encrypt(
        input_path=file_obj.original_path,
        output_path=file_obj.encrypted_path,
        key_data_for_encryption=key_data,
        algorithm_name=request.implementation
    )

    perf_data = {
        "file_id": request.file_id,
        "algorithm_id": file_obj.algorithm_id,
        "key_id": file_obj.key_id,
        "operation_type": "encrypt",
        "execution_time_ms": enc_result.time_taken * 1000,
        "memory_usage_mb": enc_result.memory_used / (1024 * 1024),
        "success": enc_result.success,
        "error_message": None if enc_result.success else f"Encryption failed: {enc_result.key_id}"
    }
    performance_crud.create_performance(db, perf_data)

    if not enc_result.success:
        raise HTTPException(status_code=500, detail=perf_data['error_message'])

    return {"encryption_result": vars(enc_result), "performance": perf_data}



@router.post("/decrypt")
def decrypt_file_endpoint(request: DecryptRequest, db: Session = Depends(get_db)):
    print(f"--- Decrypt Request ---")
    print(f"File ID: {request.file_id}, Implementation: {request.implementation}")

    file_obj = file_crud.get_file_by_id(db, request.file_id)
    if not file_obj:
        print(f"ERROR: File ID {request.file_id} not found.")
        raise HTTPException(status_code=404, detail="File not found")
    print(f"Found File: ID={file_obj.file_id}, EncPath={file_obj.encrypted_path}, KeyID={file_obj.key_id}, AlgoID={file_obj.algorithm_id}")

    key_obj = key_crud.get_key_by_id(db, file_obj.key_id)
    if not key_obj:
        print(f"ERROR: Key ID {file_obj.key_id} not found.")
        raise HTTPException(status_code=404, detail="Key not found for file")
    print(f"Found Key: ID={key_obj.key_id}, Name={key_obj.key_name}, Value?={'Yes' if key_obj.key_value else 'No'}, PrivKey?={'Yes' if key_obj.private_key else 'No'}")


    algo_obj = algorithm_crud.get_algorithm_by_id(db, file_obj.algorithm_id)
    if not algo_obj:
        print(f"ERROR: Algorithm ID {file_obj.algorithm_id} not found.")
        raise HTTPException(status_code=404, detail="Algorithm not found for file")
    print(f"Found Algo: ID={algo_obj.algorithm_id}, Name={algo_obj.name}, Type={algo_obj.type}")

    if not request.implementation.lower().startswith(algo_obj.name.lower()):
         print(f"ERROR: Implementation '{request.implementation}' vs Algo '{algo_obj.name}' mismatch.")
         raise HTTPException(status_code=400, detail=f"Implementation '{request.implementation}' does not match file algorithm '{algo_obj.name}'")

    key_data = ""
    if algo_obj.type == "symmetric":
        key_data = key_obj.key_value or key_obj.key_name
    elif algo_obj.type == "asymmetric": 
        key_data = key_obj.private_key

    if not key_data:
        print(f"ERROR: Decryption Key data is empty for Key ID {key_obj.key_id}.")
        raise HTTPException(status_code=400, detail="Decryption key data not found or invalid")
    print(f"Decryption Key data retrieved successfully.")

    input_path = file_obj.encrypted_path
    original_filename = os.path.basename(file_obj.original_path)

    output_path = f"/app/data/DECRYPTED_{original_filename}"

    print(f"Decrypting: {input_path} -> {output_path} using {request.implementation}")

    dec_result = crypto_service.decrypt(
        input_path=input_path,
        output_path=output_path,
        key_data_for_decryption=key_data,
        algorithm_name=request.implementation
    )
    print(f"Decryption Result: Success={dec_result.success}, Time={dec_result.time_taken}, Mem={dec_result.memory_used}")


    perf_data = {
        "file_id": request.file_id, "algorithm_id": file_obj.algorithm_id, "key_id": file_obj.key_id,
        "operation_type": "decrypt", "execution_time_ms": dec_result.time_taken * 1000,
        "memory_usage_mb": dec_result.memory_used / (1024 * 1024), "success": dec_result.success,
        "error_message": None if dec_result.success else f"Decryption failed: {dec_result.key_id}"
    }
    performance_crud.create_performance(db, perf_data)
    print(f"Performance record created. Success={perf_data['success']}")


    if not dec_result.success:
        print(f"ERROR: Decryption process failed.")
        raise HTTPException(status_code=500, detail=perf_data['error_message'])

    print(f"--- Decrypt Request Finished ---")

    return {"decryption_result": vars(dec_result), "performance": perf_data, "output_path": output_path}