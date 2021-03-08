"""Useful Utils for the DHT Shopping Cart Service."""
import datetime
import json
import hashlib

# Hashing and Serializing utils


def hash_key(string, bit_size=64):
    """Hash string into a 64-bit size integer."""
    return int(hashlib.sha1(string.encode("utf-8")).hexdigest(), 16) % (2 ** bit_size)


def serialize_value(value):
    """Convert object into a byte array."""
    return bytearray(json.dumps(value).encode("utf-8"))


def deserialize_value(serialized_value):
    """Decode bytes back into an object."""
    return json.loads(serialized_value.decode("utf-8"))


# Datetime utils


def epoch_to_datetime(epoch):
    """Util from epoch seconds to python object."""
    return datetime.datetime.utcfromtimestamp(epoch)


def datetime_to_epoch(dt):
    """Util from python object datetime to epoch seconds."""
    return int(dt.timestamp())


def datetime_to_string(dt):
    """Util to get a string datetime from python datetime."""
    return dt.strftime("%Y-%m-%d %H:%M:%S")


def string_to_datetime(string):
    """Util to python datetime from datetime string."""
    return datetime.datetime.strptime(string, "%Y-%m-%d %H:%M:%S")
