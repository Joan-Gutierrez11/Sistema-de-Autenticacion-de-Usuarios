from passlib.context import CryptContext

PWD_CONTEXT = CryptContext(schemes=['bcrypt'], deprecated='auto')

def check_password(password_to_check: str, hash_password: str):
    return PWD_CONTEXT.verify(password_to_check, hash_password)

def get_hash_password(password: str):
    return PWD_CONTEXT.hash(password)
