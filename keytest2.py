#!/usr/bin/env python3

from cipher import Cipher
import logging

logging.basicConfig(level=logging.WARN, format='%(asctime)s - %(module)s - %(levelname)s - %(message)s')

cipher = Cipher("k3.txt")
slice1 = cipher.known_plaintext_slice('norththirtyninedegreestenpoint', 46)
slice2 = cipher.known_plaintext_slice('westseventysixdegreesfiftyonepoint', 114)
#matrix_rotations = build_rotation_matrix_new(cipher.word_list, ((slice1.plaintext, 1), (slice2.plaintext, 147)))

#cipher = Cipher("k2.txt")
#slice1 = cipher.known_plaintext_slice('congratulationsyouareacryptograph', 0)
#slice2 = cipher.known_plaintext_slice('thecacheisattheweirdstumpthisis', 245)
#slice1 = cipher.known_plaintext_slice('extraordinairetosolveswapanddo', 35)
#slice2 = cipher.known_plaintext_slice('plaintextforuseascribsatleastforth', 170)
#matrix_rotations = build_rotation_matrix_new(cipher.word_list, ((slice1.plaintext, 0), (slice2.plaintext, 245)))

key_builder = cipher.get_key_builder(slice1, slice2)

#cipher = Cipher("k2.txt", True)
#plaintext = 'congratulationsyouareacryptograph'
#matrix_rotations = build_rotation_matrix(cipher.word_list, plaintext, 0)

if key_builder != None:
    print(f"initial rotations {key_builder.rotations}")
    good_count = 0
    bad_count = 0
    print("Stats:",key_builder.stats())

    for key in key_builder:
        print("key:", key.__dict__)
        print("decryption:", key.decrypt(cipher, slice1.cipher_index, 0))
        good_count += 1
    print(f"{good_count} total good key(s)")
