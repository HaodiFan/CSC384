# all_tests.py
# Test suite for A3 Q1 Bayes nets.
# Written for CSC 384 Winter 2015
# author: Gregory Koch (t3kochgr)

import os.path
import time
import signal
import sys
import csv
from bnetbase import *

class TO_exc(Exception):
    pass

def toHandler(signum, frame):
    raise TO_exc()

def setTO(TOsec):
    signal.signal(signal.SIGALRM, toHandler)
    signal.alarm(TOsec)


# We aren't using Python's unit test framework and we have floating point
# calculations. So it is necessary to define our own check.
def approx_equal(a, b, tol=1e-3):
     return abs(a-b) < tol

# We aren't using Python's unit test framework and we have floating point
# calculations. So it is necessary to define our own check.
def list_approx_equal(a, b, tol=1e-3):
     for i in range(len(a)):
        if abs(a[i]-b[i]) >= tol:
            return False
     return True

# Test the example Bayes net cases included with the assignment.
# 6 subtests.
def test_example_bn(scores, max_score):
    test_scores = []
    pass_subtests = []

    # Set up Bayes net
    E = Variable('E', ['e', '-e'])
    B = Variable('B', ['b', '-b'])
    S = Variable('S', ['s', '-s'])
    G = Variable('G', ['g', '-g'])
    W = Variable('W', ['w', '-w'])
    FE = Factor('P(E)', [E])
    FB = Factor('P(B)', [B])
    FS = Factor('P(S|E,B)', [S, E, B])
    FG = Factor('P(G|S)', [G,S])
    FW = Factor('P(W|S)', [W,S])

    FE.add_values([['e',0.1], ['-e', 0.9]])
    FB.add_values([['b', 0.1], ['-b', 0.9]])
    FS.add_values([['s', 'e', 'b', .9], ['s', 'e', '-b', .2], ['s', '-e', 'b', .8],['s', '-e', '-b', 0],
                   ['-s', 'e', 'b', .1], ['-s', 'e', '-b', .8], ['-s', '-e', 'b', .2],['-s', '-e', '-b', 1]])
    FG.add_values([['g', 's', 0.5], ['g', '-s', 0], ['-g', 's', 0.5], ['-g', '-s', 1]])
    FW.add_values([['w', 's', 0.8], ['w', '-s', .2], ['-w', 's', 0.2], ['-w', '-s', 0.8]])

    Q3 = BN('SampleQ4', [E,B,S,G,W], [FE,FB,FS,FG,FW])

    # Subtest 1
    pass_subtests.append(1)
    try:
        G.set_evidence('g')
        probs = VE(Q3, S, [G])
        pass_subtests[len(pass_subtests)-1] *= approx_equal(probs[0], 1.0)
        pass_subtests[len(pass_subtests)-1] *= approx_equal(probs[1], 0.0)
    except:
        pass_subtests[len(pass_subtests)-1] *= 0.0

    # Subtest 2
    pass_subtests.append(1)
    try:
        B.set_evidence('b')
        E.set_evidence('-e')
        probs = VE(Q3, W, [B, E])
        pass_subtests[len(pass_subtests)-1] *= approx_equal(probs[0], 0.68)
        pass_subtests[len(pass_subtests)-1] *= approx_equal(probs[1], 0.32)
    except:
        pass_subtests[len(pass_subtests)-1] *= 0.0

    # Subtest 3
    pass_subtests.append(1)
    try:
        S.set_evidence('s')
        probs1 = VE(Q3, G, [S])
        S.set_evidence('-s')
        probs2 = VE(Q3, G, [S])
        pass_subtests[len(pass_subtests)-1] *= approx_equal(probs1[0], 0.5)
        pass_subtests[len(pass_subtests)-1] *= approx_equal(probs1[1], 0.5)
        pass_subtests[len(pass_subtests)-1] *= approx_equal(probs2[0], 0.0)
        pass_subtests[len(pass_subtests)-1] *= approx_equal(probs2[1], 1.0)
    except:
        pass_subtests[len(pass_subtests)-1] *= 0.0

    # Subtest 4
    pass_subtests.append(1)
    try:
        S.set_evidence('s')
        W.set_evidence('w')
        probs1 = VE(Q3, G, [S,W])
        S.set_evidence('s')
        W.set_evidence('-w')
        probs2 = VE(Q3, G, [S,W])
        S.set_evidence('-s')
        W.set_evidence('w')
        probs3 = VE(Q3, G, [S,W])
        S.set_evidence('-s')
        W.set_evidence('-w')
        probs4 = VE(Q3, G, [S,W])
        pass_subtests[len(pass_subtests)-1] *= approx_equal(probs1[0], 0.5)
        pass_subtests[len(pass_subtests)-1] *= approx_equal(probs1[1], 0.5)
        pass_subtests[len(pass_subtests)-1] *= approx_equal(probs2[0], 0.5)
        pass_subtests[len(pass_subtests)-1] *= approx_equal(probs2[1], 0.5)
        pass_subtests[len(pass_subtests)-1] *= approx_equal(probs3[0], 0.0)
        pass_subtests[len(pass_subtests)-1] *= approx_equal(probs3[1], 1.0)
        pass_subtests[len(pass_subtests)-1] *= approx_equal(probs4[0], 0.0)
        pass_subtests[len(pass_subtests)-1] *= approx_equal(probs4[1], 1.0)
    except:
        pass_subtests[len(pass_subtests)-1] *= 0.0

    # Subtest 5
    pass_subtests.append(1)
    try:
        W.set_evidence('w')
        probs1 = VE(Q3, G, [W])
        W.set_evidence('-w')
        probs2 = VE(Q3, G, [W])
        pass_subtests[len(pass_subtests)-1] *= approx_equal(probs1[0], 0.15265998457979954)
        pass_subtests[len(pass_subtests)-1] *= approx_equal(probs1[1], 0.8473400154202004)
        pass_subtests[len(pass_subtests)-1] *= approx_equal(probs2[0], 0.01336753983256819)
        pass_subtests[len(pass_subtests)-1] *= approx_equal(probs2[1], 0.9866324601674318)
    except:
        pass_subtests[len(pass_subtests)-1] *= 0.0

    # Subtest 6
    pass_subtests.append(1)
    try:
        probs1 = VE(Q3, G, [])
        probs2 = VE(Q3, E, [])
        pass_subtests[len(pass_subtests)-1] *= approx_equal(probs1[0], 0.04950000000000001)
        pass_subtests[len(pass_subtests)-1] *= approx_equal(probs1[1], 0.9505)
        pass_subtests[len(pass_subtests)-1] *= approx_equal(probs2[0], 0.1)
        pass_subtests[len(pass_subtests)-1] *= approx_equal(probs2[1], 0.9)
    except:
        pass_subtests[len(pass_subtests)-1] *= 0.0

    for i in range(len(pass_subtests)):
        subscore = (pass_subtests[i] * max_score/len(pass_subtests))
        test_scores.append(subscore)

    scores.append(test_scores)
    return scores

