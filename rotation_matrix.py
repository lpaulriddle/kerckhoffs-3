import collections

def find_pivot(mat, start_row_index):
    # Iterate through the columns (except for the RHS, which we don't want to
    # ever use as a pivot)
    for col_num in range(len(mat[0]) - 1):
        min_pivot_val = 1000
        min_pivot_row = -1
        for row_num in range(start_row_index, len(mat)):

            #
            # Rather than blindly selecting the first non-zero pivot value, look for the
            # smallest non-zero pivot value we can find (preferably a 1). This is to
            # try to avoid dividing by large numbers.
            #
            val = mat[row_num][col_num]
            if abs(val) == 1:
                min_pivot_row = row_num
                break
            if (val != 0) and (abs(val) < abs(min_pivot_val)):
                min_pivot_val = mat[row_num][col_num]
                min_pivot_row = row_num
                print("Found potential pivot (%d,%d) value %f" % (row_num, col_num, mat[row_num][col_num]))
        if min_pivot_row >= 0:
            print(f"Using pivot {min_pivot_row}, {col_num} (value {mat[min_pivot_row][col_num]})")
            return(min_pivot_row, col_num)
    print("No pivot found")
    return (None, None)

def gauss_jordan_reduce(mat, words):
    good_matrix = True
    for row_index in range(len(mat)):
        (pivot_row_index, pivot_col_index) = find_pivot(mat, row_index)
        if pivot_row_index == None:
            break
        assert(pivot_row_index >= row_index)
        if pivot_row_index > row_index:
            print("swap rows %d and %d" % (row_index, pivot_row_index))
            temp = mat[row_index]
            mat[row_index] = mat[pivot_row_index]
            mat[pivot_row_index] = temp
            #print("matrix now", mat)

        pivot_val = mat[row_index][pivot_col_index]

        #
        # Transform row to make pivot equal 1
        # This also converts everything to floating point
        #
        mat[row_index] = [i / pivot_val for i in mat[row_index]]

        #
        # Transform other rows so that everything else in the pivot column is zero
        #
        pivot_row = mat[row_index]
        print("Pivot row: %s; first nonzero index: %d" % (pivot_row, pivot_col_index))
        for secondary_row_index in range(0, len(mat)):
            if secondary_row_index == row_index:
                continue
            secondary_row = mat[secondary_row_index]

            #
            # Most of the numbers in the matrix represent code word frequencies, not
            # rotation values, so should not be taken modulo 26. The exception is the
            # final row in the matrix, which is the RHS of that row's equation.
            # NOTE!! Can't take RHS % 26 until after the row reduction is completely
            # finished. This is because we have to keep track of whether it is positive or
            # negative (e.g. does 24 represent +24 or -2), or "bad things will happen(tm)"
            # when we try to divide the RHS by anything.
            #
            if secondary_row[pivot_col_index] != 0:
                row_mult = [x * secondary_row[pivot_col_index] for x in pivot_row]
                #print(f"row_mult for row {secondary_row_index:2} = {row_mult}")
                new_row = [x-y for (x,y) in zip(secondary_row, row_mult)]
                #print(f"modified row {secondary_row_index:2}     = {new_row}")
                #print("new_row %s" % new_row)
                mat[secondary_row_index] = new_row

                #
                # Look for a row of all zeroes except the RHS
                # Not sure if doing this now will work, or if it needs to be done after the
                # reduction completes. I guess I'll find out
                #
                # Another fun "gotcha" here: with a typical matrix, a row of all zeros except
                # the RHS means the matrix is indeterminant (no solution). However, in this
                # case, since we're dealing with rotations, any RHS that equals 0 (mod 26) is
                # acceptable.
                #
                if all(v == 0 for v in new_row[:-1]) and (new_row[-1] % 26 != 0):
                    good_matrix = False
                    
        #print("Subsequent rows: %s" % mat[row_index+1:])
        #print("After %d iteration(s), matrix now:" % (row_index+1))
        #print_matrix(mat, words)

    # Can't have a non-integer rotation value
    if (good_matrix == True) and any(not(row[-1].is_integer()) for row in mat):
        good_matrix = False
    print("Reduced matrix:")
    #print_matrix(mat,words)
    return(good_matrix)

def get_computed_codeword_rotations(matrix, words):
    rotations = {}
    for row in matrix:
        # Can't have a fractional rotation value
        assert(row[-1].is_integer())

        # At this point, the reduction is complete, and we need to take the RHS % 26 to get
        # the actual rotation value for the word.
        row[-1] %= 26
        l = [(mult, word) for (mult, word) in zip(row, words) if mult != 0]
        if len(l) > 0:
            # First non-zero coefficient should always be 1 for a matrix in reduced row
            # echelon form. Anything else means we have a bug.
            assert(l[0][0] == 1.0)
            print("non-zero multipliers:", l, "=>", row[-1])
        for (mult, word) in l:
            #
            # Build a list of row equations for this code word for later evaluation.
            #
            eq = (l, int(row[-1]))
            if word in rotations:
                rotations[word].append(eq)
            else:
                rotations[word] = [eq]

    print(f"{len(rotations)} rotations: {rotations}")
    return(rotations)

def build_rotation_matrix_new(cipher_list, text_offset_list):
    def print_matrix(mat, unique_words):
        line_no = 0
        for i in mat:
            zthing = [(w,x) for (w,x) in zip(unique_words, i) if x != 0]
            words = [w for (w,x) in zthing]
            total = sum([int(w[-1]) * x for (w,x) in zthing]) % 26
            print('{:2}:'.format(line_no), ' '.join(['{:-4.1f}'.format(x) for x in i]), '({:4.1f}) {:4.1f}'.format(i[-1] % 26, total), words)
            # This won't work with #3, because it assumes the last digit of the code word == the rotation
            #if total != (i[-1] % 26):
            #    print("aah.. no..")
            line_no += 1

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
                    # being the matrix coefficients
                    #
                    word_counts = collections.Counter(cipher[last_index:word_index])
                    matrix_row = [word_counts[x] if x in word_counts else 0 for x in self.unique_words]
                    matrix_row.append(required_rot)
                    self.matrix.append(matrix_row)

                last_occurrence_of[word] = (word_index, ch)

    def __str__(self):
        output = []
        # Number the columns. Each column corresponds to a word per self.unique_words
        output.append('   ' + ' '.join(['{:4}'.format(x) for x in range(len(self.matrix[0]) - 1)]))
        for (line_no, row) in enumerate(self.matrix):
            # I originally pulled non-zero entries so the words could be shown at the end of each row.
            # Probably not necessary to do this any more
            non_zero_entries = [(w,x) for (w,x) in zip(self.unique_words, row) if x != 0]
            total = sum([int(w[-1]) * x for (w,x) in non_zero_entries]) % 26
            output.append('{:2}:'.format(line_no) +
                          ' '.join(['{:-4.1f}'.format(x) for x in row]) +
                          '({:4.1f}) {:4.1f}'.format(row[-1] % 26, total))
        return "\n".join(output)

    def reduce(self):
        if gauss_jordan_reduce(self.matrix, "bonechip") == False:
            raise RotationMatrixException(f"Bad row reduction for {self.known_plaintext_slices}")

    def get_rotations(self):
        return get_computed_codeword_rotations(self.matrix, self.unique_words)
