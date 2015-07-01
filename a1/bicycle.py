#Look for #IMPLEMENT tags in this file. These tags indicate what has
#to be implemented to complete the bicycle domain.  

'''
bicycle STATESPACE 
'''
#   You may add only standard python imports---i.e., ones that are automatically
#   available on CDF.
#   You may not remove any imports.
#   You may not import or otherwise source any of your own files

from search import *
from random import randint
from math import sqrt
from copy import deepcopy


class bicycle(StateSpace):
    def __init__(self, action, gval, state, parent):
#IMPLEMENT
        '''Initialize a bicycle search state object.'''
        if action == 'START':   #NOTE action = 'START' is treated as starting the search space
            StateSpace.n = 0
        StateSpace.__init__(self, action, gval, parent)
        #implement the rest of this function.
        self.state = state

    def successors(self): 
#IMPLEMENT
        '''Return list of bicycle objects that are the successors of the current object'''
        states = list()
        # TODO
        
        current_jobs = self.state["current_jobs"]
        future_jobs = self.state["future_jobs"]
        map_list = bicycle.map_list

        # start from home, only option: first_pickup(jobname)
        if self.action == "START":
            for job in future_jobs:
                job_name, job_load = job[0], job[4]
                pickup_loc, dropoff_loc = job[1], job[3]

                # can't pick up if can't carry the load
                MAX_LOAD = 10000
                if job_load > MAX_LOAD:
                    continue

                # earliest arriving time at pickup
                pickup_time = job[2]

                # do not generate successor if impossible to pickup before 1140
                if pickup_time > 1140:
                    continue
                
                new_state = deepcopy(self.state)
                new_state["loc"] = pickup_loc
                new_state["time"] = pickup_time
                new_state["load"] = job_load
                new_state["current_jobs"].append(job)
                new_state["future_jobs"].remove(job)

                states.append(
                    bicycle(
                        "first_pickup({})".format(job_name),
                        self.gval,
                        new_state,
                        self
                    )
                )
            
        else:

            loc = self.get_loc()
            time = self.get_time()

            # deliver(jobname)
            for job in current_jobs:
                job_name, dropoff_loc, job_load = job[0], job[3], job[4]

                # earliest arriving time at dropoff
                dropoff_time = time + dist(loc, dropoff_loc, map_list)

                # do not generate successor if impossible to finish before 1140
                if dropoff_time > 1140:
                    continue

                # find earning according to pricing
                earning = find_earn_current(time, loc, job)

                new_state = deepcopy(self.state)
                new_state["loc"] = dropoff_loc
                new_state["time"] = dropoff_time
                new_state["load"] -= job_load
                new_state["earned"] += earning
                new_state["current_jobs"].remove(job)
                new_cost = job[5][0][1] - earning

                states.append(
                    bicycle(
                        "deliver({})".format(job_name),
                        self.gval + new_cost,
                        new_state,
                        self
                    )
                )

            # pickup(jobname) under some condition
            for job in future_jobs:
                job_name, job_load = job[0], job[4]
                pickup_loc, dropoff_loc = job[1], job[3]

                # can't pick up if it's some dropoff loc of carried job
                if pickup_loc in [j[3] for j in current_jobs]:
                    continue

                # can't pick up if can't carry the load
                MAX_LOAD = 10000
                if self.get_load() + job_load > MAX_LOAD:
                    continue

                # earliest arriving time at pickup
                pickup_time = max(job[2], time + dist(loc, pickup_loc, map_list))

                # do not generate successor if impossible to pickup before 1140
                if pickup_time > 1140:
                    continue

                new_state = deepcopy(self.state)
                new_state["loc"] = pickup_loc
                new_state["time"] = pickup_time
                new_state["load"] += job_load
                new_state["current_jobs"].append(job)
                new_state["future_jobs"].remove(job)

                states.append(
                    bicycle(
                        "pickup({})".format(job_name),
                        self.gval,
                        new_state,
                        self
                    )
                )

        return states

    def hashable_state(self) :
