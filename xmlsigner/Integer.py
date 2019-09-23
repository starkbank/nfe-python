def intToBytes(num):
    """Return converted integer to bytestring.
    Args:
      num: integer, non-negative
    Returns:
      str: bytestring of binary data to represent `num`
    Raises:
      ValueError: `num` is not a non-negative integer
    """
    if not isNatural(num, includeZero=True):
        raise ValueError("%s is not a non-negative integer.")
    hexed = "%x" % num
    if len(hexed) % 2 == 1:
        hexed = '0%s' % hexed
    return hexed.decode('hex')


def isNatural(value, includeZero=False):
    """Return if value is a natural integer."""
    return all((
        isinstance(value, (int, long)),
        value >= 0,
        not (value == 0 and not includeZero),
    ))


def b64d(n):
    """Return decoded values from a base64 string."""
    b64 = n.decode("base64")

    return b64


def b64e(n):
    """Return encoded base64 string."""
    if type(n) in (int, long):
        n = intToBytes(n)

    return n.encode('base64').replace('\n', '')
