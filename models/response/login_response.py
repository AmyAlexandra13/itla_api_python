from pydantic import BaseModel


class LoginResponseModel(BaseModel):
    accessToken: str
    tokenType: str