#IMPLEMENT
        '''Return a data item that can be used as a dictionary key to UNIQUELY represent the state.'''
        # TODO
        sort_key = lambda l: l[0]
        attr_tup = (
            self.get_loc(), self.get_load(), self.get_time(), self.get_earned(),
            tuple(map(str, sorted(self.get_carrying(), key=sort_key))),
            tuple(map(str, sorted(self.get_unstarted(), key=sort_key)))
        )
        return attr_tup
        
    def print_state(self):
        #DO NOT CHANGE THIS FUNCTION---it will be used in auto marking
        #and in generating sample trace output. 
        #Note that if you implement the "get" routines below properly, 
        #This function should work irrespective of how you represent
        #your state. 

        if self.parent:
            print("Action= \"{}\", S{}, g-value = {}, (From S{})".format(self.action, self.index, self.gval, self.parent.index))
        else:
            print("Action= \"{}\", S{}, g-value = {}, (Initial State)".format(self.action, self.index, self.gval))
            
        print("    Carrying: {} (load {} grams)".format(
                      self.get_carrying(), self.get_load()))
        print("    State time = {} loc = {} earned so far = {}".format(
                      self.get_time(), self.get_loc(), self.get_earned()))
        print("    Unstarted Jobs.{}".format(self.get_unstarted()))

    def get_loc(self):
#IMPLEMENT
        '''Return location of courier in this state'''
        return self.state["loc"]
        
    def get_carrying(self):
#IMPLEMENT
        '''Return list of NAMES of jobs being carried in this state'''
        return [j[0] for j in self.state["current_jobs"]]

    def get_load(self):
#IMPLEMENT
        '''Return total weight being carried in this state'''
        return self.state["load"]

    def get_time(self):
#IMPLEMENT
        '''Return current time in this state'''
        return self.state["time"]

    def get_earned(self):
#IMPLEMENT
        '''Return amount earned so far in this state'''
        return self.state["earned"]

    def get_unstarted(self):
#IMPLEMENT
        '''Return list of NAMES of jobs not yet stated in this state''' 
        return [j[0] for j in self.state["future_jobs"]]

    def get_carrying_list(self):
        '''Return list of jobs being carried in this state'''
        return self.state["current_jobs"]

    def get_unstarted_list(self):
        '''Return list of jobs not yet started in this state'''
        return self.state["future_jobs"]


def find_earn_current(now, loc, job):
    '''Find the earning of a current job if start moving to dropoff now'''
    map_list = bicycle.map_list
    dropoff_time = now + dist(loc, job[3], map_list)
    for lst in job[5]:
        if lst[0] >= dropoff_time:
            return lst[1]
    return 0 # too late that earns no money

def find_earn_future(now, loc, job):
    '''Find the earning of a future job if start moving to pickup now'''
    map_list = bicycle.map_list
    pickup_time = max(now + dist(loc, job[1], map_list), job[2])
    dropoff_time = pickup_time + dist(job[1], job[3], map_list)
    for lst in job[5]:
        if lst[0] >= dropoff_time:
            return lst[1]
    return 0 # too late that earns no money
    
def heur_null(state):
    '''Null Heuristic use to make A* search perform uniform cost search'''
    return 0

def heur_sum_delivery_costs(state):
#IMPLEMENT
    '''Bicycle Heuristic sum of delivery costs.'''
    #Sum over every job J being carried: Lost revenue if we
    #immediately travel to J's dropoff point and deliver J.
    #Plus 
    #Sum over every unstarted job J: Lost revenue if we immediately travel to J's pickup point then to J's dropoff poing and then deliver J.
    # TODO
    now = state.get_time()
    loc = state.get_loc()
    future_jobs = state.get_unstarted_list()
    current_jobs = state.get_carrying_list()
    loss_current = [job[5][0][1] - find_earn_current(now, loc, job)
                    for job in current_jobs]
    s1 = sum(loss_current) if loss_current else 0
    loss_future = [job[5][0][1] - find_earn_future(now, loc, job)
                   for job in future_jobs]
    s2 = sum(loss_future) if loss_future else 0
    return s1 + s2

