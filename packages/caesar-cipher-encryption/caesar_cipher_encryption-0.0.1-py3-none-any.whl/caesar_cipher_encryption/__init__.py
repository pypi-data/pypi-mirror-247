"""Caesar Cipher Encryption Code"""


def caesar_cipher_encryption(plain_text: str, key: int) -> str:
    """
    Encrypts a plain text using the Caesar cipher encryption algorithm.

    Parameters:
        plain_text (str): The plain text to be encrypted.
        key (int): The encryption key.

    Returns:
        str: The encrypted text.
    """

    encrypted_text = ""
    key = key % 26
    for char in plain_text:
        if char.isalpha():
            if char.isupper():
                char = chr((ord(char) + key - 65) % 26 + 65)
            else:
                char = chr((ord(char) + key - 97) % 26 + 97)
        encrypted_text += char
    return encrypted_text
