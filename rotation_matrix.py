import collections
import math

def _swap_columns(mat, unique_words, col_index1, col_index2):
    unique_words[col_index1], unique_words[col_index2] = unique_words[col_index2], unique_words[col_index1]
    for row in mat:
        row[col_index1], row[col_index2] = row[col_index2], row[col_index1]

def _find_pivot(mat, unique_words, starting_row_num):

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

def gauss_jordan_reduce(mat, unique_words):
    for pivot_row_index in range(len(mat)):
        pivot_col_index = _find_pivot(mat, unique_words, pivot_row_index)
        if pivot_col_index == None:
            break
        pivot_val = mat[pivot_row_index][pivot_col_index]
        assert(pivot_val != 0)

        #
        # Reduce/simplify the pivot row if possible
        #
        if abs(pivot_val) > 1:
            row_gcd = math.gcd(*mat[pivot_row_index])
            if row_gcd > 1:
                mat[pivot_row_index] = [x // row_gcd for x in mat[pivot_row_index]]
                pivot_val = mat[pivot_row_index][pivot_col_index]

        #
        # Transform other rows so that everything else in the pivot column is zero
        #
        pivot_row = mat[pivot_row_index]
        #print(f"Pivot row: {pivot_row}; first nonzero index: {pivot_col_index}")
        for secondary_row_index in range(0, len(mat)):
            if secondary_row_index == pivot_row_index:
                # Skip the pivot row
                continue
            secondary_row = mat[secondary_row_index]

            secondary_pivot_col_val = secondary_row[pivot_col_index]
            if secondary_pivot_col_val != 0:
                lcm = math.lcm(pivot_val, secondary_pivot_col_val)
                secondary_row = [x * (lcm // secondary_pivot_col_val) for x in secondary_row]
                pivot_row_multiple = [x * (lcm // pivot_val) for x in pivot_row]

                new_row = [(x-y) for (x,y) in zip(secondary_row, pivot_row_multiple)]
                mat[secondary_row_index] = new_row

                #
                # Look for a bad reduction (a row of all zero coefficients with a non-zero RHS)
                # and also negate the row if the leading non-zero entry is negative. Not the most
                # elegant or "Pythonic" code, but gets the job done fairly straightforwardly.
                #
                # Note that with a "regular" matrix, a row of all zeros except the RHS means the]
                # matrix is indeterminant (no solution). However, in this case, since we're
                # dealing with rotations, any RHS that equals 0 (mod 26) is acceptable.
                #
                all_zeroes = True
                negate = False
                for i in range(len(mat[0]) - 1):
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
                    return False
                    
        #print("Subsequent rows: %s" % mat[row_index+1:])
        print(f"After {pivot_row_index+1} iteration(s), matrix now:")
        print_matrix(mat, unique_words)

    #print("Reduced matrix:")
    #print_matrix(mat, unique_words)
    return True

def get_computed_codeword_rotations(matrix, words):
    rotations = {}
    for row in matrix:
        # At this point, the reduction is complete, and we need to take the RHS % 26 to get
        # the actual rotation value for the word.
        row[-1] %= 26
        l = [(mult, word) for (mult, word) in zip(row, words) if mult != 0]
        if len(l) > 0:
            # First non-zero coefficient should always be 1 for a matrix in reduced row
            # echelon form. Anything else means we have a bug.
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

def print_matrix(mat, unique_words):
    line_no = 0
    print('    ' + ' '.join(['{:3}'.format(x) for x in range(len(mat[0]) - 1)]))
    for i in mat:
        zthing = [(w,x) for (w,x) in zip(unique_words, i) if x != 0]
        #words = [w for (w,x) in zthing]
        total = sum([int(w[-1]) * x for (w,x) in zthing]) % 26
        #print('{:2}:'.format(line_no), ' '.join(['{:-4.1f}'.format(x) for x in i]), '({:4.1f}) {:4.1f}'.format(i[-1] % 26, total), words)
        print('{:2}:'.format(line_no), ' '.join(['{:-3}'.format(x) for x in i]), '({:3}) {:3}'.format(i[-1] % 26, total))
        # This won't work with #3, because it assumes the last digit of the code word == the rotation
        #if total != (i[-1] % 26):
        #    print("aah.. no..")
        line_no += 1

def build_rotation_matrix_new(cipher_list, text_offset_list):
    def build_initial_matrix(text, cipher_slice, unique_words):
        assert(len(cipher_slice) == len(text))
        last_occurrence_of = {}
        print(f"cipher slice: {cipher_slice} ({len(text)} total words)")
        #print(f"cipher slice has {len(text)} total words ({len(unique_words)} unique)")
        matrix = []
        for i in range(len(text)):
            word = cipher_slice[i]
            if word not in last_occurrence_of:
                last_occurrence_of[word] = i
                continue
            l = last_occurrence_of[word]
            required_rot = (ord(text[i]) - ord(text[l])) % 26
            print(f"Required total rotation between {l} and {i} = {required_rot}")
            sl = cipher_slice[l:i]
            print("Slice", sl)

            counts = {}
            for j in sl:
                if j in counts:
                    counts[j] += 1
                    continue
                counts[j] = 1
            matrix_row = []
            for j in unique_words:
                if j in counts:
                    matrix_row.append(counts[j])
                    continue
                matrix_row.append(0)
            matrix_row.append(required_rot)
            matrix.append(matrix_row)
            last_occurrence_of[word] = i
        return matrix

    #
    # unique_words has to be the superset of unique words in every slice, because the columns need to be
    # consistent across all the matrices we generate
    # TBD: probably can skip this step and just use the entire cipher alphabet (cipher.unique_words),
    # but let's see if we can get this working at all first...
    #
    unique_words = []
    cipher_slices = []
    for (text, offset) in text_offset_list:
        # Make sure we don't fall off the end of the cipher.
        # We also don't want any slices to overlap, but that part is left as an exercise to the caller ;)
        assert(len(text) <= len(cipher_list) - offset)
        cipher_slice = cipher_list[offset:len(text) + offset]
        cipher_slices.append(cipher_slice)
        unique_words.extend(cipher_slice)
    unique_words = list(set(unique_words))
    unique_words.sort()
    print("unique words:", unique_words)

    matrix = []
    
    for (text, cipher_slice) in zip([i[0] for i in text_offset_list], cipher_slices):
        partial_matrix = build_initial_matrix(text, cipher_slice, unique_words)
        print(f"Initial matrix for '{text}':")
        print_matrix(partial_matrix, unique_words)
        matrix.extend(partial_matrix)

    print("Full matrix before row reduction:")
    print_matrix(matrix, unique_words)
    result = gauss_jordan_reduce(matrix, unique_words)
    if result == False:
        print(f"Bad reduction for {text_offset_list}")
        return None
    known_rotations = get_computed_codeword_rotations(matrix, unique_words)
    print(f"Good reduction for {text_offset_list} - {len(known_rotations)} computed rotations: {known_rotations}")
    return known_rotations

def build_rotation_matrix(cipher_list, text, offset):
    text_offset_list = [(text, offset)]
    return build_rotation_matrix_new(cipher_list, text_offset_list)

class RotationMatrixException(Exception):
    pass

class RotationMatrix:
    def __init__(self, cipher, *slices):
        self.known_plaintext_slices = sorted(slices)
        self.unique_words = cipher.unique_words
        self.matrix = []

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

    def reduce(self):
        if gauss_jordan_reduce(self.matrix, self.unique_words) == False:
            raise RotationMatrixException(f"Bad row reduction for {self.known_plaintext_slices}")

    def get_rotations(self):
        return get_computed_codeword_rotations(self.matrix, self.unique_words)
