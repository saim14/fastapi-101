from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto") # default hash is bcrypt

def hash(password: str): 
    return pwd_context.hash(password)

def varify(password: str, hashed_password: str):
    return pwd_context.verify(password, hashed_password)