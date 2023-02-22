#!/usr/bin/env python3

#from key_builder import build_initial_key
from rotation_matrix import build_rotation_matrix, build_rotation_matrix_new
from cipher import Cipher

cipher = Cipher("k3.txt", False)
plaintext1 = 'norththirtyninedegreestenpoint'
plaintext2 = 'westseventysixdegreesfiftyonepoint'
#plaintext = 'westseventysixdegreesfiftyonepoint'
#good_rots = 0
#for x in range(len(cipher_list) - len(plaintext)):
#    print(f"rotation {x}")
#    matrix_rotations = build_rotation_matrix(cipher_list, plaintext, x)
#    print("-------")
#    if matrix_rotations != None:
#        good_rots += 1
#        rotations = build_initial_key(matrix_rotations)
#        print(f"rotations {rotations}")
#print(f"{good_rots} good offsets")
#exit(0)
l1 = len(plaintext1)
l2 = len(plaintext2)
#full_pt = 'congratulationsyouareacryptographerextraordinairetosolveswapanddoublethelastpartsofthecoordssorryifthisisconfusingididntwantanynumbersorcardinaldirectionstobepresentintheplaintextforuseascribsatleastforthisonethecheckercanhelpyouverifyyouranswerthecacheisattheweirdstumpthisisobviouslynotrequiredbutidlovetohearaboutyoursolutionmethod'
for i1 in range(0, len(cipher.word_list) - l1 + 1):
    slice1 = cipher.word_list[i1:i1+l1]
    #pt1 = full_pt[i1:i1+l1]
    for i2 in range(0, len(cipher.word_list) - l2 + 1):
        if max(i1, i2) < min(i1+l1, i2+l2):
            continue
        slice2 = cipher.word_list[i2:i2+l2]
        #pt2 = full_pt[i2:i2+l2]
        print(f"slice1 {i1}-{i1+l1} slice2 {i2}-{i2+l2}")
        matrix_rotations = build_rotation_matrix_new(cipher.word_list, [(plaintext1, i1), (plaintext2, i2)])        
print(cipher.word_list)
#for thing in range(36,106):
#    print(f"doing {thing}")
#    matrix_rotations = build_rotation_matrix_new(cipher_list, [('congratulationsyouareacryptographere', 0),('confusingididntwantanynumbersorcardin', thing)]) # 105
