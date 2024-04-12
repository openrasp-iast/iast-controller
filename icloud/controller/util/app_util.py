import base64
import hashlib
import random
import time


def generate_app_id(name):
    random_str = (
        "openrasp_app"
        + name
        + str(int(time.time() * 1e9))
        + str(random.randint(0, 10000))
    )
    sha1_hash = hashlib.sha1(random_str.encode()).hexdigest()
    return sha1_hash


def generate_secret(name, id):
    random_str = (
        "openrasp_app"
        + name
        + id
        + str(int(time.time() * 1e9))
        + str(random.randint(0, 10000))
    )
    sha256_hash = hashlib.sha256(random_str.encode()).digest()
    custom_b64 = base64.urlsafe_b64encode(sha256_hash).decode()  # 使用 URL 安全的 base64 编码

    return custom_b64.replace('=', 'a').replace('/', 'b').replace('+', 'c').replace('_', 'd').replace('-', 'f')[:45]


if __name__ == "__main__":
    name = "Test"
    id = generate_app_id(name)
    secret = generate_secret(name, id)
    print(name)
    print(id)
    print(secret)

# Default
# 36f45601c9111636f76519e7d30b9417beb8b868
# 1UDTwKcN1ak0smftbSyrDPpLOGUz5coIxAUmf0r9ZsEa
