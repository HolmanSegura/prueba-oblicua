import datetime

import jwt

from config import JWT_SECRET, JWT_ALGORITHM


def crear_token(usuario):
    """
    Crea y devuelve un token JWT para el usuario indicado.
    """
    payload = {
        "usuario_id": usuario["usuario_id"],
        "email": usuario["email"],
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1),
    }

    token = jwt.encode(
        payload=payload,
        key=JWT_SECRET,
        algorithm=JWT_ALGORITHM,
    )

    return token
