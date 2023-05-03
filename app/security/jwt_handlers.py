from typing import List
from datetime import timedelta, datetime
from calendar import timegm

from jose import ExpiredSignatureError, jwt

from core.config import get_configuration

config = get_configuration()

SECRET = config.JWT_SECRET

ALGORITHM = "HS256"

JWT_TIME_EXP= config.JWT_EXP_TOKEN

JWT_TIME_REF= config.JWT_EXP_REFRESH


def create_jwt_token_time_grace(user_claims: dict, expires_delta: timedelta = None, grace_period: timedelta = None):
    data_to_encode = user_claims.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=JWT_TIME_EXP)

    if grace_period:
        grac_time = datetime.utcnow() + grace_period
    else:
        grac_time = datetime.utcnow() + timedelta(minutes=JWT_TIME_REF)
    
    data_to_encode.update({ "exp": expire, "grt": timegm(grac_time.utctimetuple()) })
    jwt_token = jwt.encode(data_to_encode, SECRET, ALGORITHM)
    return jwt_token

def decode_jwt_token(token: str):
    """
    This method only decode jwt token using a SECRET key.
    Args:
        token (str): jwt token to decode
    Returns:
        dict: the payload that contains token
    """

    return jwt.decode(token, SECRET)

def decode_jwt_token_time_grace(token: str):
    payload = jwt.decode(token, SECRET, options={'verify_exp': False})
    grace_period = int(payload['grt'])
    now = timegm(datetime.utcnow().utctimetuple())

    if grace_period < now:
        raise ExpiredSignatureError("Signature has expired.")

    return payload
