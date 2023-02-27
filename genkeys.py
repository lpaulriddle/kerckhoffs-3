#!/usr/bin/env python3

import sys
from cipher import Cipher
from rotation_matrix import build_rotation_matrix_new
from key_builder import KeyBuilder

pt_index_dict = {}
total_positions = 0

with open('k2.numkeys', 'r') as f:
    def get_line():
        return f.readline().rstrip().split(':')[1]

    cipher_filename = get_line()
    plaintext1 = get_line()
    plaintext2 = get_line()

    print(f"filename {cipher_filename} pt1 {plaintext1} pt2 {plaintext2}")
    # Todo - Add the "known word length" flag to the cipher text file
    cipher = Cipher(cipher_filename)

    for line in f:
        (i1, i2, num_keys) = [int(x) for x in line.rstrip().split(':')[1:]]
        try:
            pt_index_dict[num_keys].append((i1, i2))
        except KeyError:
            pt_index_dict[num_keys] = [(i1, i2)]
        total_positions += 1

    print(f"keyfit:Total position combos with good matrices = {total_positions}")
    for num_keys in sorted(pt_index_dict.keys()):
        print(f"keyfit:Doing matrices with {num_keys} possible key(s)..")
        for (i1, i2) in pt_index_dict[num_keys]:
            print(f"keyfit:Looking for keys at ({i1},{i2})")
            # Todo- make build_rotation_matrix take KnownPlaintextSlice objects
            matrix_rotations = build_rotation_matrix_new(cipher.word_list, ((plaintext1, i1), (plaintext2, i2)))
            assert(matrix_rotations) # These are supposed to be indices that generate a known good matrix
            key = KeyBuilder(matrix_rotations)
            # Todo- make Key an iterable
            while True:
                slice1 = cipher.known_plaintext_slice(plaintext1, i1)
                slice2 = cipher.known_plaintext_slice(plaintext2, i2)
                if (key.fit_plaintext(slice1) == True) and (key.fit_plaintext(slice2) == True):
                    print(f"keyfit:good key at {i1},{i2}")
                else:
                    print(f"keyfit:bad key at {i1},{i2}")
                if key.next() == False:
                    break
        if num_keys > 10:
            break
