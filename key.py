import string

class Key:
    def decrypt(self, cipher_words):
        running_rotation = 0
        plaintext = ""

        #
        # - word in plaintext_char_dict (mapped to a letter) with a known rotation
        # - word in plaintext_char_dict without a known rotation
        # - word not in plaintext_char_dict (not mapped to a letter)
        #   - is it possible to have a word with a known rotation but not mapped to a letter?
        #
        # General note(s):
        # - If we hit a word with an unknown rotation, we can't do any further decryption until
        #   we figure out a rotation to use for that word.
        #   - I think this means we need a "look ahead" algorithm of some sort...
        # - Set of possible letters is limited to what key_builder didn't pre-calculate for us
        #
        for word in cipher_words:
            try:
                plaintext_char = self.plaintext_char_dict[word]
            except:
                plaintext_char = self.unused_key_chars.pop()
                self.plaintext_char_dict[word] = plaintext_char
                
            plaintext_char = chr((ord(plaintext_char) - ord('a') - running_rotation) % 26 + ord('a'))
            plaintext += plaintext_char
            try:
                rotation = self.rotation_dict[word]
            except:
                rotation = 0
                self.rotation_dict[word] = rotation
            running_rotation -= rotation
        return plaintext

    def __init__(self, plaintext_char_dict, rotation_dict, unused_key_chars):
        self.plaintext_char_dict = plaintext_char_dict
        self.rotation_dict = rotation_dict
        self.unused_key_chars = unused_key_chars
