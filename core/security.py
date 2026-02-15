import uuid
from datetime import datetime, timedelta, timezone

from jose import JWTError, jwt 
from passlib.context import CryptoContext

from config import settings
pwd_context = CryptoContext(schemes=["bcrypt"], deprecated="auto")


# Password Utilities
def hash_password(plain: str) -> str:
    return pwd_context.hash(plain)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)

# JWT Utilities 
def create_access_token(
        subject: str,
        expires_delta: timedelta | None=None,
        ) -> str:
            expire = datetime.now(timezone.utc) + (
                    expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
                    )
            payload = {"sub": subject, "exp": expire}
            return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM)


def decode_access_token(token: str) -> dict | None:
    # Return the token payload or None if invalid/expired 
    try:
        payload = jwt.decode(
                token, settings.SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
                )

        sub: str | None = payload.get("sub")
        if sub is None:
            return None
        # Validate UUID 
        uuid.UUID(sub)
        return {"sub": sub}
    except(JWTError, ValueError):
        return None

