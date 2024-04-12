# TODO 输入字，输出hash
import hashlib


def hash_string(word):
    return hashlib.sha256(word.encode("utf-8")).hexdigest()


def get_iast_url(app_id):
    return ""
