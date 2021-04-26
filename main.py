from fastapi import FastAPI, Body, Header, File
from routes.v1 import app_v1
from routes.v2 import app_v2
from starlette.requests import Request
from starlette.responses import Response
from utils.security import check_jwt_token
from starlette.status import HTTP_401_UNAUTHORIZED
from datetime import datetime

app = FastAPI()

app.mount("/v1", app_v1)
app.mount("/v2", app_v2)


@app.middleware("http")
async def middleware(request: Request, call_next):
    start_time = datetime.utcnow()
    # modify request
    if not str(request.url).__contains__("/token"):
        jwt_token = request.headers["Authorization"].split("Bearer ")[1] # get token
        is_valid = check_jwt_token(jwt_token)
        if not is_valid:
            return Response("Unauthorized", status_code = HTTP_401_UNAUTHORIZED)
    response = await call_next(request) # async fx, this fx does nothing by now
    execution_time = (datetime.utcnow() - start_time).microseconds
    # modify response
    response.headers["x-execution-time"] = str(execution_time) # header has to be a string
    return response
