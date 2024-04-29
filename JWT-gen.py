import jwt
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
import datetime

private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
    backend=default_backend()
)


private_pem = private_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.TraditionalOpenSSL,
    encryption_algorithm=serialization.NoEncryption()
)

payload = {
    "user_id": "123456",
    "username": "guz20262",
    "exp": datetime.datetime.now(datetime.UTC) + datetime.timedelta(seconds=3600)  # Expira en 1 hora
}

encoded_jwt = jwt.encode(payload, private_pem, algorithm="RS256")
print(encoded_jwt)


public_key = private_key.public_key()
public_pem = public_key.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
)


try:
    decoded_jwt = jwt.decode(encoded_jwt, public_pem, algorithms=["RS256"])
    print("JWT verificado exitosamente. Payload:", decoded_jwt)
except jwt.exceptions.InvalidTokenError:
    print("El JWT es inválido.")
