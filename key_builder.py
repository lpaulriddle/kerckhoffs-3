class KeyBuilderException(Exception):
    pass

class Key:
    #(ROTATION_CALCULATED, ROTATION_GUESSED, ROTATION_KNOWN) = range(3)
    (ROTATION_CALCULATED, ROTATION_GUESSED, ROTATION_KNOWN) = ('calculated', 'guessed', 'known')
    def calculate_single_row_rotation(self, word, unknowns):
        rotation_sum = 0
        seen_ourselves = False
        (row_data, answer) = unknowns
        for (multiplier, dependent_word) in row_data:
            if word == dependent_word:
                seen_ourselves = True
                # Anything other than 1 means that the matrix wasn't properly reduced
                assert(multiplier == 1.0)
                continue
            if dependent_word in self.rotations:
                # Keep track of the running sum of other rotations in the row
                rotation_sum += multiplier * self.rotations[dependent_word]['rotation']
                continue
            print(f"Not enough known rotations to calculate {word}")
            return None
        assert(seen_ourselves == True)
        calculated_rotation = answer - rotation_sum
        assert(calculated_rotation.is_integer())
        calculated_rotation = int(calculated_rotation) % 26
        print(f"Calculated rotation for {word} == {calculated_rotation}")
        return calculated_rotation

    def calculate_rotation(self, word, unknowns):
        required_sum = None

        #
        # Loop through the list of rows, calculating any values we can
        #
        for thing in unknowns:
            print(f"Let's take care of {thing}")
            r = self.calculate_single_row_rotation(word, thing)
            if r != None:
                if required_sum == None:
                    required_sum = r
                elif required_sum != r:

                    #
                    # If we've calculated a value from a previous row, any subsequent values we calculate
                    # must match it. If not, then we have a conflict and need to backtrack somehow.
                    # Assuming the code is correct, the matrix is properly reduced, and we work on
                    # unknown columns from right to left, this condition doesn't seem to happen.
                    #
                    raise Exception(f"Multi-row equation mismatch: {required_sum} != {r} for {unknowns}")
        print(f"Multi row calc {required_sum}")
        return required_sum

    def generate(self):
        pos = len(self.rotations)

        while pos < len(self.unique_words):
            val = self.unique_words[pos]
            assert(val not in self.rotations)
            self.rotations[val] = {}
            rotation = None
            if val in self.known_rotations:
                rotation = self.known_rotations[val]
                self.rotations[val]['type'] = self.ROTATION_KNOWN
            elif val in self.unknown_rotations:
                rotation = self.calculate_rotation(val, self.unknown_rotations[val])
                if rotation == None:
                    rotation = 0
                    self.rotations[val]['type'] = self.ROTATION_GUESSED
                else:
                    self.rotations[val]['type'] = self.ROTATION_CALCULATED
            else:
                raise KeyBuilderException(f"Word {val} not present in either known_rotations or unknown_rotations")
            self.rotations[val]['rotation'] = rotation
            print(f"position {pos} rots {self.rotations}")
            pos += 1

    def next(self):
        pos = len(self.unique_words) - 1
        while (pos >= 0):
            word = self.unique_words[pos]
            rotation = self.rotations[word]
            if (rotation['type'] == self.ROTATION_GUESSED):
                rot_val = rotation['rotation'] + 1
                if rot_val < 26:
                    rotation['rotation'] = rot_val
                    self.generate()
                    return True
                if rot_val > 26:
                    # This "should not happen"
                    raise KeyBuilderException(f"Guessed key val for {word} > 26")

            #
            # Rotation value == 26 or type is not ROTATION_GUESSED - remove the entry for the
            # current word and backtrack, looking for the previous guessed rotation value
            #
            del self.rotations[word]
            pos -= 1
        else:
            # No more guesses possible (either no guessed words, or
            # exhausted all possible guessed values)
            print("Exhausted all possible rotation combinations")
            return False

    def fit_plaintext(self, cipher_slice, plaintext):
        running_rotation = 0
        plaintext_char_dict = {}
        used_key_char_dict = {}
        for (word, ch) in zip(cipher_slice, plaintext):
            if word not in self.rotations:
                print(f"word {word} not in key - finishing")
                return True
            rot_val = self.rotations[word]['rotation']
            if word in plaintext_char_dict:
                key_ch = plaintext_char_dict[word]
                expected_pt_ch = chr((ord(key_ch) - running_rotation - ord('a')) % 26 + ord('a'))
                print(f"Found {word} keychar {key_ch} pt char {ch} (expected {expected_pt_ch})")

                #
                # Key rotation mismatch- This should never occur if the plaintext matches the cipher
                # slice and the key satisfies the matrix
                #
                if ch != expected_pt_ch:
                    print("Key mismatch: plaintext char '{ch}' != expected char '{expected_pt_ch}'")
                    return False
            else:
                key_ch = chr((ord(ch) + running_rotation - ord('a')) % 26 + ord('a'))

                #
                # Each letter can appear in the key only once. We could just pull
                # plaintext_char_dict.values() here and do a linear search, but a separate dict
                # seemed more efficent, and we can also display the previously mapped cipher word.
                #
                # Unlike rotation mismatches, this does occur a *lot* with a matching key and
                # sufficiently long plaintext sample. For example, matching 32 characters of known
                # plaintext against the beginning of the Kerckhoffs 2 cipher yielded a total of
                # 456,976 possible keys (26^4), of which only 10,296 had no dups. I wonder if it
                # would be possible to determine this mathematically somehow instead of iteratively.
                #
                if key_ch in used_key_char_dict:
                    print(f"Duplicate key_char: '{key_ch}' already mapped to word '{used_key_char_dict[key_ch]}'")
                    return False
                used_key_char_dict[key_ch] = word
                plaintext_char_dict[word] = key_ch
                print(f"Added {word} = {key_ch} (rot {rot_val} running_rot {running_rotation}")

            running_rotation = (running_rotation - rot_val) % 26
            print(f"Running rotation = {running_rotation}")
        print("Successful fit")
        return True

    def __init__(self, matrix_rotations):

        #
        # We need to get the list of words in the order they appear in the matrix
        # This gets sorted in the reduction code, so just need to return that somehow to avoid doing
        # it again here
        #
        self.unique_words = list(matrix_rotations.keys())
        self.unique_words.sort()
        self.unique_words.reverse()
        print("unique_words", self.unique_words)

        #
        # Pull out keys we know for sure ahead of time
        # This is a little bit convoluted, but if the algorithm works, we'll do this upstream
        # in the matrix code somehow..
        #
        single_row_vars = dict([(a,b[0]) for (a,b) in matrix_rotations.items() if len(matrix_rotations[a]) == 1])
        self.known_rotations = dict([(a,b[1]) for (a,b) in single_row_vars.items() if len(single_row_vars[a][0]) == 1])
        print("known_rotations", self.known_rotations)

        #
        # Now, pull out all the unknowns, which basically means "anything not in known_rotations"
        # This includes unknown rotations that appear in one or more rows of the matrix
        #
        self.unknown_rotations = dict([(a,b) for (a,b) in matrix_rotations.items() if a not in self.known_rotations])
        print("unknown_rotations", self.unknown_rotations)

        assert(len(self.known_rotations) + len(self.unknown_rotations)) == len(matrix_rotations)

        pos = 0
        self.rotations = {}
        self.generate()
