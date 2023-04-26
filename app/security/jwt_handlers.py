from typing import List
from datetime import timedelta, datetime
from calendar import timegm

from jose import ExpiredSignatureError, jwt


SECRET = "pass"
ALGORITHM = "HS256"

def create_access_token(user_claims: dict, expires_delta: timedelta = None, grace_period: timedelta = None):
    data_to_encode = user_claims.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=1)

    if grace_period:
        grac_time = datetime.utcnow() + grace_period
    else:
        grac_time = datetime.utcnow() + timedelta(minutes=10080)
    
    data_to_encode.update({ "exp": expire, "grt": timegm(grac_time.utctimetuple()) })
    jwt_token = jwt.encode(data_to_encode, SECRET, ALGORITHM)
    return jwt_token

def refresh_token(token: str, keys_claim: List[str]):
    payload = jwt.decode(token, SECRET, options={'verify_exp': False})
    grace_period = int(payload['grt'])
    now = timegm(datetime.utcnow().utctimetuple())

    if grace_period < now:
        raise ExpiredSignatureError("Signature has expired.")

    custom_claim = {}
    for key in keys_claim:
        custom_claim[key] = payload[key]

    return create_access_token(custom_claim)
