#!/usr/bin/env python3 -u

from math import lcm

#mat = [[5,6,7,8,9],
#       [6,7,8,9,1],
#       [2,3,4,5,6]]

mat = [[12,-4,5,-6],
       [15,3,2,1],
       [2,0,-3,1]]

coef = lcm(mat[0][0], mat[1][0])
rof1 = [x * (coef//mat[0][0]) for x in mat[0]]
rof2 = [x * (coef//mat[1][0]) for x in mat[1]]
newrow = [a-b for (a,b) in zip(rof1,rof2)]
print(coef)
print(rof1)
print(rof2)
print(newrow)

print("gads")

for row_index in range(len(mat)-1):
    pivot_row = mat[row_index]
    first_nonzero_index = next((i for (i,x) in enumerate(pivot_row) if x != 0), None)
    print("Pivot row: %s; first nonzero index: %d" % (pivot_row, first_nonzero_index))
    for secondary_row_index in range(row_index+1, len(mat)):
        secondary_row = mat[secondary_row_index]
        coef = lcm(pivot_row[first_nonzero_index], secondary_row[first_nonzero_index])
        row_mult1 = [x * (coef//pivot_row[first_nonzero_index]) for x in pivot_row]
        row_mult2 = [x * (coef//secondary_row[first_nonzero_index]) for x in secondary_row]
        new_row = [a-b for (a,b) in zip(row_mult1, row_mult2)]
        print("new_row %s" % new_row)
        mat[secondary_row_index] = new_row
    print("Subsequent rows: %s" % mat[row_index+1:])
    print("After %d iteration(s), matrix now = %s" % (row_index+1, mat))

#for row_index in range(len(mat)-1):
#    pivot_row = mat[row_index]
#    new_mat = [pivot_row]
#    print("Pivot row: %s" % pivot_row)
#    thing = zip([pivot_row] * (len(mat)-row_index-1), mat[row_index+1:])
#    first_nonzero_index = next((i for (i,x) in enumerate(pivot_row) if x != 0), None)
#    print("first nonzero index = %d" % first_nonzero_index)
#    for (row1, row2) in thing:
#        coef = lcm(row1[first_nonzero_index], row2[first_nonzero_index])
#        row_mult1 = [x * (coef//row1[first_nonzero_index]) for x in row1]
#        row_mult2 = [x * (coef//row2[first_nonzero_index]) for x in row2]
#        new_row = [a-b for (a,b) in zip(row_mult1, row_mult2)]
#        print("new_row %s" % new_row)
#        new_mat.append(new_row)
#    print("Subsequent rows: %s" % mat[row_index+1:])
#    print("new_mat %s" % new_mat)
#    assert(len(mat) == len(new_mat))

#new_mat = [mat[0].copy()]
#thing = zip([mat[0]] * (len(mat)-1), mat[1:])
#for (row1, row2) in thing:
#    first_nonzero = next((i for (i,x) in enumerate(mat[0]) if x != 0), None)
#    coef = lcm(row1[first_nonzero], row2[first_nonzero])
#    row_mult1 = [x * (coef//row1[first_nonzero]) for x in row1]
#    row_mult2 = [x * (coef//row2[first_nonzero]) for x in row2]
#    print("coef %d rm1 %s rm2 %s" % (coef, row_mult1, row_mult2))
#    new_row = [a-b for (a,b) in zip(row_mult1, row_mult2)]
#    new_mat.append(new_row)

#print("new_mat %s" % new_mat)
