from pydantic import BaseModel

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

# Optional: Schema for data within the token (payload)
class TokenPayload(BaseModel):
    sub: str | None = None # Subject (user identifier)
    # Add other fields like role if needed when decoding
    # role: str | None = None