# Test for the Bayes net corresponding to the written questions in part (a).
# Original version which should be weighted a low amount of points to avoid
# over-penalizing students who did not account for names/types.
# 4 subtests.
def test_assignment_three_original(scores, max_score):
    test_scores = []
    pass_subtests = []

    # Set up Bayes net
    a = Variable('A', [0,1])
    b = Variable('B', [0,1])
    c = Variable('C', [0,1])
    d = Variable('D', [0,1])
    e = Variable('E', [0,1])
    f = Variable('F', [0,1])
    g = Variable('F', [0,1])
    h = Variable('H', [0,1])
    i = Variable('I', [0,1])

    F1 = Factor("P(A)", [a])
    F2 = Factor("P(B|A,H)", [b,a,h])
    F3 = Factor("P(C|B,G)", [c,b,g])
    F4 = Factor("P(D|C,F)", [d,c,f])
    F5 = Factor("P(E|C)", [e,c])
    F6 = Factor("P(F)", [f])
    F7 = Factor("P(G)", [g])
    F8 = Factor("P(H)", [h])
    F9 = Factor("P(I|B)", [i,b])

    F1.add_values([
        [0, 0.1],
        [1, 0.9]])
    F2.add_values([
        [0, 0, 0, 0.4],
        [1, 0, 0, 0.6],
        [0, 0, 1, 0.5],
        [1, 0, 1, 0.5],
        [0, 1, 0, 1],
        [1, 1, 0, 0],

        [0, 1, 1, 0],
        [1, 1, 1, 1]])
    F3.add_values([
        [0, 0, 0, 0],
        [1, 0, 0, 1],

        [0, 0, 1, 0.9],
        [1, 0, 1, 0.1],
        [0, 1, 0, 0.1],
        [1, 1, 0, 0.9],

        [0, 1, 1, 0.1],
        [1, 1, 1, 0.9]])
    F4.add_values([
        [0, 0, 0, 0.8],

        [1, 0, 0, 0.2],
        [0, 0, 1, 0.3],
        [1, 0, 1, 0.7],
        [0, 1, 0, 0],
        [1, 1, 0, 1],

        [0, 1, 1, 1],
        [1, 1, 1, 0]])
    F5.add_values([
        [0,0,0.6],

        [1,0,0.4],
        [0,1,0.8],
        [1,1,0.2]])
    F6.add_values([

        [0, 0.9],
        [1,0.1]])
    F7.add_values([
        [0, 0],
        [1,1]])

    F8.add_values([
        [0, 0.5],
        [1, 0.5]])
    F9.add_values([

        [0, 0, 0.1],
        [1, 0, 0.9],
        [0, 1, 0.7],
        [1, 1, 0.3]])

    sn = BN('simple', [a,b,c,d,e,f,g,h,i], [F1,F2,F3,F4,F5,F6,F7,F8,F9])

    # Subtest 1
    pass_subtests.append(1)
    try:
        a.set_evidence(1)
        probs=VE(sn, b, [a])
        pass_subtests[len(pass_subtests)-1] *= approx_equal(probs[1], 0.50)
    except:
        pass_subtests[len(pass_subtests)-1] *= 0.0

    # Subtest 2
    pass_subtests.append(1)
    try:
        a.set_evidence(1)
        probs=VE(sn, c, [a])
        pass_subtests[len(pass_subtests)-1] *= approx_equal(probs[1], 0.50)
    except:
        pass_subtests[len(pass_subtests)-1] *= 0.0

    # Subtest 3
    pass_subtests.append(1)
    try:
        a.set_evidence(1)
        e.set_evidence(0)
        probs=VE(sn, c, [a,e])
        pass_subtests[len(pass_subtests)-1] *= approx_equal(probs[1], 0.57, tol=1e-2)
    except:
        pass_subtests[len(pass_subtests)-1] *= 0.0

    # Subtest 4
    pass_subtests.append(1)
    try:
        a.set_evidence(1)
        f.set_evidence(0)
        probs=VE(sn, c, [a,f])
        pass_subtests[len(pass_subtests)-1] *= approx_equal(probs[1], 0.50)
    except:
        pass_subtests[len(pass_subtests)-1] *= 0.0

    for i in range(len(pass_subtests)):
        subscore = (pass_subtests[i] * max_score/len(pass_subtests))
        test_scores.append(subscore)

    scores.append(test_scores)
    return scores

