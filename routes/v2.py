from fastapi import FastAPI, Body, Header, File
from models.users import User
from starlette.status import HTTP_201_CREATED
from starlette.responses import Response


app_v2 = FastAPI(openapi_prefix="/v2")

# add custom headers in the user endpoint, defined inside function post_user
@app_v2.post("/user", status_code=HTTP_201_CREATED)
# when sending the request we use x-custom, _ becomes -
async def post_user(user: User, x_custom: str = Header(...)):
    return {"request body": user, "request custom header" : x_custom, "version" : "v2"}

