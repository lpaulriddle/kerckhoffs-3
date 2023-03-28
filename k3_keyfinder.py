#!/usr/bin/env python3

from cipher import Cipher
import logging

logging.basicConfig(level=logging.WARN, format='%(asctime)s - %(module)s - %(levelname)s - %(message)s')

#cipher_filename = "k2.txt"
#plaintext1 = 'extraordinairetosolveswapanddo'     # 35
#plaintext2 = 'plaintextforuseascribsatleastforth' # 170
#range_to_check = None

cipher_filename = "k3.txt"
plaintext1 = 'norththirtyninedegreestenpoint'
plaintext2 = 'westseventysixdegreesfiftyonepoint'
range_to_check = range(40, 90)

cipher = Cipher(cipher_filename)
l1 = len(plaintext1)
l2 = len(plaintext2)

count_dict = {}

num_good = 0
num_bad = 0
print(f"Cipher length = {len(cipher)}")
print('Checking plaintext slice 1 at index', end=' ', flush=True)
if range_to_check == None:
    range_to_check = range(len(cipher) - l1 + 1)
for i1 in range_to_check:
    print(i1, end='...', flush=True)
    slice1 = cipher.known_plaintext_slice(plaintext1, i1)
    for i2 in range(0, len(cipher) - l2 + 1):

        # Skip overlapping slices
        if max(i1, i2) < min(i1+l1, i2+l2):
            continue
        slice2 = cipher.known_plaintext_slice(plaintext2, i2)
        key_builder = cipher.get_key_builder(slice1, slice2)
        if key_builder != None:
            num_good += 1

            #
            # Need to store: number of possible keys, the key object itself, and the plaintext indices
            # Dictionary of lists of {num_possible_keys: [(i1, i2), Key]} ?
            #
            key_builder_stats = key_builder.stats()
            num_possible_keys = key_builder_stats['num_possible_keys']
            tup = (i1, i2, key_builder)
            try:
                count_dict[num_possible_keys].append(tup)
            except KeyError:
                count_dict[num_possible_keys] = [tup]
            s = 's' if num_possible_keys > 1 else ''
            print(f"\nGood reduction at plaintext indices ({i1}, {i2}) with {num_possible_keys} possible key{s}")
        else:
            num_bad += 1

print(f"\nTotal good reductions: {num_good}\nTotal bad reductions: {num_bad}")

#
# Work through reductions in order of number of possible keys. This eliminates positions with
# fewer possible keys first, leaving the potentially longer-running positions for later.
#
for c in sorted(count_dict.keys()):
    for (index1, index2, key_builder) in count_dict[c]:
        print(f"Looking for keys at indices ({index1}, {index2})")
        good_count = 0
        for key in key_builder:
            plaintext = key.decrypt(cipher, index1, 0)
            print(f"decryption: {plaintext}; key: {key.__dict__}")
            good_count += 1
        s = 's' if good_count > 1 else ''
        print(f"Found {good_count} valid key{s} at ({index1}, {index2})")
