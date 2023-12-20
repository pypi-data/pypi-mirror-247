import base64


def base64_url_decode(encoded: str) -> bytes:
    """
    Decode a base64 url string.

    Args:
        encoded (str): encoded string

    Returns:
            bytes: decoded bytes
    """
    remainder = len(encoded) % 4
    if remainder > 0:
        encoded += "=" * (4 - remainder)
    return base64.urlsafe_b64decode(encoded)
