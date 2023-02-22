#!/usr/bin/env python3

from key_builder import Key
from rotation_matrix import build_rotation_matrix, build_rotation_matrix_new
from cipher import Cipher

#cipher = Cipher("k3.txt", False)
#slice1 = cipher.known_plaintext_slice('norththirtyninedegreestenpoint', 1)
#slice2 = cipher.known_plaintext_slice('westseventysixdegreesfiftyonepoint', 147)
#matrix_rotations = build_rotation_matrix_new(cipher.word_list, ((slice1.plaintext, 1), (slice2.plaintext, 147)))

cipher = Cipher("k2.txt", True)
slice1 = cipher.known_plaintext_slice('congratulationsyouareacryptograph', 0)
slice2 = cipher.known_plaintext_slice('thecacheisattheweirdstumpthisis', 245)
matrix_rotations = build_rotation_matrix_new(cipher.word_list, ((slice1.plaintext, 0), (slice2.plaintext, 245)))

#cipher = Cipher("k2.txt", True)
#plaintext = 'congratulationsyouareacryptograph'
#matrix_rotations = build_rotation_matrix(cipher.word_list, plaintext, 0)

if matrix_rotations != None:
    key = Key(matrix_rotations)
    print(f"initial rotations {key.rotations}")
    good_count = 0
    bad_count = 0
    key.stats()

    while True:
        if (key.fit_plaintext(slice1) == True) and (key.fit_plaintext(slice2) == True):
            good_count += 1
        else:
            bad_count += 1
        print(f"good_count {good_count} bad_count {bad_count}")
        if key.next() == False:
            break
        print(f"next rotation {key.rotations}")
