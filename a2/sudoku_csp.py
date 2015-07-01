from cspbase import *
from itertools import combinations, product, permutations
import copy

def enforce_gac(constraint_list):
    '''Input a list of constraint objects, each representing a constraint, then 
       enforce GAC on them pruning values from the variables in the scope of
       these constraints. Return False if a DWO is detected. Otherwise, return True. 
       The pruned values will be removed from the variable object's cur_domain.
       enforce_gac modifies the variable objects that are in the scope of
       the constraints passed to it.'''
    # print("enforce_gac start!")
    gacq = list(constraint_list) # shallow copy
    while gacq:
        c = gacq.pop(0) # pop from front of queue
        for v in c.scope:
            for d in v.cur_domain():
                other_var = [vv for vv in c.scope if v != vv]
                if not c.has_support(v, d):
                    v.prune_value(d)
                    if v.cur_domain_size() == 0:
                        constraint_list = []
                        return False # for DWO
                    else:
                        # reset gacq
                        # gacq = list(constraint_list)
                        # add relevant c to gacq
                        for cc in constraint_list:
                            if cc not in gacq and v in cc.scope:
                                gacq.append(cc)
    return True

			    
def sudoku_enforce_gac_model_1(initial_sudoku_board):
    '''The input board is specified as a list of 9 lists. Each of the
       9 lists represents a row of the board. If a 0 is in the list it
       represents an empty cell. Otherwise if a number between 1--9 is
       in the list then this represents a pre-set board
       position. E.g., the board
    
       -------------------  
       | | |2| |9| | |6| |
       | |4| | | |1| | |8|
       | |7| |4|2| | | |3|
       |5| | | | | |3| | |
       | | |1| |6| |5| | |
       | | |3| | | | | |6|
       |1| | | |5|7| |4| |
       |6| | |9| | | |2| |
       | |2| | |8| |1| | |
       -------------------
       would be represented by the list of lists
       
       [[0,0,2,0,9,0,0,6,0],
       [0,4,0,0,0,1,0,0,8],
       [0,7,0,4,2,0,0,0,3],
       [5,0,0,0,0,0,3,0,0],
       [0,0,1,0,6,0,5,0,0],
       [0,0,3,0,0,0,0,0,6],
       [1,0,0,0,5,7,0,4,0],
       [6,0,0,9,0,0,0,2,0],
       [0,2,0,0,8,0,1,0,0]]
       
       
       In model_1 you should create a variable for each cell of the
       board, with domain equal to {1-9} if the board has a 0 at that
       position, and domain equal {i} if the board has a fixed number i
       at that cell. 
       
       Model_1 should create BINARY CONSTRAINTS OF NOT-EQUAL between all
       relevant variables (e.g., all pairs of variables in the same
       row, etc.), then invoke enforce_gac on those constraints. All of the
       constraints of Model_1 MUST BE binary constraints (i.e.,
       constraints whose scope includes two and only two variables).

       After creating all variables and constraints you can invoke
       your enforce_gac routine to obtain the GAC reduced current domains
       of the variables.
       
       The ouput should have the same layout as the input: a list of
       nine lists each representing a row of the board. However, now the
       numbers in the positions of the input list are to be replaced by
       LISTS which are the corresponding cell's pruned domain (current
       domain) AFTER gac has been performed.
       
       For example, if GAC failed to prune any values the output from
       the above input would result in an output would be: NOTE I HAVE
       PADDED OUT ALL OF THE LISTS WITH BLANKS SO THAT THEY LINE UP IN
       TO COLUMNS. Python would not output this list of lists in this
       format.
       
       
       [[[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[		  2],[1,2,3,4,5,6,7,8,9],[		  9],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[		      6],[1,2,3,4,5,6,7,8,9]],
       [[1,2,3,4,5,6,7,8,9],[		     4],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[		     1],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[		 8]],
       [[1,2,3,4,5,6,7,8,9],[		     7],[1,2,3,4,5,6,7,8,9],[		     4],[		 2],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[		 3]],
       [[		 5],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[		 3],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9]],
       [[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[		 1],[1,2,3,4,5,6,7,8,9],[		 6],[1,2,3,4,5,6,7,8,9],[		 5],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9]],
       [[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[		 3],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[		 6]],
       [[		 1],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[		 5],[		     7],[1,2,3,4,5,6,7,8,9],[		     4],[1,2,3,4,5,6,7,8,9]],
       [[		 6],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[		     9],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[		     2],[1,2,3,4,5,6,7,8,9]],
       [[1,2,3,4,5,6,7,8,9],[		     2],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[		 8],[1,2,3,4,5,6,7,8,9],[		 1],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9]]]
       
       Of course, GAC would prune some variable domains SO THIS WOULD
       NOT BE the outputted list.
       
    '''

    # domain_map: just to make conversion easier
    domain_map = { k: [k] for k in range(1, 10) }
    domain_map[0] = list(range(1, 10))

    # nested list of domains just as above comment
    vars_dom = [[domain_map[initial_sudoku_board[i][j]]
                 for j in range(9)] for i in range(9)]
    
    # create actual Variable objects out of vars_dom
    idx2name = lambda i, j: "V{0}{1}".format(i+1, j+1)
    variables = [[Variable(idx2name(i, j), vars_dom[i][j])
                  for j in range(9)] for i in range(9)]

    # gather three kinds of constraints
    row_constraints = [create_bi_constraint(r, j1, r, j2, variables)
                       for r in range(9)
                       for j1 in range(9) for j2 in range(9)
                       if j1 < j2]
    col_constraints = [create_bi_constraint(i1, c, i2, c, variables)
                       for c in range(9)
                       for i1 in range(9) for i2 in range(9)
                       if i1 < i2]
    sub_base = [(i, j) for i in range(3) for j in range(3)]
    add_offset = lambda dx, dy: lambda tup: (tup[0] + dx, tup[1] + dy)
    subs = [list(map(add_offset(dx, dy), sub_base))
            for dx in range(0, 9, 3) for dy in range(0, 9, 3)]
    sub_constraints = [create_bi_constraint(t1[0], t1[1], t2[0], t2[1], variables)
                       for idx in range(9)
                       for t1, t2 in combinations(subs[idx], 2)]

    # aggregate to full constraint list
    constraints = row_constraints + col_constraints + sub_constraints

    # directly apply enforce_gac
    if enforce_gac(constraints):
        return [[variables[i][j].cur_domain()
                 for j in range(9)] for i in range(9)]
    else:
        return [[[] for j in range(9)] for i in range(9)]


