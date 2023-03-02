#!/usr/bin/env python3

from key_builder import KeyBuilder
from rotation_matrix import build_rotation_matrix, build_rotation_matrix_new
from cipher import Cipher

#cipher_filename = "k2.txt"
#plaintext1 = 'extraordinairetosolveswapanddo'     # 35
#plaintext2 = 'plaintextforuseascribsatleastforth' # 170

cipher_filename = "k3.txt"
plaintext1 = 'norththirtyninedegreestenpoint'
plaintext2 = 'westseventysixdegreesfiftyonepoint'

cipher = Cipher(cipher_filename)
l1 = len(plaintext1)
l2 = len(plaintext2)

print(f"numkeys:{cipher_filename}")
print(f"numkeys:{plaintext1}")
print(f"numkeys:{plaintext2}")

count_dict = {}

for i1 in range(0, len(cipher) - l1 + 1):
    #slice1 = cipher.known_plaintext_slice(plaintext1, i1)
    for i2 in range(0, len(cipher) - l2 + 1):
        if max(i1, i2) < min(i1+l1, i2+l2):
            continue
        #slice2 = cipher.known_plaintext_slice(plaintext2, i2)
        print(f"slice1 {i1}-{i1+l1} slice2 {i2}-{i2+l2}")
        matrix_rotations = build_rotation_matrix_new(cipher.word_list, [(plaintext1, i1), (plaintext2, i2)])
        if matrix_rotations:
            #
            # Need to store: number of possible keys, the key object itself, and the plaintext indices
            # Dictionary of lists of {num_possible_keys: [(i1, i2), Key]} ?
            #
            k = KeyBuilder(matrix_rotations)
            s = k.stats()
            num_possible_keys = s['num_possible_keys']
            try:
                count_dict[num_possible_keys] += 1
            except KeyError:
                count_dict[num_possible_keys] = 1
            print(f"numkeys:{i1}:{i2}:{num_possible_keys}")
            print(f"keystats:{s}")
print("slice1",count_dict)
