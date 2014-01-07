# -*- coding: utf-8 -*-

import os

from onepyssword.logic import (
    KEYCHAIN_ENV_KEY,
    get_keychain_items, load_keychain_item_data, get_encryption_key,
    unlock_encryption_key, decrypt_keychain_item_password,
)

__all__ = (
    'test_get_keychain_items',
    'test_load_keychain_item_data',
    'test_unlock_encryption_key_invalid_password',
    'test_unlock_encryption_key_valid_password',
    'test_decrypt_keychain_item_password',
)


os.environ[KEYCHAIN_ENV_KEY] = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    'data', '1Password.agilekeychain'
)


def test_get_keychain_items():
    items = get_keychain_items()
    assert type(items) == dict
    assert 'foobar' in items
    assert 'atof' in items


def test_load_keychain_item_data():
    items = get_keychain_items()
    foobar_identifier = items['foobar'].identifier

    data = load_keychain_item_data(foobar_identifier)
    assert type(data) == dict

    expected_keys = [
        'uuid', 'location', 'updatedAt', 'createdAt', 'openContents',
        'locationKey', 'keyID', 'encrypted', 'title', 'typeName',
    ]
    expected_keys.sort()
    data_keys = list(data.keys())
    data_keys.sort()
    assert data_keys == expected_keys


def _test_get_encryption_key(item):
    foobar_identifier = item.identifier
    data = load_keychain_item_data(foobar_identifier)

    encryption_key = get_encryption_key(
        data.get('keyID'), data.get('securityLevel')
    )
    assert encryption_key is not None
    return encryption_key


def test_unlock_encryption_key_invalid_password():
    items = get_keychain_items()
    item = items['foobar']
    encryption_key = _test_get_encryption_key(item)

    decrypted_encryption_key = unlock_encryption_key('password', encryption_key)
    assert decrypted_encryption_key is None


def test_unlock_encryption_key_valid_password():
    items = get_keychain_items()
    item = items['foobar']
    encryption_key = _test_get_encryption_key(item)

    decrypted_encryption_key = unlock_encryption_key('badger', encryption_key)
    assert decrypted_encryption_key is not None


def test_decrypt_keychain_item_password():
    items = get_keychain_items()
    item = items['foobar']
    foobar_identifier = item.identifier
    data = load_keychain_item_data(foobar_identifier)
    encryption_key = _test_get_encryption_key(item)

    decrypted_encryption_key = unlock_encryption_key('badger', encryption_key)
    assert decrypted_encryption_key is not None

    password = decrypt_keychain_item_password(
        data['encrypted'], decrypted_encryption_key, item.type
    )
    assert password == 'foobar'