##############################

def sudoku_enforce_gac_model_2(initial_sudoku_board):
    '''This function takes the same input format (a list of 9 lists
    specifying the board, and generates the same format output as
    sudoku_enforce_gac_model_1.
    
    The variables of model_2 are the same as for model_1: a variable
    for each cell of the board, with domain equal to {1-9} if the
    board has a 0 at that position, and domain equal {i} if the board
    has a fixed number i at that cell.

    However, model_2 has different constraints. In particular, instead
    of binary non-equals constaints model_2 has 27 all-different
    constraints: all-different constraints for the variables in each
    of the 9 rows, 9 columns, and 9 sub-squares. Each of these
    constraints is over 9-variables (some of these variables will have
    a single value in their domain). model_2 should create these
    all-different constraints between the relevant variables, then
    invoke enforce_gac on those constraints.
    '''

    # domain_map: just to make conversion easier
    domain_map = { k: [k] for k in range(1, 10) }
    domain_map[0] = list(range(1, 10))

    # nested list of domains just as above comment
    vars_dom = [[domain_map[initial_sudoku_board[i][j]]
                 for j in range(9)] for i in range(9)]
    
    # create actual Variable objects out of vars_dom
    idx2name = lambda i, j: "V{0}{1}".format(i+1, j+1)
    variables = [[Variable(idx2name(i, j), vars_dom[i][j])
                  for j in range(9)] for i in range(9)]

    # gather three kinds of constraints
    row_index = lambda r: [(r, i) for i in range(9)]
    row_constraints = [create_nine_constraint(row_index(r), variables)
                       for r in range(9)]

    col_index = lambda c: [(i, c) for i in range(9)]
    col_constraints = [create_nine_constraint(col_index(c), variables)
                       for c in range(9)]
    
    sub_base = [(i, j) for i in range(3) for j in range(3)]
    add_offset = lambda dx, dy: lambda tup: (tup[0] + dx, tup[1] + dy)
    subs = [list(map(add_offset(dx, dy), sub_base))
            for dx in range(0, 9, 3) for dy in range(0, 9, 3)]
    sub_constraints = [create_nine_constraint(sub, variables)
                       for sub in subs]

    # aggregate to full constraint list
    constraints = row_constraints + col_constraints + sub_constraints

    # focus on one var, prune some values of other var domain
    # for i in range(9):
    #     for j in range(9):
    #         cc = [c for c in constraints
    #               if c.name.find(variables[i][j].name[-2:]) != -1]
    #         enforce_gac(cc)

    # directly apply enforce_gac
    if enforce_gac(constraints):
        return [[variables[i][j].cur_domain()
                 for j in range(9)] for i in range(9)]
    else:
        return [[[] for j in range(9)] for i in range(9)]


##############################
# My Helpers
##############################

def create_bi_constraint(i1, j1, i2, j2, variables):
    v1, v2 = variables[i1][j1], variables[i2][j2]
    name = "C({0},{1})".format(v1.name[-2:], v2.name[-2:])
    scope = [v1, v2]
    c = Constraint(name, scope)
    sat_tups = [(val1, val2) 
                for val1 in v1.domain() for val2 in v2.domain()
                if val1 != val2]
    c.add_satisfying_tuples(sat_tups)
    return c

def create_nine_constraint(index_tup_list, variables):
    varmap = lambda i, j: variables[i][j]
    var_list = [varmap(i, j) for i, j in index_tup_list]
    name = "C({0})".format(",".join(v.name[-2:] for v in var_list))
    scope = var_list

    # possible optimization: 
    # mannually prune some known not possible values
    values_prune = [v.cur_domain()[0] for v in var_list
                    if v.cur_domain_size() == 1]
    for val in values_prune:
        for v in var_list:
            # when val is the only cur domain of v
            # x != val constraint actually comes from v
            if val in v.cur_domain() and v.cur_domain_size() != 1:
                v.prune_value(val)

    c = Constraint(name, scope)
    vars_dom = [v.cur_domain() for v in var_list]

    # generate sat_tups from filtering all permutation
    is_valid_perm = lambda perm: valid_perm(perm, vars_dom)

    # deal with large cur_domain specially
    if not values_prune: # all full domain
        sat_tups = list(permutations(range(1, 10)))
    elif len(values_prune) == 1: # more efficient to filter from permutation
        sat_tups = list(filter(is_valid_perm, permutations(range(1, 10))))
    else: # more efficient to filter from cartesian product
        sat_tups = list(filter(lambda t: len(set(t)) == 9,
                               product(*vars_dom)))

    c.add_satisfying_tuples(sat_tups)
    return c

def valid_perm(perm, vars_dom):
    for i in range(9):
        if perm[i] not in vars_dom[i]:
            return False
    return True

