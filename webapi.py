import base64
import json
import os
import binascii
import requests
from Crypto.Cipher import AES


# 原版API
def get_html_pre(url):
    hds = {'Cookie': 'os=pc; osver=Microsoft-Windows-8-Professional-build-9200-64bit; appver=1.5.0.75771;',
           'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)'
                         ' Chrome/35.0.1916.138 Safari/537.36',
           'Referer': 'http://music.163.com/'}
    # proxy = {
    #     'http': '221.0.232.13:61202'
    # }
    content = requests.get(url, headers=hds, timeout=20)
    html_data = content.json()
    return html_data


# 新版API加密算法
def create_secret_key(size):
    return binascii.hexlify(os.urandom(size))[:16]


def aes_encrypt(text, sec_key):
    pad = 16 - len(text) % 16
    text = text + pad * chr(pad)
    encrypt_aes = AES.new(sec_key, 2, '0102030405060708')
    cipher_text = encrypt_aes.encrypt(text)
    cipher_text = base64.b64encode(cipher_text).decode()
    return cipher_text


def rsa_encrypt(text, pub_key, modulus_in):
    text = text[::-1]
    rs = pow(int(binascii.hexlify(text), 16), int(pub_key, 16), int(modulus_in, 16))
    return format(rs, 'x').zfill(256)


def encrypted_request(text):
    modulus = '00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3a' \
              'b17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c9' \
              '3870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e8204' \
              '7b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7'
    nonce = '0CoJUm6Qyw8W8jud'
    pubkey = '010001'
    text = json.dumps(text)
    sec_key = create_secret_key(16)
    enc_text = aes_encrypt(aes_encrypt(text, nonce), sec_key)
    enc_key = rsa_encrypt(sec_key, pubkey, modulus)
    data = {
        'params': enc_text,
        'encSecKey': enc_key
    }
    return data


