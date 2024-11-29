from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi.security.oauth2 import OAuth2PasswordBearer
from . import schemas, database, models
from sqlalchemy.orm import session


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
# secret key
#algo
# experied time.
SECRET_KEY = "BD007663145FFB668C2A7F1A7B451CF8"
ALGORITHM = "HS256" 
ACCESS_TOKEN_EXPIRE_MINUTES = 60*24

def create_access_token(data:dict):
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, ALGORITHM)
    return encoded_jwt


def verify_access_token(token:str, credientials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, [ALGORITHM])
        # id: str = payload.get("user_id")
        id = payload.get("user_id")
        id=str(id)
        if id is None:
            raise credientials_exception

        token_data = schemas.Token_data(id=id)
    except JWTError:
        raise credientials_exception
    
    return token_data

def get_current_user(token= Depends(oauth2_scheme), db:session = Depends(database.get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"could not validate credentials", headers={"WWW-Authenticate": "Bearer"})
    # return verify_access_token(    def get_current_user(token:str= Depends(oauth2_scheme)):
        # Convert the token to a string if it's an integer
    if isinstance(token, int):
        token = str(token)

    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"could not validate credentials", headers={"WWW-Authenticate": "Bearer"})
    token = verify_access_token(token,credentials_exception )
    user = db.query(models.User).filter(models.User.id == token.id).first()
    return user