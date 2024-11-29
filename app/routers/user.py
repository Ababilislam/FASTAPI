from fastapi import Depends, FastAPI, Response, status, HTTPException, APIRouter
from .. import models, schemas, utils
from sqlalchemy.orm import Session

from ..database import get_db

router = APIRouter(
    prefix="/users",
    tags = ["Users"]
)
@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.user_out)
def create_user(user:schemas.UserCreate, db: Session = Depends(get_db)):
    # hash the user passward
    existsuser = db.query(models.User).filter(models.User.emails == user.emails).first()
    # print(len(existsuser))
    if existsuser:
        print("Found")
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already exists")
    else:
        hash_passward = utils.hash(user.password)
        user.password = hash_passward
        # print(user)
        new_users = models.User(**user.dict())
        db.add(new_users)
        db.commit()
        db.refresh(new_users)
        return new_users


@router.get('/{id}', response_model=schemas.user_out)
def get_user(id:int, db:Session=Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with id : {id} does not exist")
    return user