from jose import jwt
from datetime import datetime,timedelta
from dotenv import load_dotenv
import os

load_dotenv()

secret = os.getenv("SECRET")
algorithm = "HS256"
expires = 60


def createToken(data:dict):
    encoded = data.copy()
    expireTime = datetime.utcnow() + timedelta(minutes=expires)
    encoded.update({"exp":expireTime})
    token = jwt.encode(encoded,secret,algorithm=algorithm)
    return token
