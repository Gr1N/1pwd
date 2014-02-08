1pwd
====

A command line interface for `1Password <https://agilebits.com/onepassword>`_.

Install
-------

::

    pip install onepyssword


Command line usage
------------------

To get a password::

    % 1pwd github.com


By default this will look in ``~/Dropbox/1Password/1Password.agilekeychain``.
You can set your keychain path as an enviornment variable::

    % export ONEPYSSWORD_KEYCHAIN=/path/to/keychain


Only for UNIX like systems you can specify your own command for copy.::

    % export ONEPYSSWORD_COPY_CMD=xsel,-pi


License
-------

*1pwd* is licensed under the MIT license. See the license file for details.
