# command to create secret key (terminal) - openssl rand -hex 32
JWT_SECRET_KEY = "5dfc621ab92a9ccbb078fa92eb124b3bd0b11be77a6de48c8e31d9552cae4135"
JWT_ALGORITHM = "HS256"
JWT_EXPIRATION_TIME_MINUTES = 60 * 24 * 5

TOKEN_DESCRIPTION="If user and pass are correct it returns the JWT Token"
TOKEN_SUMMARY="Takes user and pass and returns JWT Token"

ISBN_DESCRIPTION="Unique Identifier of a Book"