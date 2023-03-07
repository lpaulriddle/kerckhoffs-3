from key import Key
import string

class KeyBuilderException(Exception):
    pass

class RotationCalculationException(Exception):
    pass

class KeyBuilder:
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
        if not calculated_rotation.is_integer():
            raise RotationCalculationException(f"non-integer rotation {calculated_rotation} for word {word}, unknowns {unknowns}")
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
        starting_pos = pos

        while pos < len(self.unique_words):
            val = self.unique_words[pos]
            assert(val not in self.rotations)
            self.rotations[val] = {}
            rotation = None
            if val in self.known_rotations:
                rotation = self.known_rotations[val]
                self.rotations[val]['type'] = self.ROTATION_KNOWN
            elif val in self.unknown_rotations:
                try:
                    rotation = self.calculate_rotation(val, self.unknown_rotations[val])
                    if rotation == None:
                        rotation = 0
                        self.rotations[val]['type'] = self.ROTATION_GUESSED
                    else:
                        self.rotations[val]['type'] = self.ROTATION_CALCULATED
                except RotationCalculationException:

                    #
                    # Right now, this only happens when the calculated rotation is not an
                    # integer, in which case the key is invalid and we just want to skip it.
                    # Becaue of how the code currently works, this means that we need to
                    # delete everything we computed here and return to the caller with a
                    # "clean slate" so that everything will get re-computed properly after
                    # incrementing the guessed value.
                    # 
                    for i in range(starting_pos, pos + 1):
                        del self.rotations[self.unique_words[i]]
                    return False
                    
            else:
                raise KeyBuilderException(f"Word {val} not present in either known_rotations or unknown_rotations")
            self.rotations[val]['rotation'] = rotation
            print(f"position {pos} rots {self.rotations}")
            pos += 1
        return True

    def next(self):
        self.reset()
        pos = len(self.unique_words) - 1
        while (pos >= 0):
            word = self.unique_words[pos]
            rotation = self.rotations[word]
            if (rotation['type'] == self.ROTATION_GUESSED):
                rot_val = rotation['rotation'] + 1
                while rot_val < 26:
                    rotation['rotation'] = rot_val
                    if self.generate() == True:
                        return True
                    # That rot_val didn't work, so try incrementing by one
                    rot_val += 1
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

    def reset(self):
        self.plaintext_char_dict = {}
        self.used_key_char_dict = {}
        self.unused_key_chars = set(string.ascii_lowercase)

    def fit_plaintext(self, known_plaintext_slice):
        running_rotation = None
        if bool(self.plaintext_char_dict) == False:
            # If this is our first time fitting plaintext with this key, start rotation at 0
            running_rotation = 0
        for (i, (word, ch)) in enumerate(known_plaintext_slice):
            rot_val = None
            try:
                rot_val = self.rotations[word]['rotation']
            except:
                # No rotation for this word in the matrix
                pass
            if word in self.plaintext_char_dict:
                key_ch = self.plaintext_char_dict[word]
                if running_rotation == None:
                    # Is this as easy as calculating the difference between the plaintext char and the key char?
                    running_rotation = (ord(key_ch) - ord(ch)) % 26
                    print(f"running_rotation set to {running_rotation}")
                    #print("TBD- compute running_rotation for word {word} slice_index {i} cipher index {i+known_plaintext_slice.cipher_index}")
                    # Need index and plaintext value of (at least one) other location of this word
                    #exit(0)
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
                if key_ch in self.used_key_char_dict:
                    print(f"Duplicate key_char: '{key_ch}' already mapped to word '{self.used_key_char_dict[key_ch]}'")
                    return False
                self.used_key_char_dict[key_ch] = word
                self.unused_key_chars.remove(key_ch)
                self.plaintext_char_dict[word] = key_ch
                print(f"Added {word} = {key_ch} (rot {rot_val} running_rot {running_rotation})")

            if rot_val == None:
                # unknown rotation - can't continue
                print(f"Rotation for {word} not known - finishing")
                return True
            running_rotation = (running_rotation - rot_val) % 26
            print(f"Running rotation = {running_rotation}")
        print("Successful fit")
        return True

    def key(self):
        unused_key_chars = list(self.unused_key_chars)
        unused_key_chars.sort()
        return Key(self.plaintext_char_dict, dict([(a,b['rotation']) for (a,b) in self.rotations.items()]), unused_key_chars)

    def stats(self):
        num_rotations = len(self.rotations)
        num_known_rotations = len(self.known_rotations)
        num_guessed_rotations = len([x['type'] for x in self.rotations.values() if x['type'] == self.ROTATION_GUESSED])
        num_possible_keys = 26 ** num_guessed_rotations
        return {'num_rotations': num_rotations,
                'num_known_rotations': num_known_rotations,
                'num_guessed_rotations': num_guessed_rotations,
                'num_possible_keys': num_possible_keys}

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
        if not self.generate():
            print("TBD- initial generation failed")
            exit(0)
        self.reset()
