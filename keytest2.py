#!/usr/bin/env python3

from key_builder import KeyBuilder
from rotation_matrix import build_rotation_matrix, build_rotation_matrix_new
from cipher import Cipher

#cipher = Cipher("k3.txt")
#slice1 = cipher.known_plaintext_slice('norththirtyninedegreestenpoint', 1)
#slice2 = cipher.known_plaintext_slice('westseventysixdegreesfiftyonepoint', 147)
#matrix_rotations = build_rotation_matrix_new(cipher.word_list, ((slice1.plaintext, 1), (slice2.plaintext, 147)))

cipher = Cipher("k2.txt")
slice1 = cipher.known_plaintext_slice('congratulationsyouareacryptograph', 0)
slice2 = cipher.known_plaintext_slice('thecacheisattheweirdstumpthisis', 245)
matrix_rotations = build_rotation_matrix_new(cipher.word_list, ((slice1.plaintext, 0), (slice2.plaintext, 245)))

#cipher = Cipher("k2.txt", True)
#plaintext = 'congratulationsyouareacryptograph'
#matrix_rotations = build_rotation_matrix(cipher.word_list, plaintext, 0)

if matrix_rotations != None:
    key_builder = KeyBuilder(matrix_rotations)
    print(f"initial rotations {key_builder.rotations}")
    good_count = 0
    bad_count = 0
    print("Stats:",key_builder.stats())

    while True:
        good_key = False
        if (key_builder.fit_plaintext(slice1) == True):
            #key1 = key_builder.key()
            if (key_builder.fit_plaintext(slice2) == True):
                key = key_builder.key()
                # Note - this naively passes the entire cipher to decrypt() - needs adjusting to work with slices
                # that don't start at the beginning of the cipher.
                #print("decryption:",key.decrypt(cipher.word_list),"key1rot",key1.plaintext_char_dict,"key2rot",key2.plaintext_char_dict,"numrots",len(set(list(key1.rotation_dict.keys())+list(key2.rotation_dict.keys()))))
                print("decryption:",key.decrypt(cipher))
                good_key = True
        if good_key == True:
            good_count += 1
        else:
            bad_count += 1
        print(f"good_count {good_count} bad_count {bad_count}")
        if key_builder.next() == False:
            break
        print(f"next rotation {key_builder.rotations}")
