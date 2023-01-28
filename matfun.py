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
    return (None, None)

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

# Above matrix in reduced row echelon form:
# 1.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  1.0  1.0  1.0  0.0  0.0  0.0  0.0  0.0 12.0     21+652655+7073281+7614435 = 12
# 0.0  1.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  8.0     308 = 8
# 0.0  0.0  1.0  0.0  0.0  0.0  0.0  0.0  0.0  1.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  6.0     391+652655 = 6
# 0.0  0.0  0.0  1.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  5.0     4045 = 5
# 0.0  0.0  0.0  0.0  1.0  0.0  0.0  0.0  1.0  1.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  7.0     50461+641971+652655 = 7
# 0.0  0.0  0.0  0.0  0.0  1.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  3.0     52123 = 3
# 0.0  0.0  0.0  0.0  0.0  0.0  1.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  9.0     55709 = 9
# 0.0  0.0  0.0  0.0  0.0  0.0  0.0  1.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  7.0     59207 = 7
# 0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  1.0  0.0  0.0  0.0  0.0  5.0     7699855 = 5
# 0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  1.0  0.0  0.0  0.0  9.0     7811539 = 9
# 0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  1.0  0.0  0.0  1.0     7954481 = 1
#-0.0 -0.0 -0.0 -0.0 -0.0 -0.0 -0.0 -0.0 -0.0 -0.0 -0.0 -0.0 -0.0 -0.0 -0.0  1.0 -0.0  9.0     89447709 = 9
# 0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.0

#
# Known bad matrix (K3 with 'norththirtyninedegreestenpoint' at index zero)
#
#mat = [[0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 1, 20],
#       [0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0],
#       [0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 1, 0, 0, 1, 0, 20],
#       [1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 22],
#       [1, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 2, 0, 8],
#       [1, 0, 0, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 17],
#       [1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 15],
#       [2, 1, 1, 3, 1, 1, 1, 2, 0, 1, 1, 1, 1, 2, 1, 1, 0, 2, 1, 25],
#       [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 11],
#       [1, 2, 0, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 23],
#       [2, 2, 0, 1, 2, 1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 0, 0, 1, 1, 9]]

#mat = [[0,0,-3,1],
#       [12,-4,5,-6],
#       [15,3,2,1]]

#mat = [[0,-4,5,-6],
#       [0,3,2,1],
#       [2,0,-3,1]]

#
# Put the matrix into reduced-row echelon form (Gauss-Jordan reduction)
#
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
        print("matrix now", mat)

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
            new_row = [x-y for (x,y) in zip(secondary_row, row_mult)]
            new_row[-1] %= 26
            print("new_row %s" % new_row)
            mat[secondary_row_index] = new_row

    print("Subsequent rows: %s" % mat[row_index+1:])
    print("After %d iteration(s), matrix now:" % (row_index+1))
    for i in mat:
        print(' '.join(['{:-4.1f}'.format(x) for x in i]))
exit(0)
