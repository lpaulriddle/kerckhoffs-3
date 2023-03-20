#!/usr/bin/env python3

from cipher import Cipher
from key import Key
import string

cipher = Cipher("k3.txt")
rotation_dict = {'0273351': 5, '0648': 5, '09525': 5, '14246': 24, '156978': 1, '222146337': 13, '243255912': 17, '30': 18, '317077': 0, '418': 11, '444396': 18, '5954191': 4, '6103003': 2, '63388773': 21, '781': 24, '79833': 14, '860': 1, '8621836': 10, '871646': 14, '93': 19, '946294413': 5, '96972': 1}
plaintext_char_dict = {'243255912': 'n', '0273351': 'x', '156978': 'v', '8621836': 'w', '860': 'a', '14246': 'l', '6103003': 'b', '09525': 'i', '871646': 'f', '222146337': 'u', '418': 'm', '93': 's', '781': 'y', '0648': 'k', '30': 'z', '444396': 'h', '143261': 'p', '96972': 'r', '79833': 'c', '5954191': 'j', '317077': 'e', '946294413': 't', '63388773': 'g'}

key = Key(plaintext_char_dict, rotation_dict, None)
key.plaintext_char_dict['80920926'] = 'p'
key.rotation_dict['80920926'] = 21
key.plaintext_char_dict['37638005'] = 'q'
key.rotation_dict['37638005'] = 17
# key_builder seems to be incorrectly setting 143261 to 'p'. Need to debug...
key.plaintext_char_dict['143261'] = 'd'
key.rotation_dict['143261'] = 11
key.plaintext_char_dict['2167948'] = 'o'
key.rotation_dict['2167948'] = 17
#for pt_ch in string.ascii_lowercase:
#    key.plaintext_char_dict['2167948'] = pt_ch
#    print(pt_ch, key.decrypt(cipher, 46))
#for try_rot in range(26):
#    key.rotation_dict['2167948'] = try_rot
#    print(try_rot, key.decrypt(cipher, 46))
#print(key.decrypt(cipher, 46, 0))
print(key.decrypt(cipher, 0, 4))