# Test for the Bayes net corresponding to the written questions in part (a).
# Revised version to avoid integer bugs with factor/variable names.
# 4 subtests.
def test_assignment_three_revised(scores, max_score):
    test_scores = []
    pass_subtests = []

    a = Variable('A', ['0','1'])
    b = Variable('B', ['0','1'])
    c = Variable('C', ['0','1'])
    d = Variable('D', ['0','1'])
    e = Variable('E', ['0','1'])
    f = Variable('F', ['0','1'])
    g = Variable('F', ['0','1'])
    h = Variable('H', ['0','1'])
    i = Variable('I', ['0','1'])

    F1 = Factor("P(A)", [a])
    F2 = Factor("P(B|A,H)", [b,a,h])
    F3 = Factor("P(C|B,G)", [c,b,g])
    F4 = Factor("P(D|C,F)", [d,c,f])
    F5 = Factor("P(E|C)", [e,c])
    F6 = Factor("P(F)", [f])
    F7 = Factor("P(G)", [g])
    F8 = Factor("P(H)", [h])
    F9 = Factor("P(I|B)", [i,b])

    F1.add_values([
        ['0', 0.1],
        ['1', 0.9]])
    F2.add_values([
        ['0', '0', '0', 0.4],
        ['1', '0', '0', 0.6],
        ['0', '0', '1', 0.5],
        ['1', '0', '1', 0.5],
        ['0', '1', '0', 1.0],
        ['1', '1', '0', 0.0],
        ['0', '1', '1', 0.0],
        ['1', '1', '1', 1.0]])
    F3.add_values([
        ['0', '0', '0', 0.0],
        ['1', '0', '0', 1.0],
        ['0', '0', '1', 0.9],
        ['1', '0', '1', 0.1],
        ['0', '1', '0', 0.1],
        ['1', '1', '0', 0.9],
        ['0', '1', '1', 0.1],
        ['1', '1', '1', 0.9]])
    F4.add_values([
        ['0', '0', '0', 0.8],
        ['1', '0', '0', 0.2],
        ['0', '0', '1', 0.3],
        ['1', '0', '1', 0.7],
        ['0', '1', '0', 0.0],
        ['1', '1', '0', 1.0],
        ['0', '1', '1', 1.0],
        ['1', '1', '1', 0.0]])
    F5.add_values([
        ['0','0',0.6],
        ['1','0',0.4],
        ['0','1',0.8],
        ['1','1',0.2]])
    F6.add_values([
        ['0', 0.9],
        ['1',0.1]])
    F7.add_values([
        ['0', 0.0],
        ['1',1.0]])
    F8.add_values([
        ['0', 0.5],
        ['1', 0.5]])
    F9.add_values([
        ['0', '0', 0.1],
        ['1', '0', 0.9],
        ['0', '1', 0.7],
        ['1', '1', 0.3]])

    sn = BN('simple', [a,b,c,d,e,f,g,h,i], [F1,F2,F3,F4,F5,F6,F7,F8,F9])

    # Subtest 1
    pass_subtests.append(1)
    try:
        a.set_evidence('1')
        probs=VE(sn, b, [a])
        pass_subtests[len(pass_subtests)-1] *= approx_equal(probs[1], 0.5)
    except:
        pass_subtests[len(pass_subtests)-1] *= 0.0

    # Subtest 2
    pass_subtests.append(1)
    try:
        a.set_evidence('1')
        probs=VE(sn, c, [a])
        pass_subtests[len(pass_subtests)-1] *= approx_equal(probs[1], 0.5)
    except:
        pass_subtests[len(pass_subtests)-1] *= 0.0

    # Subtest 3
    pass_subtests.append(1)
    try:
        a.set_evidence('1')
        e.set_evidence('0')
        probs=VE(sn, c, [a,e])
        pass_subtests[len(pass_subtests)-1] *= approx_equal(probs[1], 0.57, tol=1e-2)
    except:
        pass_subtests[len(pass_subtests)-1] *= 0.0

    # Subtest 4
    pass_subtests.append(1)
    try:
        a.set_evidence('1')
        f.set_evidence('0')
        probs=VE(sn, c, [a,f])
        pass_subtests[len(pass_subtests)-1] *= approx_equal(probs[1], 0.5)
    except:
        pass_subtests[len(pass_subtests)-1] *= 0.0

    for i in range(len(pass_subtests)):
        subscore = (pass_subtests[i] * max_score/len(pass_subtests))
        test_scores.append(subscore)

    scores.append(test_scores)
    return scores

