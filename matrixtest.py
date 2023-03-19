#!/usr/bin/env python3
#
# Beat the hell out of my matrix reduction code with known plaintext to make sure
# there are no bugs
#

from rotation_matrix import RotationMatrix
from cipher import Cipher

cipher = Cipher("k2.txt")
full_plaintext = 'congratulationsyouareacryptographerextraordinairetosolveswapanddoublethelastpartsofthecoordssorryifthisisconfusingididntwantanynumbersorcardinaldirectionstobepresentintheplaintextforuseascribsatleastforthisonethecheckercanhelpyouverifyyouranswerthecacheisattheweirdstumpthisisobviouslynotrequiredbutidlovetohearaboutyoursolutionmethod'

for j in range(0, len(full_plaintext)):
    for i in range(j, len(full_plaintext)):
        text = full_plaintext[j:i+1]
        #rots = build_rotation_matrix(cipher_list[:i+1], text, 0)
        slice = cipher.known_plaintext_slice(text, j)
        print(f"Doing {slice}")
        matrix = RotationMatrix(cipher, cipher.known_plaintext_slice(text, j))
        matrix.reduce()
        rots = matrix.get_rotations()
