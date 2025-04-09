from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError , InvalidHashError

ph = PasswordHasher()

def hashPassword(password: str) -> str:
    return ph.hash(password)

def verifyPassword(hashedPassword: str, enteredPassword: str) -> bool:
    try:
        ph.verify(hashedPassword, enteredPassword)
        return True
    except (VerifyMismatchError, InvalidHashError):
        return False
