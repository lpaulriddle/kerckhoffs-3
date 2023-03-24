A solver for [Kerckhoffs (part 3)](https://coord.info/GC9PC6T)

The solution method, given the cipher as one long string of concatenated code words, and two strings of known plaintext located
somewhere within the cipher:

1. Determine the 26 unique code words using an algorithm that looks for repeated sequences of numbers in the ciphertext.
2. Split the cipher into a list of code words.
3. Note the following important property: If you know the plaintext for two identical words at different offsets in the cipher, then you can conclude that the cumulative rotation value between the first offset and the second offset must equal the difference between the ordinal values of the two plaintext characters (mod 26). This can be represented as a multivariable equation with the variables being the code words occurring between the two offsets, and the frequency of each code word corresponding to its variable coefficient.
4. For every possible position of the two plaintext strings within the cipher, run the following algorithm:
  * Find every such occurrence of identical words with known plaintext, construct the corresponding equation, and assemble all of the equations into a matrix.
  * Row-reduce the matrix using only integer operations. If the matrix is inconsistent (no solution), eliminate the current position of the plaintext strings from consideration.
5. For each position that yields a matrix having one or more solutions, run the following algorithm:
  * Iterate through all possible solutions to the matrix (each solution corresponds to a set of key rotation values).
  * For each solution, try to generate a (possibly partial) key by fitting the known plaintext to each possible set of rotations. A successful fit will yield a key with no duplicate key characters.
  * For each successful fit, try to decrypt the cipher and look to see if any unknown portions of the cipher are decrypted correctly.