# Test the multiply factors function that students were required to implement.
# 5 subtests.
def test_multiply_factors(scores, max_score):
    test_scores = []
    pass_subtests = []

    E = Variable('E', ['e', '-e'])
    B = Variable('B', ['b', '-b'])
    S = Variable('S', ['s', '-s'])
    G = Variable('G', ['g', '-g'])
    W = Variable('W', ['w', '-w'])
    FE = Factor('P(E)', [E])
    FB = Factor('P(B)', [B])
    FS = Factor('P(S|E,B)', [S, E, B])
    FS2 = Factor('P(S|E)', [S, E])
    FG = Factor('P(G|S)', [G,S])
    FW = Factor('P(W|S)', [W,S])

    FE.add_values([['e',0.1], ['-e', 0.9]])
    FB.add_values([['b', 0.1], ['-b', 0.9]])
    FS.add_values([['s', 'e', 'b', .9], ['s', 'e', '-b', .2], ['s', '-e', 'b', .8],['s', '-e', '-b', 0],
                   ['-s', 'e', 'b', .1], ['-s', 'e', '-b', .8], ['-s', '-e', 'b', .2],['-s', '-e', '-b', 1]])
    FS2.add_values([['s', 'e', 0.6], ['s', '-e', 0.3], ['-s', 'e', 0.4],['-s', '-e', 0.7]])
    FG.add_values([['g', 's', 0.5], ['g', '-s', 0], ['-g', 's', 0.5], ['-g', '-s', 1]])
    FW.add_values([['w', 's', 0.8], ['w', '-s', .2], ['-w', 's', 0.2], ['-w', '-s', 0.8]])

    Q3 = BN('SampleQ4', [E,B,S,G,W], [FE,FB,FS,FS2,FG,FW])

    # Subtest 1 - Multiply variables in factor, factors share no variables
    pass_subtests.append(1)
    print("mul1")
    try:
        setTO(5)
        new_factor = multiply_factors([FE,FB])
        pass_subtests[len(pass_subtests)-1] *= (new_factor.scope == [E, B])
        pass_subtests[len(pass_subtests)-1] *= list_approx_equal(new_factor.values,[0.010000000000000002, 0.09000000000000001, 0.09000000000000001, 0.81])
    except:
        pass_subtests[len(pass_subtests)-1] *= 0.0

    setTO(0)

    # Subtest 2 - Multiply variables in factor, factors share 1 variable
    print("mul2")
    pass_subtests.append(1)
    try:
        setTO(5)
        new_factor = multiply_factors([FG,FW])
        pass_subtests[len(pass_subtests)-1] *= (new_factor.scope == [G, S, W])
        pass_subtests[len(pass_subtests)-1] *= list_approx_equal(new_factor.values,[0.4, 0.1, 0.0, 0.0, 0.4, 0.1, 0.2, 0.8])
    except:
        pass_subtests[len(pass_subtests)-1] *= 0.0

    setTO(0)

    # Subtest 3 - Multiply variables in factor, factors share >1 variables, factors agree in scope order
    print("mul3")
    pass_subtests.append(1)
    try:
        new_factor = multiply_factors([FS,FS2])
        pass_subtests[len(pass_subtests)-1] *= (new_factor.scope == [S, E, B])
        pass_subtests[len(pass_subtests)-1] *= list_approx_equal(new_factor.values,[0.54, 0.12, 0.24, 0.0, 0.04000000000000001, 0.32000000000000006, 0.13999999999999999, 0.7]
)
    except:
        pass_subtests[len(pass_subtests)-1] *= 0.0

    # Subtest 4 - Multiply variables in factor, factors disagree in scope order
    print("mul4")
    pass_subtests.append(1)
    try:
        new_factor = multiply_factors([FB,FS])
        pass_subtests[len(pass_subtests)-1] *= (new_factor.scope == [B, S, E])
        pass_subtests[len(pass_subtests)-1] *= list_approx_equal(new_factor.values,[0.09000000000000001, 0.08000000000000002, 0.010000000000000002, 0.020000000000000004, 0.18000000000000002, 0.0, 0.7200000000000001, 0.9])
    except:
        pass_subtests[len(pass_subtests)-1] *= 0.0

    for i in range(len(pass_subtests)):
        subscore = (pass_subtests[i] * max_score/len(pass_subtests))
        test_scores.append(subscore)

    scores.append(test_scores)
    return scores

