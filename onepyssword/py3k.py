# -*- coding: utf-8 -*-

import sys

__all__ = (
    'PY2',
    'PY3',

    'b',
)


PY2 = sys.version_info[0] == 2
PY3 = sys.version_info[0] == 3


if PY3:
    def b(s):
        return s.encode('utf-8')
else:
    def b(s):
        return s
