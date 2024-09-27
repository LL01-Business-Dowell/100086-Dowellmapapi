import jwt
from datetime import datetime, timedelta
import os

auth_jwt_config = {
    'JWT_SECRET_KEY': os.getenv("JWT_SECRET_KEY", "your_secret_key"),
    'JWT_ALGORITHM': os.getenv("JWT_ALGORITHM", "HS256"),
    'JWT_ALLOW_REFRESH': True,
    'JWT_EXPIRATION_DELTA': timedelta(days=2),
    'JWT_REFRESH_EXPIRATION_DELTA': timedelta(days=7),
}

class JWTUtils:
    def __init__(self):
        self.secret_key = auth_jwt_config['JWT_SECRET_KEY']
        self.algorithm = auth_jwt_config['JWT_ALGORITHM']
        self.expiry_delta = auth_jwt_config['JWT_EXPIRATION_DELTA']
        self.refresh_expiry_delta = auth_jwt_config['JWT_REFRESH_EXPIRATION_DELTA']

    def generate_jwt_tokens(self, data):
        access_payload = {
            'exp': datetime.utcnow() + self.expiry_delta,
            **data
        }
        access_token = jwt.encode(access_payload, self.secret_key, algorithm=self.algorithm)

        refresh_payload = {
            'exp': datetime.utcnow() + self.refresh_expiry_delta,
            **data
        }
        refresh_token = jwt.encode(refresh_payload, self.secret_key, algorithm=self.algorithm)

        return {
            'access_token': access_token,
            'refresh_token': refresh_token
        }

    def decode_jwt_token(self, token):
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError) as error:
            return None