# Test the restrict factor function that students were required to implement.
# 5 subtests.
def test_restrict_factor(scores, max_score):
    test_scores = []
    pass_subtests = []

    E = Variable('E', ['e', '-e'])
    B = Variable('B', ['b', '-b'])
    S = Variable('S', ['s', '-s'])
    G = Variable('G', ['g', '-g'])
    W = Variable('W', ['w', '-w'])
    FE = Factor('P(E)', [E])
    FB = Factor('P(B)', [B])
    FS = Factor('P(S|E,B)', [S, E, B])
    FS2 = Factor('P(S|E)', [S, E])
    FG = Factor('P(G|S)', [G,S])
    FW = Factor('P(W|S)', [W,S])

    FE.add_values([['e',0.1], ['-e', 0.9]])
    FB.add_values([['b', 0.1], ['-b', 0.9]])
    FS.add_values([['s', 'e', 'b', .9], ['s', 'e', '-b', .2], ['s', '-e', 'b', .8],['s', '-e', '-b', 0],
                   ['-s', 'e', 'b', .1], ['-s', 'e', '-b', .8], ['-s', '-e', 'b', .2],['-s', '-e', '-b', 1]])
    FS2.add_values([['s', 'e', 0.6], ['s', '-e', 0.3], ['-s', 'e', 0.4],['-s', '-e', 0.7]])
    FG.add_values([['g', 's', 0.5], ['g', '-s', 0], ['-g', 's', 0.5], ['-g', '-s', 1]])
    FW.add_values([['w', 's', 0.8], ['w', '-s', .2], ['-w', 's', 0.2], ['-w', '-s', 0.8]])

    Q3 = BN('SampleQ4', [E,B,S,G,W], [FE,FB,FS,FS2,FG,FW])

    # Subtest 1 - Restrict variable in factor to a value, variable restricted in factor
    pass_subtests.append(1)
    try:
        new_factor = restrict_factor(FS, E, '-e')
        pass_subtests[len(pass_subtests)-1] *= (new_factor.scope == [S, B])
        pass_subtests[len(pass_subtests)-1] *= list_approx_equal(new_factor.values,[0.8, 0, 0.2, 1])
    except:
        pass_subtests[len(pass_subtests)-1] *= 0.0

    # Subtest 2 - Restrict variable in factor to a value, variable restricted not in factor
    pass_subtests.append(1)
    try:
        new_factor = restrict_factor(FS, W, 'w')
        pass_subtests[len(pass_subtests)-1] *= (new_factor.scope == [S, E, B])
        pass_subtests[len(pass_subtests)-1] *= list_approx_equal(new_factor.values,[0.9, 0.2, 0.8, 0, 0.1, 0.8, 0.2, 1])
    except:
        pass_subtests[len(pass_subtests)-1] *= 0.0

    # Subtest 3 - Restrict variable in factor to a value, variable restricted in factor is a variable over which the CPD is defined
    pass_subtests.append(1)
    try:
        new_factor = restrict_factor(FG, G, '-g')
        pass_subtests[len(pass_subtests)-1] *= (new_factor.scope == [S])
        pass_subtests[len(pass_subtests)-1] *= list_approx_equal(new_factor.values,[0.5, 1])
    except:
        pass_subtests[len(pass_subtests)-1] *= 0.0

    # Subtest 4 - Restrict variable in factor to a value, variable restricted in factor is a conditioned variable in the factor's CPD table
    pass_subtests.append(1)
    try:
        new_factor = restrict_factor(FG, S, '-s')
        pass_subtests[len(pass_subtests)-1] *= (new_factor.scope == [G])
        pass_subtests[len(pass_subtests)-1] *= list_approx_equal(new_factor.values,[0, 1])
    except:
        pass_subtests[len(pass_subtests)-1] *= 0.0

    for i in range(len(pass_subtests)):
        subscore = (pass_subtests[i] * max_score/len(pass_subtests))
        test_scores.append(subscore)

    scores.append(test_scores)
    return scores