def heur_max_delivery_costs(state):
#IMPLEMENT
    '''Bicycle Heuristic max of delivery costs.'''
    #m1 = Max over every job J being carried: Lost revenue if we immediately travel to J's dropoff point and deliver J.
    #m2 = Max over every unstarted job J: Lost revenue if we immediately travel to J's pickup point then to J's dropoff point and then deliver J.
    #heur_max_delivery_costs(state) = max(m1, m2)
    # TODO
    now = state.get_time()
    loc = state.get_loc()
    future_jobs = state.get_unstarted_list()
    current_jobs = state.get_carrying_list()
    loss_current = [job[5][0][1] - find_earn_current(now, loc, job)
                    for job in current_jobs]
    m1 = max(loss_current) if loss_current else 0
    loss_future = [job[5][0][1] - find_earn_future(now, loc, job)
                   for job in future_jobs]
    m2 = max(loss_future) if loss_future else 0
    return max(m1, m2)

def bicycle_goal_fn(state):
#IMPLEMENT
    '''Have we reached the goal (where all jobs have been delivered)?'''
    # goal state: finish all carrying jobs and no jobs unstarted
    return not state.get_carrying() and not state.get_unstarted()

def make_start_state(map_list, job_list):
#IMPLEMENT
    '''Input a map list and a job_list. Return a bicycle StateSpace object
    with action "START", gval = 0, and initial location "home" that represents the 
    starting configuration for the scheduling problem specified'''
    state = {
        "loc": "home",
        "current_jobs": [],
        "load": 0,
        "time": 420, # no actual meaning, placeholder
        "earned": 0,
        "future_jobs": job_list
    }
    bicycle.map_list = map_list
    return bicycle("START", 0, state, None)

    
########################################################
#   Functions provided so that you can more easily     #
#   Test your implementation                           #
########################################################

def make_rand_map(nlocs):
    '''Generate a random collection of locations and distances 
    in input format'''
    lpairs = [(randint(0,50), randint(0,50)) for i in range(nlocs)]
    lpairs = list(set(lpairs))  #remove duplicates
    nlocs = len(lpairs)
    lnames = ["loc{}".format(i) for i in range(nlocs)]
    ldists = list()

    for i in range(nlocs):
        for j in range(i+1, nlocs):
            ldists.append([lnames[i], lnames[j],
                           int(round(euclideandist(lpairs[i], lpairs[j])))])
    return [lnames, ldists]

def dist(l1, l2, map):
    '''Return distance from l1 to l2 in map (as output by make_rand_map)'''
    ldist = map[1]
    if l1 == l2:
        return 0
    for [n1, n2, d] in ldist:
        if (n1 == l1 and n2 == l2) or (n1 == l2 and n2 == l1):
            return d
    return 0
    
def euclideandist(p1, p2):
    return sqrt((p1[0]-p2[0])*(p1[0]-p2[0]) + (p1[1]-p2[1])*(p1[1]-p2[1]))

def make_rand_jobs(map, njobs):
    '''input a map (as output by make_rand_map) object and output n jobs in input format'''
    jobs = list()
    for i in range(njobs):
        name = 'Job{}'.format(i)
        ploc = map[0][randint(0,len(map[0])-1)]
        ptime = randint(7*60, 16*60 + 30) #no pickups after 16:30
        dloci = randint(0, len(map[0])-1)
        if map[0][dloci] == ploc:
            dloci = (dloci + 1) % len(map[0])
        dloc = map[0][dloci]
        weight = randint(10, 5000)
        job = [name, ploc, ptime, dloc, weight]
        payoffs = list()
        amount = 50
        #earliest delivery time
        time = ptime + dist(ploc, dloc, map)
        for j in range(randint(1,5)): #max of 5 payoffs
            time = time + randint(5, 120) #max of 120mins between payoffs
            amount = amount - randint(5, 25)
            if amount <= 0 or time >= 19*60:
                break
            payoffs.append([time, amount])
        job.append(payoffs)
        jobs.append(job)
    return jobs

def test(nloc, njobs):
    map = make_rand_map(nloc)
    jobs = make_rand_jobs(map, njobs)
    print("Map = ", map)
    print("jobs = ", jobs)
    s0 = make_start_state(map, jobs)
    print("heur Sum = ", heur_sum_delivery_costs(s0))
    print("heur max = ", heur_max_delivery_costs(s0))
    se = SearchEngine('astar', 'full')
    #se.trace_on(2)
    final = se.search(s0, bicycle_goal_fn, heur_max_delivery_costs)
