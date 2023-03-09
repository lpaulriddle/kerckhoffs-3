import string

from enum import Enum

class Key:
    class DecryptionException(Exception):
        pass

    def decrypt(self, cipher):
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
        for word in cipher.word_list:
            plaintext_char = self.plaintext_char_dict.get(word)
            rotation = self.rotation_dict.get(word)

            if plaintext_char == None:
                print(f"Missing plaintext character for {word}")
                return plaintext
            plaintext_char = chr((ord(plaintext_char) - ord('a') - running_rotation) % 26 + ord('a'))
            plaintext += plaintext_char
            if rotation == None:
                # Unknown rotation: need to look ahead to find next word without a mapped plaintext char
                # character
                print(f"Missing rotation for {word}")
                return plaintext
            else:
                running_rotation = (running_rotation - rotation) % 26

        return plaintext

    def __init__(self, plaintext_char_dict, rotation_dict, unused_key_chars):
        self.plaintext_char_dict = plaintext_char_dict
        self.rotation_dict = rotation_dict
        self.unused_key_chars = unused_key_chars
