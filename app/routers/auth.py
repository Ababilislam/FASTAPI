from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. import database, models, schemas, utils,oauth2

router = APIRouter(tags=['Authentacation'])

@router.post('/login', response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db:Session= Depends(database.get_db)):
    # username = ""
    # passward =""
    # user_credentials.emails = user_credentials.username
    user = db.query(models.User).filter(models.User.emails == user_credentials.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"Invalid Credentials")
    
    # create token.  
    access_token = oauth2.create_access_token({"user_id": user.id})

    # return the token
    return {"access_token": access_token, "token_type": "Bearer"}



    
          