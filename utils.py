from flask import jsonify, request
from flask.ext.babel import gettext as _
from simplecrypt import encrypt as _encrypt, decrypt as _decrypt
from binascii import hexlify, unhexlify
import config
import time
import cgi
from sqlalchemy import inspect

import hashlib

def json_data(data):
    return jsonify(dict(data=data))

def json_error(type, messages):
    if not isinstance(messages, list):
        messages = [messages]
    return jsonify({"error": {"type": type, "messages": messages}}), 400

def json_error_unauthorized_access():
    return json_error(type='UNAUTHORIZED_ACCESS', messages=_('Unauthorized access'))

def json_error_invalid_request():
    return json_error(type='INVALID_REQUEST', messages=_('Invalid request'))

def json_error_database():
    return json_error(type='DATABASE_ERROR', messages=_('Database Error'))

def now_ms():
    return int(round(time.time() * 1000))

def encrypt(text):
    return hexlify(_encrypt(config.SECRET, text))

def decrypt(text):
    return _decrypt(config.SECRET, unhexlify(text))

def hash(text):
    sha256 = hashlib.sha256()
    sha256.update(text)
    return sha256.hexdigest()

def escape(text):
    return cgi.escape(text)


def unicode_truncate(s, length, encoding='utf-8'):
    encoded = s.encode(encoding)[:length]
    return encoded.decode(encoding, 'ignore')

"""
Return the foreign key name based on the current class of obj
"""
def get_remote_side(obj, name):
    _remote_side_name = None
    attribute_name = '_remote_side_' + name
    try:
        _remote_side_name = getattr(obj, attribute_name)
    except AttributeError:
        pass
    
    if not _remote_side_name:
        cls = obj.__class__
        inspect(cls)
        ref = getattr(cls, name)
        remote_side = list(ref.property.remote_side)
        remote_side = remote_side[0]
        _remote_side_name = remote_side.name
        setattr(obj, attribute_name, _remote_side_name)
        
    return _remote_side_name

"""
Return the class remote side class of a relationship based on the current class of obj
"""
def get_remote_side_class(obj, name):
    _remote_side_class = None
    attribute_name = '_remote_side_class_' + name

    try:
        _remote_side_class = getattr(obj, attribute_name)
    except AttributeError:
        pass

    if not _remote_side_class:
        cls = obj.__class__
        inspect(cls)
        ref = getattr(cls, name)
        _remote_side_class = ref.property.mapper.class_
        setattr(obj, attribute_name, _remote_side_class)

    return _remote_side_class

"""
Process the tags param sent from client
"""
def process_tags_input(tags):
    return set([tag['name'].lower() for tag in tags])

"""
Turn -date_created to date_created DESC and date_created to date_created ASC
"""
def process_order_input(order):
    if order:
        order = order.split(",")
        order_strings = []
        for o in order:
            if o[0] == '-':
                order_strings.append(o[1:] + ' DESC')
            else:
                order_strings.append(o + ' ASC')
        order_strings = ", ".join(order_strings)
    else:
        order_strings = None

    return order_strings