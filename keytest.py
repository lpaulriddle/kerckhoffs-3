#!/usr/bin/env python3

from key_builder import Key
from rotation_matrix import build_rotation_matrix, build_rotation_matrix_new
from cipher import Cipher

cipher = Cipher("k3.txt", False)
plaintext1 = 'norththirtyninedegreestenpoint'
plaintext2 = 'westseventysixdegreesfiftyonepoint'
l1 = len(plaintext1)
l2 = len(plaintext2)

for i1 in range(0, len(cipher) - l1 + 1):
    #slice1 = cipher.known_plaintext_slice(plaintext1, i1)
    for i2 in range(0, len(cipher) - l2 + 1):
        if max(i1, i2) < min(i1+l1, i2+l2):
            continue
        #slice2 = cipher.known_plaintext_slice(plaintext2, i2)
        print(f"slice1 {i1}-{i1+l1} slice2 {i2}-{i2+l2}")
        matrix_rotations = build_rotation_matrix_new(cipher.word_list, [(plaintext1, i1), (plaintext2, i2)])
        if matrix_rotations:
            k = Key(matrix_rotations)
            print(k.stats())
            print("...") # Breakpoint placeholder
print(cipher.word_list)
#for thing in range(36,106):
#    print(f"doing {thing}")
#    matrix_rotations = build_rotation_matrix_new(cipher_list, [('congratulationsyouareacryptographere', 0),('confusingididntwantanynumbersorcardin', thing)]) # 105
