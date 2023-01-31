#!/usr/bin/env python3

from rotation_matrix import build_rotation_matrix
from split_cipher import read_cipher

def build_offset_rotation_dict(cipher_list, plaintext):
    rotation_dict = {}

    for i in range(len(cipher_list) - len(plaintext)):
        print(f"Fitting {plaintext} at position {i}")
        known_rotations = build_rotation_matrix(cipher_list, plaintext, i)
        if known_rotations:
            rotation_dict[i] = known_rotations

    print(f"Found {len(rotation_dict)} possible fits for {plaintext}: {rotation_dict}")
    return rotation_dict

(cipher_words, cipher_list) = read_cipher("k3.txt", False)

latitude_pt = "norththirtyninedegreestenpoint"
longitude_pt = "westseventysixdegreesfiftyonepoint"
lat_dict = build_offset_rotation_dict(cipher_list, latitude_pt)
lon_dict = build_offset_rotation_dict(cipher_list, longitude_pt)

#
# Eliminate index pairs that would result in overlapping strings.
# In practice with K3, this cuts out just under 10% of the possible position combos
#
for lon_index in lon_dict:
    for lat_index in lat_dict:
        if (lat_index >= lon_index) and (lat_index < lon_index + len(longitude_pt)):
            print(f"latindex overlap {lat_index} {lon_index}")
        elif (lon_index >= lat_index) and (lon_index < lat_index + len(latitude_pt)):
            print(f"lonindex overlap {lat_index} {lon_index}")
        else:
            print(f"latlonindex {lat_index}, {lon_index}")

#
# TBD: Eliminate pairs with conflicting rotation values for the same cipher word
#
