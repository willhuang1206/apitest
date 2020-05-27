import sys
import hashlib

def encrypt(str):
    return hashlib.md5(str.encode("utf-8")).hexdigest()

if __name__ == '__main__':
    str="huangrong-F9C0A57D945E9CD70105A6A27E544D2E-autotest-0183701f18045024eb3a120eb4bf1d7b"
    print(encrypt(str))
