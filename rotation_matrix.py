import collections
import math

class RotationMatrixException(Exception):
    pass

class RotationMatrix:
    def __init__(self, cipher, *slices):
        self.known_plaintext_slices = sorted(slices)
        self.unique_words = cipher.unique_words
        self.matrix = []
        self.reduced = False

        slice_index = None
        last_occurrence_of = {}
        for pt_slice in self.known_plaintext_slices:
            if slice_index == None:
                slice_index = pt_slice.cipher_index
            else:
                # Make sure subsequent slices appear later in the cipher
                # Since we sorted the slices above, this in theory should always be the case
                assert(pt_slice.cipher_index > slice_index)
            for (i, (word, ch)) in enumerate(pt_slice):
                # Get the word's index in the cipher
                word_index = i + pt_slice.cipher_index
                #print("wordindex", word_index)

                #
                # If we've seen this word before, and have known plaintext at both locations, then
                # we can calculate the required rotation value between the two locations of the word
                #
                if word in last_occurrence_of:
                    (last_index, last_pt_ch) = last_occurrence_of[word]
                    assert(word_index > last_index)
                    required_rot = (ord(ch) - ord(last_pt_ch)) % 26
                    print(f"Required total rotation between {last_index} and {word_index} = {required_rot}")

                    #
                    # Count the number of occurrences of each word in the range. These will end up
                    # being the row coefficients
                    #
                    word_counts = collections.Counter(cipher[last_index:word_index])
                    matrix_row = [word_counts[x] if x in word_counts else 0 for x in self.unique_words]
                    matrix_row.append(required_rot)
                    self.matrix.append(matrix_row)

                last_occurrence_of[word] = (word_index, ch)

    def __str__(self):
        output = []
        # Number the columns. Each column corresponds to a word per self.unique_words
        output.append('   ' + ' '.join(['{:3}'.format(x) for x in range(len(self.matrix[0]) - 1)]))
        for (line_no, row) in enumerate(self.matrix):
            # I originally pulled non-zero entries so the words could be shown at the end of each row.
            # Probably not necessary to do this any more
            non_zero_entries = [(w,x) for (w,x) in zip(self.unique_words, row) if x != 0]
            total = sum([int(w[-1]) * x for (w,x) in non_zero_entries]) % 26
            output.append('{:2}:'.format(line_no) +
                          ' '.join(['{:-3}'.format(x) for x in row]) +
                          '({:3}) {:3}'.format(row[-1] % 26, total))
        return "\n".join(output)

    def _find_pivot(self, starting_row_num):
        mat = self.matrix

        #
        # Iterate through the columns (except for the RHS, which we don't want to
        # ever use as a pivot)
        #
        for col_num in range(len(mat[0]) - 1):
            pivot_row_num = -1
            pivot_val = None
            for row_num in range(starting_row_num, len(mat)):

                #
                # Find the smallest entry in the column with an absolute value greater than zero
                #
                potential_pivot_val = mat[row_num][col_num]
                appv = abs(potential_pivot_val)
                if (appv != 0) and ((pivot_val == None) or (appv < abs(pivot_val))):
                    pivot_val = potential_pivot_val
                    pivot_row_num = row_num
                    if appv == 1:
                        # If we find a 1, we can short circuit
                        break

            if pivot_row_num >= 0:
                # Swap rows if needed
                if pivot_row_num > starting_row_num:
                    print(f"Swapping rows {starting_row_num} and {pivot_row_num}")
                    mat[starting_row_num], mat[pivot_row_num] = mat[pivot_row_num], mat[starting_row_num]
                return col_num

            #
            # If we fall through to here, it means that there were no non-zero entries in
            # the column at or below the starting row, so we should move on and check the
            # next column
            #

        #
        # If we get here, then there were no non-zero entries anywhere in the matrix at or below
        # the starting row (which basically means we're finished)
        #
        print("No pivot found")
        return None

    def reduce(self):
        for pivot_row_index in range(len(self.matrix)):
            pivot_col_index = self._find_pivot(pivot_row_index)
            if pivot_col_index == None:
                break
            pivot_val = self.matrix[pivot_row_index][pivot_col_index]
            assert(pivot_val != 0)

            #
            # Reduce/simplify the pivot row if possible
            # Commented out for now because (a) I don't think it's necessary and (b) I'm not 100%
            # sure if dividing the RHS produces an accurate result
            #
            #if abs(pivot_val) > 1:
            #    row_gcd = math.gcd(*self.matrix[pivot_row_index])
            #    if row_gcd > 1:
            #        self.matrix[pivot_row_index] = [x // row_gcd for x in self.matrix[pivot_row_index]]
            #        pivot_val = self.matrix[pivot_row_index][pivot_col_index]

            #
            # Transform other rows so that everything else in the pivot column is zero
            #
            pivot_row = self.matrix[pivot_row_index]
            #print(f"Pivot row: {pivot_row}; first nonzero index: {pivot_col_index}")
            for secondary_row_index in range(0, len(self.matrix)):
                if secondary_row_index == pivot_row_index:
                    # Skip the pivot row
                    continue
                secondary_row = self.matrix[secondary_row_index]

                secondary_pivot_col_val = secondary_row[pivot_col_index]
                if secondary_pivot_col_val != 0:
                    lcm = math.lcm(pivot_val, secondary_pivot_col_val)
                    secondary_row = [x * (lcm // secondary_pivot_col_val) for x in secondary_row]
                    pivot_row_multiple = [x * (lcm // pivot_val) for x in pivot_row]

                    new_row = [(x-y) for (x,y) in zip(secondary_row, pivot_row_multiple)]
                    self.matrix[secondary_row_index] = new_row

                    #
                    # Look for a bad reduction (a row of all zero coefficients with a non-zero RHS)
                    # and also negate the row if the leading non-zero entry is negative. Not the most
                    # elegant or "Pythonic" code, but gets the job done fairly straightforwardly.
                    #
                    # Note that with a "regular" matrix, a row of all zeroes except the RHS means the
                    # matrix is indeterminant (no solution). However, in this case, since we're
                    # dealing with rotations, any RHS that equals 0 (mod 26) is acceptable.
                    #
                    all_zeroes = True
                    negate = False
                    for i in range(len(self.matrix[0]) - 1):
                        coeff = new_row[i]
                        if coeff != 0:
                            if all_zeroes == True and coeff < 0:
                                negate = True
                            all_zeroes = False
                            if negate == True:
                                new_row[i] *= -1
                    if negate == True:
                        new_row[-1] *= -1
                    if (all_zeroes == True) and (new_row[-1] % 26 != 0):
                        raise RotationMatrixException(f"Bad row reduction for {self.known_plaintext_slices}")

            print(f"After {pivot_row_index+1} iteration(s), matrix now:")
            print(self)

        self.reduced = True

    def get_rotations(self):
        if (self.reduced == False):
            self.reduce()
        rotations = {}
        for row in self.matrix:
            # At this point, the reduction is complete, and we need to take the RHS % 26 to get
            # the actual rotation value for the word.
            row[-1] %= 26
            l = [(mult, word) for (mult, word) in zip(row, self.unique_words) if mult != 0]
            if len(l) > 0:
                # First non-zero coefficient should always be 1 for a matrix in reduced row
                # echelon form. Anything else means we have a bug. (Commented out- this is not
                # the case for an integer-only row reduced matrix)
                #
                #assert(l[0][0] == 1)
                print("non-zero multipliers:", l, "=>", row[-1])
            for (mult, word) in l:
                #
                # Build a list of row equations for this code word for later evaluation.
                #
                eq = (l, row[-1])
                if word in rotations:
                    rotations[word].append(eq)
                else:
                    rotations[word] = [eq]

        print(f"{len(rotations)} rotations: {rotations}")
        return(rotations)
