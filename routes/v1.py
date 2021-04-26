from fastapi import FastAPI, Body, Header, File, Depends, HTTPException
from models.users import User
from models.author import Author
from models.book import Book
from starlette.status import HTTP_201_CREATED, HTTP_401_UNAUTHORIZED
from starlette.responses import Response
from fastapi.security import OAuth2PasswordRequestForm
from utils.security import authenticate_user, create_jwt_token
from models.jwt_user import JWTUser
# For the client to be able to consume our api he has to pass a "authorization"
# "attribute" in the Header of the request containing "Bearer asuijaruoqw8928912389123iu" (Bearer + token)

app_v1 = FastAPI(openapi_prefix="/v1")

@app_v1.get("/")
async def hello_world():
    return {"request body": "hello world from FastAPI"}


@app_v1.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    User sends it's username and password, if this validation is passed
    then our app generates a web token for us.
    :param form_data:
    :return: Returns the JSON Web Token if the username and password were correctly validated.
    """
    jwt_user_dict = {"username" : form_data.username,
                     "password" : form_data.password}
    jwt_user = JWTUser(**jwt_user_dict)
    user = authenticate_user(jwt_user)
    if user is None: # we are setting this in authentica_user if auth fails
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED)
    jwt_token = create_jwt_token(user)
    return {"token" : jwt_token}


# add custom headers in the user endpoint, defined inside function post_user
@app_v1.post("/user", status_code=HTTP_201_CREATED)
# when sending the request we use x-custom, _ becomes -
async def post_user(user: User, x_custom: str = Header(...)):
    return {"request body": user, "request custom header" : x_custom}


@app_v1.get("/user")
async def get_user_validation(password: str):  # query parameters
    return {"query parameter": password}

# adding response_model, we tell our endpoint it will return a Book class
# path parameter below
@app_v1.get("/book/name/{name}", response_model=Book, response_model_include=["name", "year"])
async def get_book_with_isbn(name: str):
    author_dict = {
        "name" : "author1",
        "book" : ["book1", "book2"]
    }
    author1 = Author(**author_dict)
    book_dict = {
        "isbn" : "isbn1",
        "name" : "book1",
        "year" : 2019,
        "author" :author1
    }
    book1 = Book(**book_dict)
    return book1 # with that we can easily return our full object that we want to get


@app_v1.get("/author/{id}/book")
async def get_authors_books(id: int, category: str, order: str = "asc"):  # query parameters
    return {"query parameter": order + category + str(id)}


@app_v1.patch("/author/name")
# FAST API knows that this name api is taken from body of request (Body(...))
# embed = True let us send through our request the parameter name and its value (otherwise it will fail if we
# also send the key)
async def patch_author_name(name: str = Body(..., embed=True)):
    return {"name in body": name}

# Body is used for parameters that are NOT in our MODELs
@app_v1.post("/user/author")
async def post_user_and_author(user: User, author: Author, bookstore_name: str = Body(..., embed=True)):
    return {"user" : user, "author" : author, "bookstore_name" : bookstore_name}

# response will return to user a response in the header
@app_v1.post("/user/photo") # this will take multipart form as input for the picture
async def upload_user_photo(response: Response, profile_photo: bytes = File(...)):
    response.headers["x-file-size"] = str(len(profile_photo))
    response.set_cookie(key="cookie-api", value="test")
    return {"file size" : len(profile_photo)}