# Test the sum out variable function that students were required to implement.
# 5 subtests.
def test_sum_out_variable(scores, max_score):
    test_scores = []
    pass_subtests = []

    E = Variable('E', ['e', '-e'])
    B = Variable('B', ['b', '-b'])
    S = Variable('S', ['s', '-s'])
    G = Variable('G', ['g', '-g'])
    W = Variable('W', ['w', '-w'])
    FE = Factor('P(E)', [E])
    FB = Factor('P(B)', [B])
    FS = Factor('P(S|E,B)', [S, E, B])
    FS2 = Factor('P(S|E)', [S, E])
    FG = Factor('P(G|S)', [G,S])
    FW = Factor('P(W|S)', [W,S])

    FE.add_values([['e',0.1], ['-e', 0.9]])
    FB.add_values([['b', 0.1], ['-b', 0.9]])
    FS.add_values([['s', 'e', 'b', .9], ['s', 'e', '-b', .2], ['s', '-e', 'b', .8],['s', '-e', '-b', 0],
                   ['-s', 'e', 'b', .1], ['-s', 'e', '-b', .8], ['-s', '-e', 'b', .2],['-s', '-e', '-b', 1]])
    FS2.add_values([['s', 'e', 0.6], ['s', '-e', 0.3], ['-s', 'e', 0.4],['-s', '-e', 0.7]])
    FG.add_values([['g', 's', 0.5], ['g', '-s', 0], ['-g', 's', 0.5], ['-g', '-s', 1]])
    FW.add_values([['w', 's', 0.8], ['w', '-s', .2], ['-w', 's', 0.2], ['-w', '-s', 0.8]])

    Q3 = BN('SampleQ4', [E,B,S,G,W], [FE,FB,FS,FS2,FG,FW])

    # Subtest 1 - Marginalize a variable in factor, variable summed over is in the factor
    pass_subtests.append(1)
    try:
        new_factor =  sum_out_variable(FS, E)
        pass_subtests[len(pass_subtests)-1] *= (new_factor.scope == [S, B])
        pass_subtests[len(pass_subtests)-1] *= list_approx_equal(new_factor.values,[1.7000000000000002, 0.2, 0.30000000000000004, 1.8])
    except:
        pass_subtests[len(pass_subtests)-1] *= 0.0

    # Subtest 2 - Marginalize a variable in factor, variable summed over is not in the factor (producing constant multiple of the factor)
    pass_subtests.append(1)
    try:
        new_factor = sum_out_variable(FS, W)
        pass_subtests[len(pass_subtests)-1] *= (new_factor.scope == [S, E, B])
        pass_subtests[len(pass_subtests)-1] *= list_approx_equal(new_factor.values,[1.8, 0.4, 1.6, 0, 0.2, 1.6, 0.4, 2])
    except:
        pass_subtests[len(pass_subtests)-1] *= 0.0

    # Subtest 3 - Marginalize a variable in factor, variable summed over produces a constant factor
    pass_subtests.append(1)
    try:
        new_factor = sum_out_variable(FG, G)
        pass_subtests[len(pass_subtests)-1] *= (new_factor.scope == [S])
        pass_subtests[len(pass_subtests)-1] *= list_approx_equal(new_factor.values,[1.0, 1])
    except:
        pass_subtests[len(pass_subtests)-1] *= 0.0

    # Subtest 4 - Marginalize a variable in factor, factor with single variable is summed over that variable
    pass_subtests.append(1)
    try:
        new_factor = sum_out_variable(FE, E)
        pass_subtests[len(pass_subtests)-1] *= (new_factor.scope == [])
        pass_subtests[len(pass_subtests)-1] *= list_approx_equal(new_factor.values,[1.0])
    except:
        pass_subtests[len(pass_subtests)-1] *= 0.0

    for i in range(len(pass_subtests)):
        subscore = (pass_subtests[i] * max_score/len(pass_subtests))
        test_scores.append(subscore)

    scores.append(test_scores)
    return scores

