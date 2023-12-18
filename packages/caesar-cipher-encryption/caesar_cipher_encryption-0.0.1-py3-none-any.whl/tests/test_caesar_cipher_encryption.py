from caesar_cipher_encryption import caesar_cipher_encryption
import unittest

class TestCaesarCipherEncryption(unittest.TestCase):
    def test_caesar_cipher_encryption(self):
        self.assertEqual(caesar_cipher_encryption("hello", 5), "mjqqt")

if __name__ == '__main__':
    unittest.main()
