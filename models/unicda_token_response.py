from pydantic import BaseModel


class UNICDATokenResponse(BaseModel):
    token: str
    expiry: str
    message: str
