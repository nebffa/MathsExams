import random
from maths.symbols import *
from maths import all_functions
import copy

import pprint


discretes = (int, sympy.Rational)


def cubic(spec):
    '''
    An algorithm to be able to request cubics by such things as "x-intercepts > -1".

    The algorithm works by generating 4 pieces of information, and then to solve for the cubic's constants via matrices.

    I don't know if this algorithm is air-tight, and if it isn't, I don't know if it can be made air-tight. 

    It's not all bad though, this seems to be an infinitely better way to request cubics than what I had before. It will probably 
    just need some fixing/tweaking over time.

    '''


    # need 4 pieces of information to determine a cubic
    # point at (x, y) coord = 1 piece
    # turning point at (x, y) = 2 pieces
    # stationary point of inflexion at (x, y) = 3 pieces


    # the best algorithm I can come up with is:
    #   1. determine the pieces of definite information, e.g. x-intercept at 1 (**NOT** x-intercepts > 1)
    #   2. determine how much information we still need
    #   3. check the inequalities that have been specified (e.g. x-intercepts > 1)
    #   4. based on inequalities, randomly generate extra pieces of information until the cubic is fully specified

    X_RANGE = [i for i in range(-6, 7)]
    Y_RANGE = [i for i in range(-6, 7)]

    k0, k1, k2, k3 = sympy.symbols('k0:4')
    y = k0*x**3 + k1*x**2 + k2*x + k3
    y_diff = y.diff(x)
    y_diffdiff = y_diff.diff(x)
    information = []  # holds tuples - linear combinations of a, b, c and d corresponding to the values those linear combinations take

    # 'clear' pieces of information
    num_tps_specified_master = 0
    num_spis_specified_master = 0
    num_points_specified_master = 0
    y_int_specified_master = False

    x_ints_location = [i for i in X_RANGE]
    tps_location = [i for i in X_RANGE]

    # helper functions
    def add_x_y(x_coord, y_coord):
        nonlocal num_points_specified_master

        information.append( (y.subs({x: x_coord}), y_coord) )
        num_points_specified_master += 1
    def add_tp(x_coord, y_coord):
        nonlocal num_points_specified_master
        nonlocal num_tps_specified_master

        information.append( (y_diff.subs({x: x_coord}), 0) )
        information.append( (y.subs({x: x_coord}), y_coord) )
        num_points_specified_master += 1
        num_tps_specified_master += 1
    def add_spi(x_coord, y_coord):
        nonlocal num_points_specified_master
        nonlocal num_tps_specified_master
        nonlocal num_spis_specified_master

        information.append( (y_diff_diff.subs({x: x_coord}), 0) )
        information.append( (y_diff.subs({x: x_coord}), 0) )
        information.append( (y.subs({x: x_coord}), y_coord) )
        num_points_specified_master += 1
        num_tps_specified_master += 1
        num_spis_specified_master += 1


    if isinstance(spec['x_intercepts']['locations'], tuple):
        for x_intercept in spec['x_intercepts']['locations']:
            add_x_y(x_intercept, 0)
            num_points_specified_master += 1
    elif isinstance(spec['x_intercepts']['locations'], sympy.Interval):
        x_ints_location = [i for i in X_RANGE if i in spec['x_intercepts']['locations']]

    if isinstance(spec['turning_points']['locations'], tuple):
        for turning_point in spec['turning_points']['locations']:
            if isinstance(turning_point, tuple):  # is an (x, y) coordinate
                add_tp(*turning_point)
            #elif isinstance(turning_point, discretes):  # is an x coordinate only
            #    information.append( (y_diff.subs({x: turning_point}), 0) )
            num_tps_specified_master += 1
    elif isinstance(spec['turning_points']['locations'], sympy.Interval):
        tps_location = [i for i in X_RANGE if i in spec['turning_points']['locations']]

    if isinstance(spec['inflexion_points']['locations'], tuple):
        for inflexion_point in spec['inflexion_points']['locations']:
            if isinstance(inflexion_point, tuple):  # is an (x, y) coordinate
                information.append( (y_diff_diff.subs({x: inflexion_point[0]}), 0) )
                information.append( (y.subs({x: inflexion_point[0]}), inflexion_point[1]) )
            elif isinstance(inflexion_point, discretes):  # is an x coordinate only
                information.append( (y_diff.subs({x: inflexion_point}), 0) )
            num_spis_specified_master += 1

    if isinstance(spec['y_intercept'], discretes):
        information.append( (y.subs({x: 0}), spec['y_intercept']) )
        y_int_specified_master = True


    information_master = copy.copy(information)
    while True:
        num_points_specified = num_points_specified_master
        num_tps_specified = num_tps_specified_master
        num_spis_specified = num_spis_specified_master
        y_int_specified = y_int_specified_master
        information = copy.copy(information_master)

        # we should probably only be able to specify the number of one quantity as they impact eachother
        # e.g. 3 x-intercepts causes 2 turning points, 2 turning points causes one point of inflexion
        if spec['x_intercepts']['n'] is not None:
            if spec['x_intercepts']['n'] == 1:
                if random.randint(0, 1):  # generate a SPI
                    add_spi(random.choice(X_RANGE), random.choice(Y_RANGE))
                else:  # or 2 turning points both above or both below the x-axis
                    x_locs = random.sample(tps_location, 2)
                    y_locs = random.sample([i for i in Y_RANGE if i > 0], 2)
                    if random.randint(0, 1):
                        add_tp(x_locs[0], y_locs[0])
                        add_tp(x_locs[1], y_locs[1])
                    else:
                        add_tp(x_locs[0], -y_locs[0])
                        add_tp(x_locs[1], -y_locs[1])

            elif spec['x_intercepts']['n'] == 2:  # generate a TP on the x-axis
                if isinstance(spec['x_intercepts']['locations'], tuple):
                    add_tp(random.choice(['x_intercepts']), 0)  # take an existing x-intercept and make it a TP
                else:
                    add_x_y(random.choice(x_ints_location))
            elif spec['x_intercepts']['n'] == 3:  # generate 2 TPs, one above the x-axis, one below
                if spec['turning_points']['locations'] is not None:  # we already have one TP, generate the other
                    x_loc = random.choice([i for i in tps_location if i != spec['turning_points']['locations'][0] ])
                    y_loc = random.choice([i for i in Y_RANGE if i != spec['turning_points']['locations'][1] ])
                    add_tp(x_loc, y_loc)
                #elif isinstance(spec['turning_points']['locations'], discretes):
                #    x_loc = random.choice([i for i in tps_location if i != spec['turning_points']['locations'] ])
                #    y_locs = random.sample(Y_RANGE, 2)
                #    add_tp(x_loc[0])
                else:
                    x_locs = random.sample(tps_location, 2)
                    y_locs = random.sample([i for i in Y_RANGE if i > 0])
                    add_tp(x_locs[0], -y_locs[0])  # a TP below the x-axis
                    add_tp(x_locs[1], y_locs[1])  # a TP above the x-axis


        elif spec['turning_points']['n'] is not None:
            if spec['turning_points']['n'] == 0:  # a special case, we can return early
                quadratic = all_functions.request_quadratic(difficulty=random.randint(4, 5)).equation  # a quadratic with discriminant < 0
                if len(information) == 0:
                    return quadratic.integrate() + random.randint(-3, 3)  # make it a cubic and give it a meaningful y-intercept
                else:  # we already have an x-intercept or y-intercept, add 3 points of information to the 
                            #matrix and let the solver compute the constant of integration
                    equation = quadratic.integrate()
                    information.append((1, 0, 0, 0), equation.coeff(x**3))
                    information.append((0, 1, 0, 0), equation.coeff(x**2))
                    information.append((0, 0, 1, 0), equation.coeff(x))
                
            elif spec['turning_points']['n'] == 1:
                if spec['turning_points']['locations'] is not None:  # there must be a turning point specified - make it an SPI
                    information.append( (y_diff_diff.subs({x: spec['turning_points']['locations'][0] }), 0) )
                else:  # otherwise just make a new SPI
                    x_loc = random.choice(tps_location)
                    y_loc = random.choice(Y_RANGE)
                    add_spi(x_loc, y_loc)
            elif spec['turning_points']['n'] == 2:  
                if isinstance(spec['turning_points']['locations'], tuple):  # there must be a turning point already specified
                    if len(information) <= 2:
                        x_loc = random.choice([i for i in tps_location if i != spec['turning_points']['locations'][0] ])
                        y_loc = random.choice([i for i in Y_RANGE if i != spec['turning_points']['locations'][1] ])
                        add_tp(x_loc, y_loc)
                else:  # no TPs were specified - make 2 TPs
                    x_locs = random.sample(tps_location, 2)
                    y_locs = random.sample(tps_location, 2)
                    add_tp(x_locs[0], y_locs[0])
                    if len(information) <= 2:
                        add_tp(x_locs[1], y_locs[1])



        # 'not clear' pieces of information
        information_needed = 4 - len(information)
        while information_needed != 0:  # add new TPs or intercepts
            if information_needed == 4:  # add two TPs
                x_locs = random.sample(tps_location, 2)
                y_locs = random.sample(tps_location, 2)
                add_tp(x_locs[0], y_locs[0])
                add_tp(x_locs[1], y_locs[1])
            elif information_needed >= 2:  # add one TP only
                if spec['turning_points']['locations'] is not None:  # there must be a turning point already specified
                    x_loc = random.choice([i for i in tps_location if i != spec['turning_points']['locations'][0] ])
                    y_loc = random.choice([i for i in Y_RANGE if i != spec['turning_points']['locations'][1] ])
                    add_tp(x_loc, y_loc)
                else:  # no TPs were specified
                    x_loc = random.choice(tps_location)
                    y_loc = random.choice(tps_location)
                    add_tp(x_locs[0], y_locs[0])
            else:  # add an intercept
                if not y_int_specified:
                    y_loc = random.choice(Y_RANGE)
                    add_x_y(0, y_loc)
                else:
                    x_loc = random.choice(x_ints_location)
                    add_x_y(x_loc, 0)

            information_needed = 4 - len(information)

        # at this point we have 4 pieces of information - time to solve the matrix equation!            
        # the matrix looks like:
        #   [(k0 + 5*k2 + 3*k3, 0), (2*k0 + 3*k1, 1), ...]
        square_matrix = sympy.Matrix([[i[0].coeff(k0), i[0].coeff(k1), i[0].coeff(k2), i[0].coeff(k3)] for i in information])
        column_matrix = sympy.Matrix([i[1] for i in information])

        inverse = square_matrix.inv()

        constants = inverse * column_matrix

        if spec['direction'] == -1 and constants[0] > 0 or spec['direction'] == 1 and constants[0] < 0:
            continue

        equation = y.subs( dict(zip([k0, k1, k2, k3], constants)) )
        if isinstance(spec['x_intercepts']['locations'], sympy.Interval):
            #print([i for i in sympy.solve(equation)])
            real_solutions = [sympy.simplify(sympy.radsimp(i)) for i in sympy.solve(equation) if sympy.ask(sympy.Q.real(i)) ]
            if len(real_solutions) == 0:
                continue
            #pprint.pprint(real_solutions)
            #print('here are your real solutions sire: {0}'.format(real_solutions))
            for solution in real_solutions:
                #print(solution, solution.evalf())
                #print(spec['x_intercepts']['locations'])
                try:
                    solution.evalf() not in spec['x_intercepts']['locations']
                except:
                    continue


        diff_equation = equation.diff(x)
        if isinstance(spec['turning_points']['locations'], sympy.Interval):
            real_solutions = [sympy.simplify(sympy.radsimp(i)) for i in sympy.solve(diff_equation) if sympy.ask(sympy.Q.real(i)) ]
            print(real_solutions)
            for solution in real_solutions:
                if solution.evalf() not in spec['turning_points']['locations']:
                    continue


        return y.subs( dict(zip([k0, k1, k2, k3], constants)) )


