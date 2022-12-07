import unittest
import crc8


class CRC8TestCase(unittest.TestCase):
    def test_crc8_return_crc8(self):
        self.get_version_response = [0x37, 0x00, 0x15, 0x25, 0x00, 0x00, 0x00, 0x02, 0x00, 0x00, 0x0b, 0x56, 0x53, 0x41,
                                     0x20, 0x32, 0x2e, 0x30, 0x2e, 0x30, 0x2e, 0x37]
        self.get_version_send = [0x00, 0x00, 0x08, 0x25, 0x00, 0x00, 0x00, 0x02, 0x00]

        self.assertEqual(0x76, crc8.calculate(self.get_version_send, 1, 8))  # add assertion here


if __name__ == '__main__':
    unittest.main()
