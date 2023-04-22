'''import math

angle1 = float(input("Enter angle 1 in radians: "))
c1 = math.cos(angle1)
s1 = math.sin(angle1)

angle2 = float(input("Enter angle 2 in radians: "))
c2 = math.cos(angle2)
s2 = math.sin(angle2)

angle3 = float(input("Enter angle 3 in radians: "))
c3 = math.cos(angle3)
s3 = math.sin(angle3)

angle4 = float(input("Enter angle 4 in radians: "))
c4 = math.cos(angle4)
s4 = math.sin(angle4)

angle5 = float(input("Enter angle 5 in radians: "))
c5 = math.cos(angle5)
s5 = math.sin(angle5)

print("angle1 =", angle1, "c1 =", c1, "s1 =", s1)
print("angle2 =", angle2, "c2 =", c2, "s2 =", s2)
print("angle3 =", angle3, "c3 =", c3, "s3 =", s3)
print("angle4 =", angle4, "c4 =", c4, "s4 =", s4)
print("angle5 =", angle5, "c5 =", c5, "s5 =", s5)'''


import math

# Initialize lists to store the angles, sines, and cosines
angles = []
sines = []
cosines = []

# Get input angles and calculate their sines and cosines
for i in range(5):
    angle_str = input("Enter angle #{} in multiples of pi (e.g. -1/2 or 1 1/4): ".format(i+1))
    angle_parts = angle_str.split()
    numerator, denominator = 0, 1
    for part in angle_parts:
        if '/' in part:
            frac_parts = part.split('/')
            numerator += int(frac_parts[0]) / int(frac_parts[1])
        else:
            numerator += int(part)
    angle = numerator * math.pi
    angles.append(angle)
    sines.append(math.sin(angle))
    cosines.append(math.cos(angle))


# overwrite angles

angles = [1,2,3,4,999]
sines = [math.sin(x) for x in angles]
cosines = [math.cos(x) for x in angles]
# Assign the values to angle1-5, s1-5, and c1-5
angle1, angle2, angle3, angle4, angle5 = angles
s1, s2, s3, s4, s5 = sines
c1, c2, c3, c4, c5 = cosines

# Print out the angles and their sines and cosines
print("The input angles in radians are:", angles)
print("Their sines are:", sines)
print("Their cosines are:", cosines)



a2 = 16
a3 = 105
a4 = 90
d5 = 65

matrix_list = [[c5*math.sin(angle2+angle3+angle4)*c1 - s5*s1, -s5*math.cos(angle2+angle3+angle4)*c1 - c5*s1, math.sin(angle2+angle3+angle4)*c1, a2*c1*c2 + a3*c1*math.cos(angle2+angle3) + a4*math.cos(angle2+angle3+angle4)*c1 + d5*math.cos(angle2+angle3+angle4)*c1],
          [c5*math.cos(angle2+angle3+angle4)*c1 + s5*c1, -s5*math.cos(angle2+angle3+angle4)*s1 + c5*c1, math.sin(angle2+angle3+angle4)*s1, a2*s1*c2 + a3*s1*math.cos(angle2+angle3) + a4*math.cos(angle2+angle3+angle4)*s1 + d5*math.cos(angle2+angle3+angle4)*s1],
          [-c5*math.sin(angle2+angle3+angle4), s5*math.sin(angle2+angle3+angle4), math.cos(angle2+angle3+angle4), -d5*math.sin(angle2+angle3+angle4)-a2*s2-a3*math.sin(angle2+angle3)-a4*math.sin(angle2+angle3+angle4)],
          [0, 0, 0, 1]]

from pprint import pprint

for row in matrix_list:
    row = ["{:.2f}".format(x) for x in row]
    print(row)

# pprint(matrix)

import numpy as np

# Example 4x4 2D list , matrix_list

# Convert to NumPy array
matrix = np.array(matrix_list)

# Extract the upper-left 3x3 matrix
upper_left_3x3 = matrix[:3, :3]

# Calculate the determinant of the upper-left 3x3 matrix
determinant = np.linalg.det(upper_left_3x3)

print("Upper-left 3x3 matrix:")
print(upper_left_3x3)
print("Determinant of upper-left 3x3 matrix:", determinant)