class Key:
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
                rotation_sum += multiplier * self.rotations[dependent_word]
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

    def __init__(self, matrix_rotations):

        #
        # We need to get the list of words in the order they appear in the matrix
        # This gets sorted in the reduction code, so just need to return that somehow to avoid doing
        # it again here
        #
        unique_words = list(matrix_rotations.keys())
        unique_words.sort()
        unique_words.reverse()
        print("unique_words", unique_words)

        #
        # Pull out keys we know for sure ahead of time
        # This is a little bit convoluted, but if the algorithm works, we'll do this upstream
        # in the matrix code somehow..
        #
        single_row_vars = dict([(a,b[0]) for (a,b) in matrix_rotations.items() if len(matrix_rotations[a]) == 1])
        known_rotations = dict([(a,b[1]) for (a,b) in single_row_vars.items() if len(single_row_vars[a][0]) == 1])
        print("known_rotations", known_rotations)

        #
        # Now, pull out all the unknowns, which basically means "anything not in known_rotations"
        # This includes unknown rotations that appear in one or more rows of the matrix
        #
        unknown_rotations = dict([(a,b) for (a,b) in matrix_rotations.items() if a not in known_rotations])
        print("unknown_rotations", unknown_rotations)

        assert(len(known_rotations) + len(unknown_rotations)) == len(matrix_rotations)

        pos = 0
        self.rotations = known_rotations.copy()
        self.guessed_rotations = []

        while pos < len(unique_words):
            val = unique_words[pos]
            print(f"doing {val}")
            if val in known_rotations:
                pass
            else:
                assert(val in unknown_rotations)
                r = self.calculate_rotation(val, unknown_rotations[val])
                # TBD- Need to mark as calculated or guessed for backtracking purposes
                if r == None:
                    r = 0
                    self.guessed_rotations.append(val)
                self.rotations[val] = r
            print(f"position {pos} rots {self.rotations}")
            pos += 1
