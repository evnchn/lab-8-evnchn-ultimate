import os
from sympy import *
import math
import sys

build_theta_debug = False
th1, th2, th3, th4, th5 = symbols("th1, th2, th3, th4, th5")

"""
print("BUILD WARNING: defining th1-5 to 1,2,3,4,5")
build_theta_debug = True
th1, th2, th3, th4, th5 = 1,2,3,4,5"""

def check_upper_left_det(matrix):
    print("Performing sanity check for the determinant of rotation matrix...", end="", flush=True)
    # Extract the upper-left 3x3 matrix
    upper_left_3x3 = matrix[:3, :3]
    
    # Calculate the determinant of the upper-left 3x3 matrix
    det = upper_left_3x3.det()
    try:
        det = simplify(det)
    except:
        pass
    # Check if the determinant is not close to 1 within the default tolerance
    try:
        if not math.isclose(det, 1):
            print("")
            print("SANITY CHECK FAILED: Determinant of upper-left 3x3 matrix is not numerically close to 1.")
            print(det.evalf())
        else:
            print("OK!")
    except:
        print("")
        print("SANITY CHECK FAILED: Determinant of upper-left 3x3 matrix is an expression not a number but an expression!")
        print(det.evalf())
    return det

DH_params_LeArm = None
DH_params_LeArm_buggy = None


def update_DH_params_using_th():
    global DH_params_LeArm, DH_params_LeArm_buggy
    DH_params_LeArm = Matrix([
        # you need the first row of all 0s for standard form
        [0, 0, 0, 0],
        [-pi/2, 0, 0, th1],
        [0, 16, 0, th2],
        [0, 105, 0, th3],
        [pi/2, 90, 0, th4], #buggy version: [0, 90, 0, th4],
        [0, 0, 65, th5],
        [0, 0, 0, 0]
        # you need the last row of all 0s for standard form
    ])

    DH_params_LeArm_buggy = Matrix([
        # you need the first row of all 0s for standard form
        [0, 0, 0, 0],
        [-pi/2, 0, 0, th1],
        [0, 16, 0, th2],
        [0, 105, 0, th3],
        [0, 90, 0, th4], #normal version: [pi/2, 90, 0, th4],
        [0, 0, 65, th5],
        [0, 0, 0, 0]
        # you need the last row of all 0s for standard form
    ])
update_DH_params_using_th()


def clear_screen():
    # for Windows
    if os.name == 'nt':
        os.system('cls')
    # for macOS and Linux (here, os.name is 'posix')
    else:
        os.system('clear')


def get_transformation_matrices_standard(var1, var2, var3, var4):
    # CHECK THE VARIABLE ORDER HERE!!!
    # expected variable order: al_im1, a_im1, th_i, d_i

    # Winnie's definition of DH: A B C D

    # A needs al_im1
    A = Matrix([[1, 0, 0, 0],
                [0, cos(var1), -sin(var1), 0],
                [0, sin(var1), cos(var1), 0],
                [0, 0, 0, 1]
                ])

    # B needs a_im1
    B = Matrix([[1, 0, 0, var2],
                [0, 1, 0, 0],
                [0, 0, 1, 0],
                [0, 0, 0, 1]
                ])

    # C needs th_i
    C = Matrix([[cos(var3), -sin(var3), 0, 0],
                [sin(var3), cos(var3), 0, 0],
                [0, 0, 1, 0],
                [0, 0, 0, 1]
                ])

    # D needs d_i
    D = Matrix([[1, 0, 0, 0],
                [0, 1, 0, 0],
                [0, 0, 1, var4],
                [0, 0, 0, 1]
                ])
    final = A.multiply(B).multiply(C).multiply(D)

    return final, A, B, C, D


def get_transformation_matrices_modified(var1, var2, var3, var4):
    # CHECK THE VARIABLE ORDER HERE!!!
    # expected variable order: al_i, a_i, th_i, d_i

    # LeArm's definition of DH: C D B A

    # A needs al_i
    A = Matrix([[1, 0, 0, 0],
                [0, cos(var1), -sin(var1), 0],
                [0, sin(var1), cos(var1), 0],
                [0, 0, 0, 1]
                ])

    # B needs a_i
    B = Matrix([[1, 0, 0, var2],
                [0, 1, 0, 0],
                [0, 0, 1, 0],
                [0, 0, 0, 1]
                ])

    # C needs th_i
    C = Matrix([[cos(var3), -sin(var3), 0, 0],
                [sin(var3), cos(var3), 0, 0],
                [0, 0, 1, 0],
                [0, 0, 0, 1]
                ])

    # D needs d_i
    D = Matrix([[1, 0, 0, 0],
                [0, 1, 0, 0],
                [0, 0, 1, var4],
                [0, 0, 0, 1]
                ])

    final = C.multiply(D).multiply(B).multiply(A)

    return final, A, B, C, D


