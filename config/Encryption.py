import os
import argon2
import base64
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from dotenv import load_dotenv

load_dotenv()

# Constants
ALGORITHM = "aes-256-gcm"
IV_LENGTH = 12
AUTH_TAG_LENGTH = 16

# Secret Keys (from environment variables)
def get_key(env_var):
    key_hex = os.getenv(env_var, "").strip()
    if not key_hex:
        raise ValueError(f"Missing {env_var} in .env file")
    try:
        return bytes.fromhex(key_hex)  # Convert HEX to bytes
    except ValueError as e:
        raise ValueError(f"Invalid hex value in {env_var}: {key_hex}") from e

# Load encryption keys
KEY1 = get_key("KEY1")
KEY2 = get_key("KEY2")
KEY3 = get_key("KEY3")
KEY4 = get_key("KEY4")
SALT = get_key("SALT")  # SALT must also be hex

# Read passphrase as plain text
PASSPHRASE = os.getenv("PASSPHRASE", "").encode()
if not PASSPHRASE:
    raise ValueError("Missing PASSPHRASE in .env file")

# Key Derivation Function (Argon2)
def derive_key():
    hasher = argon2.PasswordHasher(
        time_cost=3,                # Number of iterations
        memory_cost=65536,          # Memory usage in KiB (64 MiB)
        parallelism=4,              # Number of threads
        hash_len=32,                # 32 bytes = 256 bits
        salt_len=len(SALT),         # Length of the salt
        type=argon2.Type.ID,        # Use Argon2id
    )
    
    # Hash the passphrase with the salt
    argon2_hash = hasher.hash(PASSPHRASE, salt=SALT)
    
    # Extract the raw hash (last part after '$')
    raw_hash_base64 = argon2_hash.split('$')[-1]
    
    # Add padding if necessary
    padding = len(raw_hash_base64) % 4
    if padding:
        raw_hash_base64 += '=' * (4 - padding)
    
    # Decode the Base64-encoded hash into bytes
    derived_key = base64.b64decode(raw_hash_base64)
    return derived_key

# AES Encryption
def aes_encrypt(data: str, key: bytes) -> str:
    iv = os.urandom(IV_LENGTH)
    cipher = Cipher(algorithms.AES(key), modes.GCM(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    encrypted = encryptor.update(data.encode("utf-8")) + encryptor.finalize()
    auth_tag = encryptor.tag
    # Combine IV, auth tag, and encrypted data
    return f"{iv.hex()}:{auth_tag.hex()}:{encrypted.hex()}"

# AES Decryption
def aes_decrypt(encrypted_data: str, key: bytes) -> str:
    try:
        iv_hex, auth_tag_hex, encrypted_hex = encrypted_data.split(":")
        iv = bytes.fromhex(iv_hex)
        auth_tag = bytes.fromhex(auth_tag_hex)
        encrypted = bytes.fromhex(encrypted_hex)
        cipher = Cipher(algorithms.AES(key), modes.GCM(iv, auth_tag), backend=default_backend())
        decryptor = cipher.decryptor()
        decrypted = decryptor.update(encrypted) + decryptor.finalize()
        return decrypted.decode("utf-8")
    except Exception as e:
        print(f"Decryption failed: {e}")
        raise

# Encrypt Password
def encrypt_pass(password: str) -> str:
    derived_key = derive_key()
    first_layer = aes_encrypt(password, KEY1)
    second_layer = aes_encrypt(first_layer, KEY2)
    third_layer = aes_encrypt(second_layer, KEY3)
    fourth_layer = aes_encrypt(third_layer, KEY4)
    final_encrypted = aes_encrypt(fourth_layer, derived_key)
    return final_encrypted

# Decrypt Password
def decrypt_pass(encrypted_data: str) -> str:
    derived_key = derive_key()
    fourth_decryption = aes_decrypt(encrypted_data, derived_key)
    third_decryption = aes_decrypt(fourth_decryption, KEY4)
    second_decryption = aes_decrypt(third_decryption, KEY3)
    first_decryption = aes_decrypt(second_decryption, KEY2)
    return aes_decrypt(first_decryption, KEY1)

# Test the script
if __name__ == "__main__":
    password = "my_secure_password123456789mysecurepassword"
    encrypted = encrypt_pass(password)
    print(f"Encrypted: {encrypted}")

    decrypted = decrypt_pass(encrypted)
    print(f"Decrypted: {decrypted}")
