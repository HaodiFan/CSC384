from bicycle import *

map = [['loc0', 'loc1', 'loc2', 'loc3', 'loc4', 'loc5', 'loc6'], [['loc0', 'loc1', 12], ['loc0', 'loc2', 37], ['loc0', 'loc3', 36], ['loc0', 'loc4', 54], ['loc0', 'loc5', 35], ['loc0', 'loc6', 8], ['loc1', 'loc2', 34], ['loc1', 'loc3', 33], ['loc1', 'loc4', 44], ['loc1', 'loc5', 30], ['loc1', 'loc6', 7], ['loc2', 'loc3', 3], ['loc2', 'loc4', 33], ['loc2', 'loc5', 6], ['loc2', 'loc6', 30], ['loc3', 'loc4', 36], ['loc3', 'loc5', 9], ['loc3', 'loc6', 29], ['loc4', 'loc5', 28], ['loc4', 'loc6', 46], ['loc5', 'loc6', 28]]]

jobs = [['Job0', 'loc1', 620, 'loc2', 2259, [[698, 39]]], ['Job1', 'loc5', 470, 'loc4', 776, [[511, 37], [625, 14]]], ['Job2', 'loc0', 764, 'loc5', 2182, [[827, 25], [940, 1]]], ['Job3', 'loc3', 810, 'loc0', 4577, [[943, 30], [969, 13], [1022, 2]]], ['Job4', 'loc5', 468, 'loc6', 3144, [[606, 44], [724, 35], [824, 13]]], ['Job5', 'loc1', 432, 'loc6', 1419, [[497, 28], [578, 17], [665, 1]]], ['Job6', 'loc5', 927, 'loc2', 337, [[978, 41]]], ['Job7', 'loc5', 987, 'loc6', 3305, [[1075, 36]]], ['Job8', 'loc3', 590, 'loc0', 2460, [[701, 33], [779, 10]]], ['Job9', 'loc1', 864, 'loc2', 2044, [[905, 30], [921, 10]]]]


def testNxtState(action, successors,testnum):
    print("\n========================================TEST {}==============================".format(testnum))
    print("Picking state that arises from \"{}\"".format(action))
    s1 = "ERROR \"{}\" not found in successor list".format(action)

    for s in successors:
        if s.action == action:
            s1 = s
    print("State found is")
    s1.print_state()
    print("max heuristic = ", heur_max_delivery_costs(s1), "sum heuristic = ", heur_sum_delivery_costs(s1))

    succ = s1.successors()
    print("\nThe \"{}\" state has".format(action), len(succ), "successors listed below (YOUR ORDER MIGHT DIFFER)")
    print("  NOTE THIS TESTING CODE WILL FAIL HERE IF YOU DID NOT PASS THE PREVIOUS TESTS\n")
    i = 1
    for s in succ:
        print("Successor state #{}:".format(i))
        s.print_state()
        print("max heuristic = ", heur_max_delivery_costs(s), "sum heuristic = ", heur_sum_delivery_costs(s))
        i = i +1
        print("====\n")
    return succ
    
if __name__ == '__main__':
    print("Jobs:")
    for j in jobs:
        print(j)
    print("Map")
    print("Locations:", map[0])
    print("Distances:")
    for (l1, l2, dist) in map[1]:
        print(l1, " <==> ", l2, " = ", dist, " mins.")
    print("Start State:")
    s0 = make_start_state(map,jobs)
    s0.print_state()
    succ = s0.successors()
    print("\n========================================TEST 1==============================")
    print("Start State has", len(succ), "successors. You should get same set of successors as below"
          " with same heuristic values")
    print(" BUT THE ORDER YOUR PROGRAM PRINTS THEM MIGHT DIFFER!")
    i = 1
    for s in succ:
        print("Successor state #{}:".format(i))
        s.print_state()
        print("max heuristic = ", heur_max_delivery_costs(s), "sum heuristic = ", heur_sum_delivery_costs(s))
        i = i +1
        
        print("====\n")
    
    i=1
    succ = testNxtState("first_pickup(Job2)", succ, i)
    i=i+1
    succ = testNxtState("pickup(Job9)", succ, i)
    i=i+1
    succ = testNxtState("pickup(Job8)", succ, i)
    i=i+1
    succ = testNxtState("pickup(Job5)", succ, i)
    i=i+1
    succ = testNxtState("deliver(Job2)", succ, i)
    i=i+1
    succ = testNxtState("pickup(Job7)", succ, i)
    i=i+1
    succ = testNxtState("deliver(Job8)", succ, i)
    i=i+1
    succ = testNxtState("deliver(Job9)", succ, i)
    i=i+1
    succ = testNxtState("deliver(Job5)", succ, i)
    i=i+1
    succ = testNxtState("deliver(Job7)", succ, i)
    i=i+1
    succ = testNxtState("pickup(Job0)", succ, i)
    i=i+1
    succ = testNxtState("pickup(Job1)", succ, i)
    i=i+1
    succ = testNxtState("pickup(Job3)", succ, i)
    i=i+1
    succ = testNxtState("deliver(Job0)", succ, i)

    
