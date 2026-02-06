import jwt
import uuid
from datetime import datetime, timezone, timedelta
from fastapi import HTTPException

def generate_id():
    return str(uuid.uuid4())

def current_time():
    return datetime.now(timezone.utc)

class JWTManager:
    def __init__(self, secret_key: str, algorithm: str = "HS256", access_token_expire_minutes: int = 1, refresh_token_expire_minutes: int = 2):
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.access_token_expire_minutes = access_token_expire_minutes
        self.refresh_token_expire_minutes = refresh_token_expire_minutes

    def create_access_token(self, user_id: str):
        jti = generate_id()
        to_encode = {
            "sub": str(user_id),
            "jti": str(jti),
            "type": "access",
            "iat": current_time(),
            "exp": current_time() + timedelta(minutes=self.access_token_expire_minutes)
        }
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt, jti

    def create_refresh_token(self, user_id: str):
        jti = generate_id()
        to_encode = {
            "sub": str(user_id),
            "jti": str(jti),
            "type": "refresh",
            "iat": current_time(),
            "exp": current_time() + timedelta(minutes=self.refresh_token_expire_minutes)
        }
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt, jti

    def decode_token(self, token: str):
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token expired")
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail="Invalid token")