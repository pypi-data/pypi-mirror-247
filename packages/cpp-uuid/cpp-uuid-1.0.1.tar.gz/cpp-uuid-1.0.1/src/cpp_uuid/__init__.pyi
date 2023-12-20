"""UUID objects (universally unique identifiers) according to RFC 4122 written in C.

This module replaces uuid4() function and UUID object (class UUID) from Python-builtin library.
"""

class UUID:
    """Instances of the UUID class represent UUIDs v4.

    UUID objects are immutable, hashable, and usable as dictionary keys.
    UUID objects have single read-only attribute `bytes`.
    """

    def __init__(self, hex: str = None, bytes: bytes = None) -> None:
        """Create a UUID from either a string or a string of 16 bytes.

        :param hex: String of hex digits.
        :param bytes: UUID bytes.
        """

    @property
    def bytes(self) -> bytes:
        """UUID as a 16-byte string."""

def uuid4() -> UUID:
    """Generate a random UUID v4."""