# Extra Bayes net test.
# Here we work with the "Asia" network from example_bn.py.
# 5 subtests.
def test_ve_extra_one(scores, max_score):
    test_scores = []
    pass_subtests = []

    VisitAsia = Variable('Visit_To_Asia', ['visit', 'no-visit'])
    F1 = Factor("F1", [VisitAsia])
    F1.add_values([['visit', 0.01], ['no-visit', 0.99]])

    Smoking = Variable('Smoking', ['smoker', 'non-smoker'])
    F2 = Factor("F2", [Smoking])
    F2.add_values([['smoker', 0.5], ['non-smoker', 0.5]])

    Tuberculosis = Variable('Tuberculosis', ['present', 'absent'])
    F3 = Factor("F3", [Tuberculosis, VisitAsia])
    F3.add_values([['present', 'visit', 0.05],
                   ['present', 'no-visit', 0.01],
                   ['absent', 'visit', 0.95],
                   ['absent', 'no-visit', 0.99]])

    Cancer = Variable('Lung Cancer', ['present', 'absent'])
    F4 = Factor("F4", [Cancer, Smoking])
    F4.add_values([['present', 'smoker', 0.10],
                   ['present', 'non-smoker', 0.01],
                   ['absent', 'smoker', 0.90],
                   ['absent', 'non-smoker', 0.99]])

    Bronchitis = Variable('Bronchitis', ['present', 'absent'])
    F5 = Factor("F5", [Bronchitis, Smoking])
    F5.add_values([['present', 'smoker', 0.60],
                   ['present', 'non-smoker', 0.30],
                   ['absent', 'smoker', 0.40],
                   ['absent', 'non-smoker', 0.70]])

    TBorCA = Variable('Tuberculosis or Lung Cancer', ['true', 'false'])
    F6 = Factor("F6", [TBorCA, Tuberculosis, Cancer])
    F6.add_values([['true', 'present', 'present', 1.0],
                   ['true', 'present', 'absent', 1.0],
                   ['true', 'absent', 'present', 1.0],
                   ['true', 'absent', 'absent', 0],
                   ['false', 'present', 'present', 0],
                   ['false', 'present', 'absent', 0],
                   ['false', 'absent', 'present', 0],
                   ['false', 'absent', 'absent', 1]])

    Dyspnea = Variable('Dyspnea', ['present', 'absent'])
    F7 = Factor("F7", [Dyspnea, TBorCA, Bronchitis])
    F7.add_values([['present', 'true', 'present', 0.9],
                   ['present', 'true', 'absent', 0.7],
                   ['present', 'false', 'present', 0.8],
                   ['present', 'false', 'absent', 0.1],
                   ['absent', 'true', 'present', 0.1],
                   ['absent', 'true', 'absent', 0.3],
                   ['absent', 'false', 'present', 0.2],
                   ['absent', 'false', 'absent', 0.9]])

    Xray = Variable('XRay Result', ['abnormal', 'normal'])
    F8 = Factor("F8", [Xray, TBorCA])
    F8.add_values([['abnormal', 'true', 0.98],
                   ['abnormal', 'false', 0.05],
                   ['normal', 'true', 0.02],
                   ['normal', 'false', 0.95]])

    Asia = BN("Asia", [VisitAsia, Smoking, Tuberculosis, Cancer,
                       Bronchitis, TBorCA, Dyspnea, Xray],
                       [F1, F2, F3, F4, F5, F6, F7, F8])

    # Subtest 1
    pass_subtests.append(1)
    try:
        Xray.set_evidence('normal')
        probs1 = VE(Asia, Smoking, [Xray])
        Xray.set_evidence('abnormal')
        probs2 = VE(Asia, Smoking, [Xray])
        pass_subtests[len(pass_subtests)-1] *= approx_equal(probs1[0], 0.47672569609089244)
        pass_subtests[len(pass_subtests)-1] *= approx_equal(probs2[0], 0.6877538533851288)
    except:
        pass_subtests[len(pass_subtests)-1] *= 0.0

    # Subtest 2
    pass_subtests.append(1)
    try:
        Bronchitis.set_evidence('present')
        TBorCA.set_evidence('false')
        probs = VE(Asia, VisitAsia, [Bronchitis, TBorCA])
        pass_subtests[len(pass_subtests)-1] *= approx_equal(probs[1], 0.9904001616814875)
    except:
        pass_subtests[len(pass_subtests)-1] *= 0.0

    # Subtest 3
    pass_subtests.append(1)
    try:
        Smoking.set_evidence('smoker')
        probs1 = VE(Asia, Cancer, [Smoking])
        Smoking.set_evidence('non-smoker')
        probs2 = VE(Asia, Cancer, [Smoking])
        pass_subtests[len(pass_subtests)-1] *= approx_equal(probs1[0], 0.1)
        pass_subtests[len(pass_subtests)-1] *= approx_equal(probs1[1], 0.9)
        pass_subtests[len(pass_subtests)-1] *= approx_equal(probs2[0], 0.01)
        pass_subtests[len(pass_subtests)-1] *= approx_equal(probs2[1], 0.99)
    except:
        pass_subtests[len(pass_subtests)-1] *= 0.0

    # Subtest 4
    pass_subtests.append(1)
    try:
        Smoking.set_evidence('smoker')
        Xray.set_evidence('normal')
        probs1 = VE(Asia, Cancer, [Smoking, Xray])
        Smoking.set_evidence('smoker')
        Xray.set_evidence('abnormal')
        probs2 = VE(Asia, Cancer, [Smoking, Xray])
        Smoking.set_evidence('non-smoker')
        Xray.set_evidence('normal')
        probs3 = VE(Asia, Cancer, [Smoking, Xray])
        Smoking.set_evidence('non-smoker')
        Xray.set_evidence('abnormal')
        probs4 = VE(Asia, Cancer, [Smoking, Xray])
        pass_subtests[len(pass_subtests)-1] *= approx_equal(probs1[1], 0.9976423301699692)
        pass_subtests[len(pass_subtests)-1] *= approx_equal(probs2[1], 0.3540085745474105)
        pass_subtests[len(pass_subtests)-1] *= approx_equal(probs3[1], 0.9997852060033375)
        pass_subtests[len(pass_subtests)-1] *= approx_equal(probs4[1], 0.8577138270799044)
    except:
        pass_subtests[len(pass_subtests)-1] *= 0.0

    # Subtest 5
    pass_subtests.append(1)
    try:
        Xray.set_evidence('normal')
        probs1 = VE(Asia, Cancer, [Xray])
        Xray.set_evidence('abnormal')
        probs2 = VE(Asia, Cancer, [Xray])
        pass_subtests[len(pass_subtests)-1] *= approx_equal(probs1[0], 0.001236357969961357)
        pass_subtests[len(pass_subtests)-1] *= approx_equal(probs1[1], 0.9987636420300386)
        pass_subtests[len(pass_subtests)-1] *= approx_equal(probs2[0], 0.4887114013196477)
        pass_subtests[len(pass_subtests)-1] *= approx_equal(probs2[1], 0.5112885986803523)
    except:
        pass_subtests[len(pass_subtests)-1] *= 0.0

    # Subtest 6
    pass_subtests.append(1)
    try:
        Xray.set_evidence('normal')
        Dyspnea.set_evidence('present')
        VisitAsia.set_evidence('visit')
        probs1 = VE(Asia, Smoking, [Xray,Dyspnea,VisitAsia])
        Xray.set_evidence('normal')
        Dyspnea.set_evidence('absent')
        VisitAsia.set_evidence('visit')
        probs2 = VE(Asia, Smoking, [Xray,Dyspnea,VisitAsia])
        Xray.set_evidence('abnormal')
        Dyspnea.set_evidence('present')
        VisitAsia.set_evidence('no-visit')
        probs3 = VE(Asia, Smoking, [Xray,Dyspnea,VisitAsia])
        pass_subtests[len(pass_subtests)-1] *= approx_equal(probs1[0], 0.6045119217499575)
        pass_subtests[len(pass_subtests)-1] *= approx_equal(probs2[0], 0.387616837357692)
        pass_subtests[len(pass_subtests)-1] *= approx_equal(probs3[0], 0.7867957903686024)
    except:
        pass_subtests[len(pass_subtests)-1] *= 0.0

    # Subtest 7
    pass_subtests.append(1)
    try:
        probs1 = VE(Asia, Cancer, [])
        probs2 = VE(Asia, Smoking, [])
        pass_subtests[len(pass_subtests)-1] *= approx_equal(probs1[0], 0.05500000000000001)
        pass_subtests[len(pass_subtests)-1] *= approx_equal(probs1[1], 0.945)
        pass_subtests[len(pass_subtests)-1] *= approx_equal(probs2[0], 0.5)
        pass_subtests[len(pass_subtests)-1] *= approx_equal(probs2[1], 0.49999999999999994)
    except:
        pass_subtests[len(pass_subtests)-1] *= 0.0

    for i in range(len(pass_subtests)):
        subscore = (pass_subtests[i] * max_score/len(pass_subtests))
        test_scores.append(subscore)

    scores.append(test_scores)

    return scores

