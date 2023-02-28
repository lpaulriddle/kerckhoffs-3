class Key:
    def decrypt(self, cipher_words):
        running_rotation = 0
        plaintext = ""
        for word in cipher_words:
            (plaintext_char, rotation) = self.key_dict[word]
            plaintext_char = chr((ord(plaintext_char) - ord('a') - running_rotation) % 26 + ord('a'))
            running_rotation -= rotation
            plaintext += plaintext_char
        return plaintext

    def __init__(self, key_dict):
        self.key_dict = key_dict
