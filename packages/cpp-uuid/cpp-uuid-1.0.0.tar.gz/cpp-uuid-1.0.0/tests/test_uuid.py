import uuid
from unittest import TestCase

import cpp_uuid

uuid4_fixture = 'c5fcf05c-6320-47ec-98c0-be84fdb1c321'
uuid4_other_fixture = 'a85144b4-255b-4484-8afe-69feb227e89c'
bytes_fixture = b'\xc5\xfc\xf0\\c G\xec\x98\xc0\xbe\x84\xfd\xb1\xc3!'

uuid4 = cpp_uuid.UUID(uuid4_fixture)
std_uuid4 = uuid.UUID(uuid4_fixture)
other_uuid4 = cpp_uuid.UUID(uuid4_other_fixture)
other_std_uuid4 = cpp_uuid.UUID(uuid4_other_fixture)


class TestUUID(TestCase):
    def test_uuid_from_args(self) -> None:
        self.assertEqual(uuid4_fixture, str(cpp_uuid.UUID(uuid4_fixture)))

    def test_uuid_from_hex(self) -> None:
        self.assertEqual(uuid4_fixture, str(cpp_uuid.UUID(hex=uuid4_fixture)))

    def test_uuid_from_bytes(self) -> None:
        self.assertEqual(bytes_fixture, cpp_uuid.UUID(bytes=bytes_fixture).bytes)

    def test_uuid_from_std_uuid4(self) -> None:
        some_std_uuid4 = uuid.uuid4()
        self.assertEqual(str(some_std_uuid4), str(cpp_uuid.UUID(str(some_std_uuid4))))

    def test_std_uuid_from_uuid4(self) -> None:
        some_uuid4 = cpp_uuid.uuid4()
        self.assertEqual(str(some_uuid4), str(uuid.UUID(str(some_uuid4))))

    def test_bytes(self) -> None:
        self.assertEqual(uuid.UUID(bytes=bytes_fixture).bytes, cpp_uuid.UUID(bytes=bytes_fixture).bytes)

    def test_hash(self) -> None:
        self.assertEqual(hash(cpp_uuid.UUID(bytes=bytes_fixture)), hash(cpp_uuid.UUID(bytes=bytes_fixture)))

    def test_compare_equal(self) -> None:
        some_uuid4 = uuid.uuid4()
        self.assertEqual(cpp_uuid.UUID(str(some_uuid4)), cpp_uuid.UUID(str(some_uuid4)))

    def test_compare_equal_with_std_uuid(self) -> None:
        self.assertEqual(uuid4, cpp_uuid.UUID(uuid4_fixture))
        self.assertEqual(uuid4, std_uuid4)
        self.assertNotEqual(uuid4, other_uuid4)
        self.assertNotEqual(uuid4, other_std_uuid4)

    def test_compare_greater(self) -> None:
        self.assertGreater(uuid4, other_uuid4)
        self.assertGreater(std_uuid4, other_std_uuid4)
        self.assertGreater(uuid4, other_std_uuid4)

    def test_compare_less_or_equal(self) -> None:
        self.assertLessEqual(other_uuid4, uuid4)
        self.assertLessEqual(other_std_uuid4, std_uuid4)
        self.assertLessEqual(other_std_uuid4, uuid4)
