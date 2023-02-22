#!/usr/bin/env python3

from key_builder import Key
from rotation_matrix import build_rotation_matrix, build_rotation_matrix_new
from cipher import Cipher

cipher = Cipher("k3.txt", False)
plaintext1 = 'norththirtyninedegreestenpoint'
plaintext2 = 'westseventysixdegreesfiftyonepoint'
matrix_rotations = build_rotation_matrix_new(cipher.word_list, [(plaintext1, 1), (plaintext2, 147)])

#cipher = Cipher("k2.txt", True)
#plaintext1 = 'congratulationsyouareacryptograph'
#plaintext2 = 'thecacheisattheweirdstumpthisis'
#matrix_rotations = build_rotation_matrix_new(cipher.word_list, ((plaintext1, 0), (plaintext2, 245)))

#cipher = Cipher("k2.txt", True)
#plaintext = 'congratulationsyouareacryptograph'
#matrix_rotations = build_rotation_matrix(cipher.word_list, plaintext, 0)

if matrix_rotations != None:
    key = Key(matrix_rotations)
    print(f"initial rotations {key.rotations}")
    good_count = 0
    bad_count = 0
    key.stats()
#    exit(0)
    while True:
#        if key.fit_plaintext(cipher.word_list[245:], plaintext2) == True:
        if (key.fit_plaintext(cipher.word_list[1:], plaintext1) == True) and (key.fit_plaintext(cipher.word_list[147:], plaintext2) == True):
            good_count += 1
        else:
            bad_count += 1
        print(f"good_count {good_count} bad_count {bad_count}")
        if key.next() == False:
            break
        print(f"next rotation {key.rotations}")

