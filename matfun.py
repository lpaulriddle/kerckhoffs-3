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

#mat = [[5,6,7,8,9],
#       [6,7,8,9,1],
#       [2,3,4,5,6]]

mat = [[0,0,-3,1],
       [12,-4,5,-6],
       [15,3,2,1]]

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
            print("new_row %s" % new_row)
            mat[secondary_row_index] = new_row
    print("Subsequent rows: %s" % mat[row_index+1:])
    print("After %d iteration(s), matrix now = %s" % (row_index+1, mat))
exit(0)
