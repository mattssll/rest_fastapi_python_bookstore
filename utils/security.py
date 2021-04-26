# below's library to hash our passwords (instead of having it in plaintext)
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from models.jwt_user import JWTUser
from datetime import datetime, timedelta
from utils.const import JWT_EXPIRATION_TIME_MINUTES, JWT_ALGORITHM, JWT_SECRET_KEY
import jwt
from fastapi import Depends, HTTPException
from starlette.status import HTTP_401_UNAUTHORIZED
import time
# One function will hash our password and another will check if the
# plain password is the same as the hashed password
pwd_context = CryptContext(schemes=["bcrypt"])
oauth_schema = OAuth2PasswordBearer(tokenUrl="/token") # gives token to user
jwt_user1 = {
    "username" : "user1",
    "password" : "$2b$12$l1SyAcdDKVdagwtR0aUEQ.HYu8WMwF0njQUycOQ14Zg2PpL9L8ft.", # hashed password for admin
    "disabled" : "false",
    "role" : "admin"
}
dummie_jwt_user1 = JWTUser(**jwt_user1) # kind of instantiating

# takes password in plaintext and hashes it
def get_hashed_password(password):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    """
    This function verifies if the password sent by the user
    matches with the hashed_password in our app
    :param plain_password:
    :param hashed_password:
    :return: Returns the result of the validation (True for it matches, False for it doesn't)
    """
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except Exception as e:
        return False


# Authenticate username and password to give JWT Token
def authenticate_user(user: JWTUser):
    """
    This Function checks whether the user request has valid
    credentials, it checks if its username and password are correct
    We use our verify_password to check the hashed password
    :param username:
    :param password:
    :return: the user if the validation passed, or None if it didn't pass
    """
    if dummie_jwt_user1.username == user.username:
        if verify_password(user.password, dummie_jwt_user1.password):
            user.role = "admin"
            return user
    return None


def create_jwt_token(user: JWTUser):
    """
    Creates the JWT Token that can be used to authenticate and access our API.
    It creates the JWT Token Payload with our user, role, and exp time of the token
    :param user:
    :return: Returns our encoded JWT_Token
    """
    expiration_time = datetime.utcnow() + timedelta(minutes=JWT_EXPIRATION_TIME_MINUTES)
    jwt_payload = {
        "sub" : user.username,
        "role" : user.role,
        "exp" : expiration_time
    }
    jwt_token = jwt.encode(jwt_payload, JWT_SECRET_KEY, JWT_ALGORITHM)
    return jwt_token



def check_jwt_token(token: str = Depends(oauth_schema)): # takes info from request auth header
    """
    Checks whether our JWT Token is valid or not
    It also calls the final_checks function to check the role
    :param token:
    :return: True if the JWT Token is valid, false if not
    """
    try:
        jwt_payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=JWT_ALGORITHM)
        username = jwt_payload.get("sub")
        role = jwt_payload.get("role")
        expiration = jwt_payload.get("exp")
        if time.time() < expiration: # epoch time, jwt token uses it too
            if dummie_jwt_user1.username == username:
                return final_checks(role)
    except Exception as e:
        return False
    raise False
# Check additional constraints and return final results (good or bad request)
def final_checks(role:str):
    if role == "admin":
        return True
    else:
        return False

print(get_hashed_password("admin"))