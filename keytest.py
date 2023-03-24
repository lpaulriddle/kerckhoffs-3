#!/usr/bin/env python3

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

num_good = 0
num_bad = 0
print(f"Cipher length = {len(cipher)}")
for i1 in range(0, len(cipher) - l1 + 1):
    print(f"trying plaintext1 at index {i1}")
    slice1 = cipher.known_plaintext_slice(plaintext1, i1)
    for i2 in range(0, len(cipher) - l2 + 1):
        if max(i1, i2) < min(i1+l1, i2+l2):
            continue
        slice2 = cipher.known_plaintext_slice(plaintext2, i2)
        #print(f"slice1 {i1}-{i1+l1} slice2 {i2}-{i2+l2}")
        key_builder = cipher.get_key_builder(slice1, slice2)
        if key_builder != None:
            num_good += 1

            #
            # Need to store: number of possible keys, the key object itself, and the plaintext indices
            # Dictionary of lists of {num_possible_keys: [(i1, i2), Key]} ?
            #
            key_builder_stats = key_builder.stats()
            num_possible_keys = key_builder_stats['num_possible_keys']
            try:
                count_dict[num_possible_keys] += 1
            except KeyError:
                count_dict[num_possible_keys] = 1
            print(f"numkeys:{i1}:{i2}:{num_possible_keys}")
            print(f"keystats:{key_builder_stats}")
        else:
            num_bad += 1
print("count_dict",count_dict)
print(f"num_good {num_good} num_bad {num_bad}")
