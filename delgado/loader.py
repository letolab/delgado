"""
JSON Loading utilities
"""
from json import loads
import delgado
from delgado.exceptions import Forbidden, InvalidFormat


def loader(string, allowed=None):
    allowed = allowed or delgado.config.get('allowed', [])
    try:
        obj = loads(string)
        return format_command(obj)
    except ValueError:
        msg = 'unable to parse unexpected input: %s' % repr(string)
        raise InvalidFormat(msg)
    for exe in obj.keys():
        if exe not in allowed:
            raise Forbidden('Executable %s, is not allowed' % exe)


def format_command(obj):
    try:
        if not obj:
            raise AttributeError
        executable = obj.keys()[0]
        arguments = obj[executable]
        return [executable] + arguments
    except AttributeError:
        msg = "JSON format should be like {'executable': [arguments]}" \
              " but received: %s" % repr(obj)
        raise InvalidFormat(msg)
