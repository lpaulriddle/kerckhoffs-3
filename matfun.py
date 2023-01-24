#!/usr/bin/env python3 -u

from math import lcm

def find_pivot(mat, start_row_index):
    # Iterate through the columns
    for col_num in range(len(mat[0])):
        for row_num in range(start_row_index, len(mat)):
            if mat[row_num][col_num] != 0:
                print("Found pivot (%d,%d)" % (row_num, col_num))
                return (row_num, col_num)
    print("No pivot found")
    return None

mat = [[5,6,7,8,9],
       [6,7,8,9,1],
       [2,3,4,5,6]]

mat = [[0,1,1,1,4],
       [2,0,1,0,8],
       [1,1,1,0,7],
       [0,1,0,2,3]]

#
# Known good matrix - Beginning of K2 cipher with known plaintext
#
# K2 words in matrix order (ones digits correspond to rotation values):
# ['21', '308', '391', '4045', '50461', '52123', '55709', '59207', '641971', '652655', '7073281', '7614435', '7699855', '7811539', '7954481', '89447709', '945432286']
#
# [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, -9]  # 52123 7699855 7811539
#
mat = [[0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9],  # 55709             =  9
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1],  # 7954481           =  1
       [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 11], # 55709+(7954481*2) = 11
       [0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 23],
       [1, 0, 0, 1, 0, 0, 4, 0, 0, 1, 1, 1, 0, 0, 2, 1, 0, 12],
       [0, 0, 0, 0, 1, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 16],
       [0, 0, 0, 1, 1, 0, 2, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 20],
       [0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 8],
       [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 17],
       [0, 2, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 7],
       [0, 2, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 2, 1, 0, 2, 0, 1],
       [0, 2, 1, 1, 1, 1, 2, 1, 1, 2, 0, 0, 2, 1, 0, 2, 0, 21],
       [0, 2, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 2, 1, 0, 1, 0, 6]]

#
# Row-reduced matrix with no moduli taken:
# [1, 0, 0, 1, 0, 0, 4, 0, 0, 1, 1, 1, 0, 0, 2, 1, 0, 12]
# [0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 8]
# [0, 0, -1, -1, -1, 1, -2, -1, -1, -2, 0, 0, 0, 1, 0, 0, 0, -5]
# [0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 23]
# [0, 0, 0, 0, 1, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 16]
# [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, -9]
# [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9]
# [0, 0, 0, 0, 0, 0, 0, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 19]
# [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, 0, 0, 0, 0, 21]
# [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, 0, -1, 0, -18]
# [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1]
# [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, 0, -9]
# [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
#

#
# Known bad matrix (K3 with 'norththirtyninedegreestenpoint' at index zero)
#
mat = [[0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 1, 20],
       [0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0],
       [0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 1, 0, 0, 1, 0, 20],
       [1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 22],
       [1, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 2, 0, 8],
       [1, 0, 0, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 17],
       [1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 15],
       [2, 1, 1, 3, 1, 1, 1, 2, 0, 1, 1, 1, 1, 2, 1, 1, 0, 2, 1, 25],
       [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 11],
       [1, 2, 0, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 23],
       [2, 2, 0, 1, 2, 1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 0, 0, 1, 1, 9]]

#mat = [[0,0,-3,1],
#       [12,-4,5,-6],
#       [15,3,2,1]]

#mat = [[0,-4,5,-6],
#       [0,3,2,1],
#       [2,0,-3,1]]

for row_index in range(len(mat)-1):
    (pivot_row_index, pivot_col_index) = find_pivot(mat, row_index)
    assert(pivot_row_index >= row_index)
    if pivot_row_index > row_index:
        print("swap rows %d and %d" % (row_index, pivot_row_index))
        temp = mat[row_index]
        mat[row_index] = mat[pivot_row_index]
        mat[pivot_row_index] = temp
        print("matrix now", mat)

    pivot_row = mat[row_index]
    print("Pivot row: %s; first nonzero index: %d" % (pivot_row, pivot_col_index))
    for secondary_row_index in range(row_index+1, len(mat)):
        secondary_row = mat[secondary_row_index]

        #
        # The numbers in the matrix (with exception of the final column) represent
        # the frequencies of each code word in the cipher slice, NOT the rotation
        # values themselves. Thus, I don't think any moduli should be taken at this
        # stage. We're calculating the LCM of multipliers, not rotation values.
        #
        # Thinking final column is an exception, as it's the RHS of the equation and
        # the result of multipling moduli by frequencies...
        #
        coef = lcm(pivot_row[pivot_col_index], secondary_row[pivot_col_index])

        #
        # The LCM will be zero if the corresponding number in the second row is zero.
        # In this case, leave things as-is, and the row will bubble its way to the bottom
        # of the matrix.
        #
        if coef != 0:
            row_mult1 = [x * (coef//pivot_row[pivot_col_index]) for x in pivot_row]
            row_mult2 = [x * (coef//secondary_row[pivot_col_index]) for x in secondary_row]
            new_row = [a-b for (a,b) in zip(row_mult1, row_mult2)]
            new_row[-1] %= 26   # Adjust RHS column only
            print("new_row %s" % new_row)
            mat[secondary_row_index] = new_row
    print("Subsequent rows: %s" % mat[row_index+1:])
    print("After %d iteration(s), matrix now:" % (row_index+1))
    for i in mat:
        print(' '.join(['{:-3}'.format(x) for x in i]))
exit(0)
