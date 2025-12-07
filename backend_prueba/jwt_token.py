import jwt, datetime, os
from dotenv import load_dotenv

load_dotenv()

def crear_token(usuario):
    payload = {
        "usuario_id": usuario["usuario_id"],
        "email": usuario["email"],
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }
    token = jwt.encode(
        payload,
        os.getenv("JWT_SECRET"),
        algorithm=os.getenv("JWT_ALGORITHM")
    )
    return token