def build_rotation_matrix(cipher_list, text, offset):
    def find_pivot(mat, start_row_index):
        # Iterate through the columns (except for the RHS, which we don't want to
        # ever use as a pivot)
        for col_num in range(len(mat[0]) - 1):
            for row_num in range(start_row_index, len(mat)):
                if mat[row_num][col_num] != 0:
                    print("Found pivot (%d,%d)" % (row_num, col_num))
                    return (row_num, col_num)
        print("No pivot found")
        return (None, None)

    def gauss_jordan_reduce(mat, words):
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
            # One of the "gotchas" of taking everything (mod 26) is that we need to
            # make sure the values in the rightmost column are positive before
            # dividing them by anything, or "bad things will happen"(tm)
            #
            if pivot_val < 0:
                print(f"**Negative pivot val {pivot_val}")
                mat[row_index] = [-x for x in mat[row_index]]
                pivot_val = -pivot_val
                mat[row_index][-1] %= 26

            #
            # Transform row to make pivot equal 1
            # This also converts everything to floating point
            #
            mat[row_index] = [i / pivot_val for i in mat[row_index]]

            #
            # Transform other rows so that everything else in the pivot column is zero
            #
            pivot_row = mat[row_index]
            pivot_row[-1] %= 26
            print("Pivot row: %s; first nonzero index: %d" % (pivot_row, pivot_col_index))
            for secondary_row_index in range(0, len(mat)):
                if secondary_row_index == row_index:
                    continue
                secondary_row = mat[secondary_row_index]

                #
                # Most of the numbers in the matrix represent code word frequencies, not
                # rotation values, so should not be taken modulo 26. The exception is the
                # final row in the matrix, which is the RHS of that row's equation.
                #
                if secondary_row[pivot_col_index] != 0:
                    row_mult = [x * secondary_row[pivot_col_index] for x in pivot_row]
                    #print(f"row_mult for row {secondary_row_index:2} = {row_mult}")
                    new_row = [x-y for (x,y) in zip(secondary_row, row_mult)]
                    #print(f"modified row {secondary_row_index:2}     = {new_row}")
                    new_row[-1] %= 26
                    #print("new_row %s" % new_row)
                    mat[secondary_row_index] = new_row

            #print("Subsequent rows: %s" % mat[row_index+1:])
            print("After %d iteration(s), matrix now:" % (row_index+1))
            print_matrix(mat, words)

    def get_computed_codeword_rotations(matrix, words):
        rotations = {}
        for row in matrix:
            l = [(mult, word) for (mult, word) in zip(row, words) if mult != 0]
            if len(l) > 0:
                print("non-zero multipliers:", l, "=>", row[-1])
            # TBD: handle rows with multiple entries in the backtracking algo somehow
            if len(l) == 1:
                (mult, word) = l[0]
                # multiplier should always be 1 for a matrix in reduced row echelon form.
                # anything else means we have a bug
                assert(mult == 1.0)
                assert(row[-1].is_integer())   # Can't have a fractional rotation value
                rotations[word] = int(row[-1])
        return(rotations)

    def print_matrix(mat, unique_words):
        line_no = 0
        for i in mat:
            zthing = [(w,x) for (w,x) in zip(unique_words, i) if x != 0]
            words = [w for (w,x) in zthing]
            total = sum([int(w[-1]) * x for (w,x) in zthing]) % 26
            print('{:2}:'.format(line_no), ' '.join(['{:-4.1f}'.format(x) for x in i]), '{:4.1f}'.format(total), words)
            if total != i[-1]:
                print("aah.. no..")
            line_no += 1

    assert(len(text) <= len(cipher_list) - offset)
    cipher = cipher_list[offset:len(text) + offset]
    last_occurrence_of = {}
    unique_words = list(set(cipher))
    unique_words.sort()
    print("cipher slice:", cipher)
    print("cipher slice has %d total words (%d unique)" % (len(text), len(unique_words)))
    print("unique words:", unique_words)
    matrix = []
    for i in range(len(text)):
        word = cipher[i]
        if word not in last_occurrence_of:
            last_occurrence_of[word] = i
            continue
        l = last_occurrence_of[word]
        required_rot = (ord(text[i]) - ord(text[l])) % 26
        print("Required total rotation between %d and %d = %d" % (l, i, required_rot))
        sl = cipher[l:i]
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
        
    print("unique words:", unique_words)
    print("Initial matrix:")
    print_matrix(matrix, unique_words)
    gauss_jordan_reduce(matrix, unique_words)
    known_rotations = get_computed_codeword_rotations(matrix, unique_words)
    print("Computed rotations", known_rotations)
    return(known_rotations)