def show_transformation_matrix_proof_standard():
    print("i-1")
    print("    T   =")
    print("      i")
    print("")
    print("Rot_x(al_i-1)D_x(a_i-1)Rot_z(th_i)D_z(d_i)")
    print("")
    print("=")
    print("")
    # var("al_im1, a_im1, th_i, d_i") # cannot have minus sign in variable names this way
    var("th_i, d_i")
    al_im1 = Symbol('al_i-1')
    a_im1 = Symbol('a_i-1')

    final, A, B, C, D = get_transformation_matrices_standard(
        al_im1, a_im1, th_i, d_i)

    pprint(A, use_unicode=True)
    print("")
    pprint(B, use_unicode=True)
    print("")
    pprint(C, use_unicode=True)
    print("")
    pprint(D, use_unicode=True)
    print("")
    print("=")
    print("")
    check_upper_left_det(final)
    pprint(final, use_unicode=True)


def show_transformation_matrix_proof_modified():
    print("i-1")
    print("    T   =")
    print("      i")
    print("")
    # print("Rot_x(al_im1)D_x(a_im1)Rot_z(th_i)D_z(d_i)")
    # A B C D
    print("Rot_z(th_i)D_z(d_i)D_x(a_i)Rot_x(al_i)")
    # C D B A
    print("")
    print("=")
    print("")
    var("al_i, a_i, th_i, d_i")

    final, A, B, C, D = get_transformation_matrices_modified(
        al_i, a_i, th_i, d_i)

    pprint(C, use_unicode=True)
    print("")
    pprint(D, use_unicode=True)
    print("")
    pprint(B, use_unicode=True)
    print("")
    pprint(A, use_unicode=True)
    print("")
    print("=")
    print("")
    check_upper_left_det(final)
    pprint(final, use_unicode=True)

def show_robot_trans_modified(DHparams, angles = None):
    rows, _ = shape(DHparams)
    """for i in range(1, rows-1):
        pprint(DHparams.row(i))"""
    result = eye(4)
    for i in range(1, rows-1):
        # pprint(DH_params_LeArm.row(i))
        # i starts with 1 here
        print(f"A_{i} = ")
        alpha_i, A_i, d_i, theta_i = DHparams.row(i)
        # expected variable order: al_i, a_i, th_i, d_i
        final, _, _, _, _ = get_transformation_matrices_modified(alpha_i, A_i, theta_i, d_i)
        result = result.multiply(final)
        pprint(final)
        check_upper_left_det(result)
    if angles is None:
        print("Simplifying final matrix...", end="", flush=True)
        result = simplify(result)
        print("OK!")
        pprint(result, wrap_line=False, num_columns=None)
        if build_theta_debug:
            result_eval = result.evalf()
            pprint(result_eval, wrap_line=False, num_columns=None)
    else:
        result_eval = result.evalf()
        pprint(result_eval, wrap_line=False, num_columns=None)
        return
        

def show_robot_trans_standard(DHparams, angles = None):
    rows, _ = shape(DHparams)
    """for i in range(1, rows-1):
        pprint(DHparams.row(i))"""
    result = eye(4)
    for i in range(1, rows):
        # pprint(DH_params_LeArm.row(i))
        # i starts with 1 here
        print(f"A_{i} = ")
        
        alpha_im1, A_im1, _, _ = DHparams.row(i-1)
        _, _, d_i, theta_i = DHparams.row(i)
        # expected variable order: al_im1, a_im1, th_i, d_i
        final, _, _, _, _ = get_transformation_matrices_modified(alpha_im1, A_im1, theta_i, d_i)
        result = result.multiply(final)
        pprint(final)
        check_upper_left_det(result)
    if angles is None:
        print("Simplifying final matrix...", end="", flush=True)
        result = simplify(result)
        print("OK!")
        pprint(result, wrap_line=False, num_columns=None)
        if build_theta_debug:
            result_eval = result.evalf()
            pprint(result_eval, wrap_line=False, num_columns=None)
    else:
        result_eval = result.evalf()
        pprint(result_eval, wrap_line=False, num_columns=None)
        return
    




clear_screen()
print("0: Proof, using SymPy, ")
print("the general matrix of the paper is WRONG")
print("")
print("1: Proof, using SymPy, ")
print("the general matrix transformation")
print("(Given the 4 parameters)")
print("")
print("2: Evaluate, using SymPy, ")
print("the general matrix transformation of the robot")
print("(Given the 5 thetas)")
print("")
print("3: Evaluate, using SymPy, ")
print("a specific matrix transformation of the robot")
print("(Given the 5 thetas)")
print("")
choice = input("What would you like to do today? ")

