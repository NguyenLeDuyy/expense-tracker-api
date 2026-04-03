from jose import jwt
import datetime

from models.user import User

SECRET_KEY = "LeoNguyen"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
ALGORITHM = "HS256"

def create_access_token(user_login: User):
    now = datetime.datetime.now(datetime.timezone.utc)

    payload =  {
        "user_id": user_login.id,
        "email": user_login.email,
        "iat": now,
        "exp": now + datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token