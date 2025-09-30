import jwt

secret_key = "ijasfdioj83rj89jafsd83jaf8"
algorithm = "HS256"

class CredentialsRepository:
    def decode_token(self, token: str) -> str:
        payload = jwt.decode(token, secret_key, [algorithm])
        return payload["nickname"]

    def make_token(self, nickname: str) -> str:
        payload = {
            "nickname": nickname,
        }
        token = jwt.encode(payload, secret_key, algorithm)
        return token

    def is_valid_token(self, token: str) -> bool:
        try:
            jwt.decode(token, secret_key, [algorithm])
            return True
        except jwt.ExpiredSignatureError:
            print("Срок годности токена")
            return False
        except Exception:
            print("Какая-то ошибка")
            return False
