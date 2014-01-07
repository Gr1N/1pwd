1pwd
====

A command line interface for [1Password](https://agilebits.com/onepassword).

Install
-------

```shell
pip install onepyssword
```

Command line usage
------------------

To get a password:

```shell
1pwd github.com
```

By default this will look in ``~/Dropbox/1Password.agilekeychain``.
You can set your keychain path as an enviornment variable:

```shell
export ONEPYSSWORD_KEYCHAIN=/path/to/keychain
```

License
-------

*1pwd* is licensed under the MIT license. See the license file for details.
