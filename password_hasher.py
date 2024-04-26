import hashlib
import secrets

class PasswordHasher:
    @staticmethod
    def hash_password(password, salt):
        return hashlib.sha256((password + salt).encode()).hexdigest()

    @staticmethod
    def generate_salt():
        return secrets.token_hex(16)  # 16 bytes = 32 characters