if choice == "0":
    var("t1, t2, t3, t4, t5")
    test_matrix = Matrix([[cos(t5)*sin(t2+t3+t4)*cos(t1) - sin(t5)*sin(t1), -sin(t5)*cos(t2+t3+t4)*cos(t1) - cos(t5)*sin(t1), sin(t2+t3+t4)*cos(t1), 871],
                          [cos(t5)*cos(t2+t3+t4)*cos(t1) + sin(t5)*cos(t1), -sin(t5)*cos(t2+t3+t4)*sin(t1) + cos(t5)*cos(t1), sin(t2+t3+t4)*sin(t1), 871],
                          [-cos(t5)*sin(t2+t3+t4), sin(t5)*sin(t2+t3+t4), cos(t2+t3+t4), 871],
                          [871, 871, 871, 871]])
    
    print("The matrix in the paper is:")
    pprint(test_matrix, wrap_line=False, num_columns=None)
    print("(focused on the upper-left 3x3 matrix only, other values are 871 as a placeholder)")
    print("")
    check_upper_left_det(test_matrix)
    print("")
    print("Try with angle values:")
    t1, t2, t3, t4, t5 = 1, 2, 3, 4, 999
    print(t1, t2, t3, t4, t5)
    test_matrix = Matrix([[cos(t5)*sin(t2+t3+t4)*cos(t1) - sin(t5)*sin(t1), -sin(t5)*cos(t2+t3+t4)*cos(t1) - cos(t5)*sin(t1), sin(t2+t3+t4)*cos(t1), 871],
                          [cos(t5)*cos(t2+t3+t4)*cos(t1) + sin(t5)*cos(t1), -sin(t5)*cos(t2+t3+t4)*sin(t1) + cos(t5)*cos(t1), sin(t2+t3+t4)*sin(t1), 871],
                          [-cos(t5)*sin(t2+t3+t4), sin(t5)*sin(t2+t3+t4), cos(t2+t3+t4), 871],
                          [871, 871, 871, 871]])
    test_matrix = test_matrix.evalf()
    print("The matrix in the paper is:")
    pprint(test_matrix, wrap_line=False, num_columns=None)
    check_upper_left_det(test_matrix)
    print("")
    print("")
    print("")
    print("Matrix in the paper is inaccurate!")
    sys.exit()

print("")
print("1: Standard definition (Winnie)")
print("or")
print("2: Modified definition (LeArm)?")
print("Info: https://poe.com/s/076x3NsDgj8g53YynbmZ")
print("")
choice2 = input("Enter 1 / 2 / I: ")

if not choice == "1":
    print("1: Normal LeArm DH parameters (following general matrix in LeArm paper)")
    pprint(DH_params_LeArm[1:-1, :])
    print("")
    print("2: Buggy LeArm DH parameters")
    pprint(DH_params_LeArm_buggy[1:-1, :])
    print("")
    choice3 = input("Which set of DH parameters would you like to use?")

if choice == "1":
    if choice2 == "1":
        clear_screen()
        show_transformation_matrix_proof_standard()
    elif choice2 == "2":
        clear_screen()
        show_transformation_matrix_proof_modified()
    else:
        print("Opening info page...")
        import webbrowser
        webbrowser.open("https://poe.com/s/076x3NsDgj8g53YynbmZ")
elif choice == "2":
    if choice2 == "1":
        if choice3 == "1":
            clear_screen()
            print("Normal LeArm DH parameters (following general matrix in LeArm paper)")
            show_robot_trans_standard(DH_params_LeArm)
        elif choice3 == "2":
            clear_screen()
            print("Buggy LeArm DH parameters")
            show_robot_trans_standard(DH_params_LeArm_buggy)
    elif choice2 == "2":
        if choice3 == "1":
            clear_screen()
            print("Normal LeArm DH parameters (following general matrix in LeArm paper)")
            show_robot_trans_modified(DH_params_LeArm)
        elif choice3 == "2":
            clear_screen()
            print("Buggy LeArm DH parameters (following A1-A5 matrices in LeArm paper)")
            show_robot_trans_modified(DH_params_LeArm_buggy)
    else:
        print("Opening info page...")
        import webbrowser
        webbrowser.open("https://poe.com/s/076x3NsDgj8g53YynbmZ")

elif choice == "3":
    while True:
        print(f"Using {'DH_params_LeArm_buggy' if choice3 == '2' else 'DH_params_LeArm'} and {'show_robot_trans_standard' if choice2 == '1' else 'show_robot_trans_modified'}")
        
        arr = []
        arr.append(input("Enter theta 1 in radians: "))
        arr.append(input("Enter theta 2 in radians: "))
        arr.append(input("Enter theta 3 in radians: "))
        arr.append(input("Enter theta 4 in radians: "))
        arr.append(input("Enter theta 5 in radians: "))
        arr = [float(x) for x in arr]
        th1, th2, th3, th4, th5 = arr
        update_DH_params_using_th()
        
        callfunc = show_robot_trans_standard if choice2 == "1" else show_robot_trans_modified
        print(callfunc)
        pprint(DH_params_LeArm_buggy if choice3 == "2" else DH_params_LeArm)
        callfunc(DH_params_LeArm_buggy if choice3 == "2" else DH_params_LeArm, "HAVEANGLES")


print("Thank you!")
