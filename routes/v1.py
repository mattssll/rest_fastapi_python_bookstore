from fastapi import FastAPI, Body, Header, File, APIRouter
from models.user import User
from models.author import Author
from models.book import Book
from starlette.status import HTTP_201_CREATED, HTTP_401_UNAUTHORIZED
from starlette.responses import Response
# For the client to be able to consume our api he has to pass a "authorization"
# "attribute" in the Header of the request containing "Bearer asuijaruoqw8928912389123iu" (Bearer + token)

app_v1 = APIRouter()

# tags in our endpoints group our APIs in the swagger documentation
@app_v1.get("/")
async def hello_world():
    return {"request body": "hello world from FastAPI"}

# add custom headers in the user endpoint, defined inside function post_user
@app_v1.post("/user", status_code=HTTP_201_CREATED, tags=["User"])
# when sending the request we use x-custom, _ becomes -
async def post_user(user: User, x_custom: str = Header(...)):
    return {"request body": user, "request custom header" : x_custom}

@app_v1.get("/user", tags=["User"])
async def get_user_validation(password: str):  # query parameters
    return {"query parameter": password}


# adding response_model, we tell our endpoint it will return a Book class
# path parameter below
@app_v1.get("/book/{isbn}", response_model=Book, response_model_include=["isbn","name", "year"], tags=["Book"])
async def get_book_with_isbn(isbn: int):
    author_dict = {
        "isbn" : 1,
        "name" : "author1",
        "books" : ["book1", "book2"]
    }
    author1 = Author(**author_dict)
    book_dict = {
        "id" : 1,
        "name" : "book1",
        "year" : 2019,
        "author" : author1
    }
    book1 = Book(**book_dict)
    return book1 # with that we can easily return our full object that we want to get


@app_v1.get("/author/{id}/books", tags=["Author"])
async def get_authors_books(id: int, order: str = "asc"):  # query parameters
    return {"query parameter": order + str(id)}


@app_v1.patch("/author/name", tags = ["Author"])
# FAST API knows that this name api is taken from body of request (Body(...))
# embed = True let us send through our request the parameter name and its value (otherwise it will fail if we
# also send the key)
async def patch_author_name(name: str = Body(..., embed=True)):
    return {"name in body": name}

# Body is used for parameters that are NOT in our MODELs
@app_v1.post("/user/author", tags = ["Author"])
async def post_user_and_author(user: User, author: Author, bookstore_name: str = Body(..., embed=True)):
    return {"user" : user, "author" : author, "bookstore_name" : bookstore_name}

# response will return to user a response in the header
@app_v1.post("/user/photo", tags = ["User"]) # this will take multipart form as input for the picture
async def upload_user_photo(response: Response, profile_photo: bytes = File(...)):
    response.headers["x-file-size"] = str(len(profile_photo))
    response.set_cookie(key="cookie-api", value="test")
    return {"file size" : len(profile_photo)}


