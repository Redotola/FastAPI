from jwt import encode

#Method to encode the token
def create_token(data: dict):
    token: str = encode(payload=data, key="my_secret_key", algorithm = "HS256")
    return token