# -*- coding: utf-8 -*-

import functools
import os
import json
from base64 import b64decode
from collections import namedtuple

from Crypto.Cipher import AES
from Crypto.Hash import MD5
from pbkdf2_ctypes import pbkdf2_bin

from onepyssword.py3k import PY3, b

__all__ = (
    'get_keychain_items',
    'load_keychain_item_data',
    'decrypt_keychain_item_password',

    'get_encryption_key',
    'unlock_encryption_key',
)


KEYCHAIN_ENV_KEY = 'ONEPYSSWORD_KEYCHAIN'
DEFAULT_KEYCHAIN_PATH = '~/Dropbox/1Password/1Password.agilekeychain'


KeychainItem = namedtuple('KeychainItem', 'type, identifier')
EncryptionKey = namedtuple('EncryptionKey', 'level, validation, iterations, encrypted_key')
SaltyString = namedtuple('SaltyString', 'salt, data')


def get_keychain_items():
    path = os.path.join(get_keychain_path(), 'data', 'default', 'contents.js')
    with open(path, 'r') as f:
        item_list = json.load(f)

    return dict(
        (item[2], KeychainItem(type=item[1], identifier=item[0])) for item in item_list
    )


def load_keychain_item_data(identifier):
    filename = '{0}.1password'.format(identifier)
    path = os.path.join(get_keychain_path(), 'data', 'default', filename)
    with open(path, 'r') as f:
        data = json.load(f)

    return data


def decrypt_keychain_item_password(b64_data, decrypted_key, item_type):
    decrypted_json = decrypt_encryption_key(b64_data, decrypted_key)
    decrypted_json = decrypted_json.decode('utf-8') if PY3 else decrypted_json

    try:
        data = json.loads(decrypted_json)
    except ValueError:
        data = json.loads(decrypted_json[:-16])

    if item_type == 'webforms.WebForm':
        for field in data['fields']:
            if field.get('designation') == 'password' or field.get('name') == 'Password':
                return field['value']
    elif item_type in ('passwords.Password', 'wallet.onlineservices.GenericAccount', ):
        return data['password']
    else:
        return None


def get_encryption_keys():
    path = os.path.join(get_keychain_path(), 'data', 'default', 'encryptionKeys.js')
    with open(path, 'r') as f:
        keys_data = json.load(f)

    return dict(
        (key_data['identifier'], init_encryption_key(key_data)) for key_data in keys_data['list']
    )


def init_encryption_key(key_data):
    minimum_iterations = 1000

    return EncryptionKey(
        level=key_data['level'],
        validation=key_data['validation'],
        iterations=max(int(key_data['iterations']), minimum_iterations),
        encrypted_key=get_santy_string(key_data['data'])
    )


def get_encryption_key(key_id, key_level):
    encryption_keys = get_encryption_keys()

    if key_id:
        return encryption_keys[key_id]
    elif key_level:
        for key in encryption_keys.values():
            if key.level == key_level:
                return key

    return None


def get_santy_string(base64_encoded_string):
    salted_prefix = b('Salted__')
    zero_init_vector = b('\x00') * 16

    decoded_data = b64decode(base64_encoded_string)
    if decoded_data.startswith(salted_prefix):
        return SaltyString(salt=decoded_data[8:16], data=decoded_data[16:])
    return SaltyString(salt=zero_init_vector, data=decoded_data)


def unlock_encryption_key(password, encryption_key):
    key, iv = derive_pbkdf2(password, encryption_key.encrypted_key.salt, encryption_key.iterations)

    decrypted_key = aes_decrypt(key, iv, encryption_key.encrypted_key.data)
    decrypted_key_valid = decrypt_encryption_key(encryption_key.validation, decrypted_key) == decrypted_key
    return decrypted_key if decrypted_key_valid else None


def decrypt_encryption_key(b64_data, decrypted_key):
    encrypted = get_santy_string(b64_data)
    key, iv = derive_openssl(decrypted_key, encrypted.salt)
    return aes_decrypt(key, iv, encrypted.data)


def derive_pbkdf2(password, salt, iterations):
    key_and_iv = pbkdf2_bin(b(password), salt, iterations=iterations, keylen=32)
    return key_and_iv[0:16], key_and_iv[16:]


def derive_openssl(key, salt):
    key = key[0:-16]
    key_and_iv = b('')
    prev = b('')
    while len(key_and_iv) < 32:
        prev = MD5.new(prev + key + salt).digest()  # ?
        key_and_iv += prev
    return key_and_iv[0:16], key_and_iv[16:]


def aes_decrypt(key, iv, encrypted_data):
    aes = AES.new(key, mode=AES.MODE_CBC, IV=iv)
    decrypted = aes.decrypt(encrypted_data)

    padding_size = decrypted[-1]
    padding_size = padding_size if PY3 else ord(padding_size)

    if padding_size >= 16:
        return decrypted
    return decrypted[:-padding_size]


_get_keychain_path = lambda: os.path.expanduser(
    os.environ.get(KEYCHAIN_ENV_KEY, DEFAULT_KEYCHAIN_PATH)
)
if PY3:
    get_keychain_path = functools.lru_cache()(_get_keychain_path)
else:
    get_keychain_path = _get_keychain_path
