from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"])


def get_hashed_password(password): # takes pwd in plaintext
    return pwd_context.hash(password)

password = "admin"
print(get_hashed_password(password))