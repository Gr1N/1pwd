# -*- coding: utf-8 -*-

import argparse
import os
import sys
from difflib import get_close_matches
from getpass import getpass

import copypaste

from onepyssword.logic import (
    get_keychain_items, get_encryption_key, unlock_encryption_key,
    load_keychain_item_data, decrypt_keychain_item_password,
)
from onepyssword.py3k import PY2

__all__ = (
    'go',
)


COPY_CMD_ENV_KEY = 'ONEPYSSWORD_COPY_CMD'


if PY2:
    NoSuchFileOrDirectoryException = OSError
else:
    NoSuchFileOrDirectoryException = FileNotFoundError


def go(argv=sys.argv[1:], stdout=sys.stdout, stderr=sys.stderr):
    parser = argparse.ArgumentParser()
    parser.add_argument('item')
    parser.add_argument('-f', '--find', action='store_true', help='find item')
    parser.add_argument('-p', '--prompt', action='store_true',
                        help='print password')
    arguments = parser.parse_args(argv)

    item = arguments.item
    keychain_items = get_keychain_items()

    if arguments.find:
        find(keychain_items, item)
        return

    password = decrypt(keychain_items, item, stdout=stdout, stderr=stderr)
    if arguments.prompt:
        stdout.write('{0}\n'.format(password))
    else:
        copy(password, stdout=stdout, stderr=stderr)
        stdout.write('Password copied to clipboard!\n')


def decrypt(keychain_items, item, stdout=sys.stdout, stderr=sys.stderr):
    if item not in keychain_items:
        stderr.write('Item ({0}) not found!\n'.format(item))
        sys.exit(os.EX_DATAERR)

    try:
        password = getpass('Master password: ')
    except KeyboardInterrupt:
        stdout.write('\n')
        sys.exit(0)

    if not password:
        stderr.write('Plz enter master password!\n')
        sys.exit(os.EX_DATAERR)

    item = keychain_items[item]
    item_data = load_keychain_item_data(item.identifier)
    encryption_key = get_encryption_key(
        item_data.get('keyID'), item_data.get('securityLevel')
    )
    decrypted_encryption_key = unlock_encryption_key(password, encryption_key)
    if not decrypted_encryption_key:
        stderr.write('Incorrect master password!\n')
        sys.exit(os.EX_DATAERR)

    return decrypt_keychain_item_password(
        item_data['encrypted'], decrypted_encryption_key, item.type
    )


def find(keychain_items, item, stdout=sys.stdout, stderr=sys.stderr):
    keys = keychain_items.keys()
    matches = get_close_matches(item, keys, n=5, cutoff=0.3)
    if matches:
        stdout.write('Founded matches:\n')
        for m in matches:
            stdout.write('\t{0}\n'.format(m))


def copy(string, stdout=sys.stdout, stderr=sys.stderr):
    try:
        platform = sys.platform
        if platform not in ('darwin', 'linux', 'linux2',):
            copypaste.copy(string)
            return

        copy_cmd = os.environ.get(COPY_CMD_ENV_KEY)
        if not copy_cmd:
            copypaste.copy(string)
            return

        copy_cmd = copy_cmd.split(',')
        copypaste.copy(string, cmd=copy_cmd)
    except NotImplementedError:
        stderr.write('Sorry, copy command not supported for your platform.\n')
        sys.exit(os.EX_DATAERR)
    except NoSuchFileOrDirectoryException:
        stderr.write('Invalid copy command or tool for copy'
                     ' was not installed in your system.\n')
        sys.exit(os.EX_DATAERR)
