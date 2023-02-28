class Key:
    def decrypt(self, cipher_words):
        running_rotation = 0
        plaintext = ""
        for word in cipher_words:
            plaintext_char = self.plaintext_char_dict[word]
            rotation = self.rotation_dict[word]
            plaintext_char = chr((ord(plaintext_char) - ord('a') - running_rotation) % 26 + ord('a'))
            running_rotation -= rotation
            plaintext += plaintext_char
        return plaintext

    def __init__(self, plaintext_char_dict, rotation_dict):
        self.plaintext_char_dict = plaintext_char_dict
        self.rotation_dict = rotation_dict
