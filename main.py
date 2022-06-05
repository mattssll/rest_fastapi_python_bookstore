from fastapi import FastAPI, File, Depends, HTTPException
from routes.v1 import app_v1
from routes.v2 import app_v2
from starlette.requests import Request
from starlette.responses import Response
from utils.security import check_jwt_token
from starlette.status import HTTP_401_UNAUTHORIZED
from datetime import datetime
from fastapi.security import OAuth2PasswordRequestForm
from utils.security import authenticate_user, create_jwt_token
from models.jwt_user import JWTUser
from utils.const import TOKEN_SUMMARY, TOKEN_DESCRIPTION

app = FastAPI(title="Bookstore API Swagger Documentation", description="API That manages a bookstore", version="1.0.0")

app.include_router(app_v1, prefix="/v1", dependencies=[Depends(check_jwt_token)])
app.include_router(app_v2, prefix="/v2", dependencies=[Depends(check_jwt_token)])


@app.post("/token", summary=TOKEN_SUMMARY , description= TOKEN_DESCRIPTION)
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
    return {"access_token" : jwt_token}

@app.middleware("http")
async def middleware(request: Request, call_next):
    start_time = datetime.utcnow()
    # modify request
    if not any(word in str(request.url) for word in ["/token", "/docs", "/openapi.json"]):
        try:
            jwt_token = request.headers["Authorization"].split("Bearer ")[1] # get token
            is_valid = check_jwt_token(jwt_token)
        except Exception as e:
            is_valid = False
        if not is_valid:
            return Response("Unauthorized", status_code = HTTP_401_UNAUTHORIZED)
    response = await call_next(request) # async fx, this fx does nothing by now
    execution_time = (datetime.utcnow() - start_time).microseconds
    # modify response
    response.headers["x-execution-time"] = str(execution_time) # header has to be a string
    return response