# Run test suite and output scores
if __name__ == '__main__':
    test_strs = ['example_bn.py base test cases:',
                  'A3 Q1 original test cases:', 'A3 Q1 revised test cases:',
                  'multiply_factors test cases:',
                  'restrict_factor test cases:',
                  'sum_out_variable test cases:',
                  've_extra_one test cases:',
                ]
    max_scores = [18.0,2.0,16.0,6.0,6.0,6.0,14.0]
    scores = []
    test_scores = []

    # Split the input path to get the student ID
    arg_split = sys.argv[1].split('/')
    student_id = arg_split[len(arg_split)-1]

    # Run each test, accumulating the results in the scores array.
    # The first dimension of the scores array indexes the test number.
    # The second dimension accumulates all sub scores for each test.
    scores = test_example_bn(scores, max_scores[0])
    print("test1")
    scores = test_assignment_three_original(scores, max_scores[1])
    print("test2")
    scores = test_assignment_three_revised(scores, max_scores[2])
    print("test3")
    scores = test_multiply_factors(scores, max_scores[3])
    print("test4")
    scores = test_restrict_factor(scores, max_scores[4])
    print("test5")
    scores = test_sum_out_variable(scores, max_scores[5])
    print("test6")
    scores = test_ve_extra_one(scores, max_scores[6])

    # First accumulate the total scores for each test
    for i in range(len(scores)):
        test_score = 0.0
        for j in range(len(scores[i])):
            test_score += scores[i][j]
        test_scores.append(test_score)

    # Extract written answer score and comments for this student from csv file
    csv_splits = []
    f = open('a3marks-written.csv', 'rU')
    reader = csv.reader(f, dialect=csv.excel_tab)
    for row in reader:
        row_str = row[0]
        if row_str.startswith(student_id):
             csv_splits = row_str.split(",")

    csv_scores = [csv_splits[0],(float(csv_splits[1])*8.0/4.0),csv_splits[2],(float(csv_splits[3])*24.0/4.0),(float(csv_splits[4])*24.0/4.0),(float(csv_splits[5])*24.0/4.0),(float(csv_splits[6])*24.0/4.0),csv_splits[7]]

    q1_score = sum(test_scores)+csv_scores[1]
    q2_score = csv_scores[3]+csv_scores[4]+csv_scores[5]+csv_scores[6]
    total_score = q1_score+q2_score

    sys.stdout = open('summary.txt', 'w')

    # Now print out the full summary and combine all information
    print('====================================================')
    print(student_id)
    print('CSC 384 - Assignment 3 Summary')
    print('Total score: ' + str(total_score) + '/100.0')
    print('====================================================\n')
    print("Q1")
    print("Score: " + str(q1_score) + "/" + str(sum(max_scores)+8.0))
    print('====================================================')
    for i in range(len(scores)):
        print(test_strs[i], ' ' + str(test_scores[i]) + '/' + str(max_scores[i]))
        for j in range(len(scores[i])):
            print('\tsubtest ' + str(j+1) + ' of ' + str(len(scores[i])) + ': ' + str(scores[i][j]) + '/' + str(max_scores[i]/len(scores[i])))

    print('\nWritten answers:')
    print("\tparts (a)-(d): " + str(csv_scores[1]) + '/8.0')
    print("\tcomments: " + csv_scores[2])
    print("\nQ2")
    print("Score: " + str(q2_score) + "/24.0")
    print('====================================================')
    print("\tpart (a): " + str(csv_scores[3]) + '/6.0')
    print("\tpart (b): " + str(csv_scores[4]) + '/6.0')
    print("\tpart (c): " + str(csv_scores[5]) + '/6.0')
    print("\tpart (d): " + str(csv_scores[6]) + '/6.0')
    print("\tcomments: " + csv_scores[7])

    # Insert final score into master csv, creating a new csv if it doesn't exist
    final_csv_data = []
    if os.path.isfile('a3marks-final.csv'):
        f2 = open('a3marks-final.csv', 'r', newline='')
        reader2 = csv.reader(f2, delimiter=',')
        for line in reader2:
            final_csv_data.append(line)

    final_csv_data.append([student_id, total_score])
    f2 = open('a3marks-final.csv', 'w', newline='')
    writer2 = csv.writer(f2, delimiter=',')
    writer2.writerows(final_csv_data)