def absolute_value(spec):
    # y = a * |x - b| + c
    a = range(-3, 4)
    b = range(-3, 4)
    c = range(-5, 6)

    # key['gradient']  a = k or a > k or a < k
    if isinstance(spec['gradient'], discretes):
        a = list(spec['gradient'])
    elif isinstance(spec['gradient'], sympy.Interval):
        a = [i for i in a if i in spec['gradient']]

    # key['direction']    a > 0 or a < 0
    if isinstance(spec['direction'], sympy.Interval):
        a = [i for i in a if i in spec['direction']]

    # key['inflexion_point']
    if isinstance(spec['turning_point']['location'], tuple):
        b = list( spec['turning_point']['location'][0] )
        c = list( spec['turning_point']['location'][1] )
    elif isinstance(spec['turning_point']['location'], sympy.Interval):
        b = [i for i in b if i in spec['turning_point']['location'] ]

    master_a, master_b, master_c = a, b, c
    while True:
        a, b, c = copy.copy(master_a), copy.copy(master_b), copy.copy(master_c)

        a, b, c = list(a), list(b), list(c)  # ensure we are dealing with lists, not iterables
        a, b, c = (random.choice(i) for i in (a, b, c))
        equation = a * sympy.Abs(x - b) + c

        solutions = sympy.solve(equation)

        for solution in solutions:
            if solution not in spec['x_intercepts']:
                continue

        if isinstance(spec['direction'], sympy.Interval):
            if a not in spec['direction']:
                continue

        return equation


def hyperbola(spec):
    