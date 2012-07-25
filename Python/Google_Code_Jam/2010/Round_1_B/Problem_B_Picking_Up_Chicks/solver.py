import Google_Code_Jam.problem_solver as gcj_solver

# Used for testing
reload(gcj_solver)

import logger

import copy
import os
import sys




def run_unit_tests():
    """
    Runs all the unit tests
    """

    solver = Solver()
    #solver._generate_clump_permutations()

    chicks = [[0,5,0], [1,3,0], [2,4,0], [3,1,0], [4,6,0]]
    res = solver._generate_clump_permutations(chicks)

    #clumps, num_swaps = zip(*res)

    expected_clumps = [
        [[0, 5, 0], [1, 3, 0], [2, 4, 0], [3, 1, 0], [4, 6, 0]],
        [[0, 3, 1], [1, 5, 1], [2, 4, 0], [3, 1, 0], [4, 6, 0]],
        [[0, 3, 1], [1, 4, 1], [2, 5, 2], [3, 1, 0], [4, 6, 0]],
        [[0, 3, 1], [1, 4, 1], [2, 1, 1], [3, 5, 3], [4, 6, 0]],
        [[0, 3, 1], [1, 1, 2], [2, 4, 2], [3, 5, 3], [4, 6, 0]],
        [[0, 1, 3], [1, 3, 2], [2, 4, 2], [3, 5, 3], [4, 6, 0]],
        [[0, 3, 1], [1, 5, 1], [2, 1, 1], [3, 4, 1], [4, 6, 0]],
        [[0, 3, 1], [1, 1, 2], [2, 5, 2], [3, 4, 1], [4, 6, 0]],
        [[0, 1, 3], [1, 3, 2], [2, 5, 2], [3, 4, 1], [4, 6, 0]],
        [[0, 5, 0], [1, 3, 0], [2, 1, 1], [3, 4, 1], [4, 6, 0]],
        [[0, 5, 0], [1, 1, 2], [2, 3, 1], [3, 4, 1], [4, 6, 0]],
        [[0, 1, 3], [1, 5, 1], [2, 3, 1], [3, 4, 1], [4, 6, 0]]
        ]

    expected_swaps = [0,1,2,3,4,5,2,3,4,1,2,3]

    #print "res: "
    #for r in res:
        #print r
    assert (len(expected_clumps) == len(res))
    #assert (len(expected_swaps) == len(clumps))
    for case in expected_clumps:
        assert case in res
    #for case in expected_swaps:
        #assert case in num_swaps


    chicks = [[4,3, 0],[5,2,0],[6,4,0],[8,6,0],[10,6,0],[11,3,0],[12,1,0],[14,10,0]]
    res = solver._get_clumps(chicks)

    expected = [
        [[4, 3, 0], [5, 2, 0], [6, 4, 0]],
        [[8, 6, 0]],
        [[10, 6, 0], [11, 3, 0], [12, 1, 0]],
        [[14, 10, 0]]
        ]
    assert (len(expected) == len(res))
    for case in expected:
        assert case in res

    res = [solver._generate_clump_permutations(clump) for clump in res]

    expected = [
        [
            [[4,3,0],[5,2,0],[6,4,0]],
            [[4,2,1],[5,3,1],[6,4,0]]
            ],
    [
        [[8,6,0]]
        ],
    [
        [[10,6,0],[11,3,0],[12,1,0]],
        [[10,3,1],[11,6,1],[12,1,0]],
        [[10,3,1],[11,1,1],[12,6,2]],
        [[10,1,2],[11,3,2],[12,6,2]],
        [[10,6,0],[11,1,1],[12,3,1]],
        [[10,1,2],[11,6,1],[12,3,1]]
        ],
    [
        [[14,10,0]]
        ]
        ]


    assert (len(expected) == len(res))
    #for r in res:
        #print r
    for case in expected:
        assert case in res


    inputs = [
        [
            [[1,5,0],[2,100,0]],
            [[1,100,1],[2,5,1]]
            ],
        [
            [[7,5,0],[8,3,0]],
            [[7,3,1],[8,5,1]]
            ]
        ]

    res = solver._generate_new_swap_states(inputs)

    expected = [
        [[1,5,0],[2,100,0],[7,5,0],[8,3,0]],
        [[1,5,0],[2,100,0],[7,3,1],[8,5,1]],
        [[1,100,1],[2,5,1],[7,5,0],[8,3,0]],
        [[1,100,1],[2,5,1],[7,3,1],[8,5,1]],
        ]

    assert (len(expected) == len(res))
    for case in expected:
        assert case in res


    solver._b = 10

    
    #assert(solver._num_arrived(chicks_reformed) == 4)
    assert(solver._num_arrived(chicks) == 4)


    # chicks_reformed = [[4,3],[5,2],[6,4],[8,6],[10,6],[11,3],[12,1],[14,10]]
    chicks_cpy = copy.deepcopy(chicks)

    solver._step_forward_internal(chicks_cpy, 0)
    #assert(chicks_cpy == chicks_reformed)

    solver._step_forward_internal(chicks_cpy, 1)
    expected = [[6, 3, 0], [7, 2, 0], [9, 4, 0], [10, 6, 0], [11, 6, 0], [12, 3, 0], [13, 1, 0], [24, 10, 0]]

    assert(chicks_cpy == expected)

    

    chicks_cpy = copy.deepcopy(chicks)
    assert (solver._step_forward(chicks_cpy, i_num_steps=2) == 2)
    expected = [[8,3,0],[9,2,0],[10,4,0],[11,6,0],[12,6,0],[13,3,0],[14,1,0],[34,10,0]]
    assert(chicks_cpy == expected)



    chicks_cpy = copy.deepcopy(chicks)
    """
    print "can step forward {0}".format(solver._can_step_forward(chicks_cpy))
    solver._step_forward_internal(chicks_cpy, 1)
    print "chicks cpy: ", chicks_cpy
    
    print chicks_cpy
    print num_steps
    """
    num_steps = solver._step_forward(chicks_cpy, i_num_steps='max', i_max=100)
    assert (num_steps == 0)


    # Put in a test case here
    chicks_cpy = [[3,4], [15,5], [40,6], [70,7], [110,8], [160,10]]
    num_steps = solver._step_forward(chicks_cpy, 7)
    assert (num_steps == 7)
    expected = [[31,4], [50,5], [82,6], [119,7], [166,8], [230,10]]
    assert(chicks_cpy == expected)


    chicks_cpy = [[3,1], [23,11], [40,6], [106,2], [110,8], [120,3]]
    num_steps = solver._step_forward(chicks_cpy, 7)
    assert (num_steps == 7)
    expected = [[10,1], [81,11], [82,6], [120,2], [140,8], [141,3]]
    assert(chicks_cpy == expected)


    chicks_cpy = [[3,1], [23,11], [40,6], [106,2], [110,8], [120,3]]
    num_steps = solver._step_forward(chicks_cpy, i_num_steps='max')
    assert (num_steps == 1)
    expected = [[4,1], [34,11], [46,6], [108,2], [118,8], [123,3]]
    assert(chicks_cpy == expected)


    chicks_cpy = [[3,1], [23,11], [40,6], [106,2], [110,8], [126,3]]
    num_steps = solver._step_forward(chicks_cpy, i_num_steps='max')
    assert (num_steps == 3)
    expected = [[6,1], [56,11], [58,6], [112,2], [134,8], [135,3]]
    assert(chicks_cpy == expected)


    solver._k = 4
    solver._t = 400
    solver._b = 15
    print "chickies ", chicks
    print solver._solve_state(chicks, 0, 0, sys.maxint)
    print "All tests passed"




class Solver(gcj_solver.ProblemSolver):

    
    def __init__(self):
        base_path = "C:\\Users\\cmorris\\Documents\\Projects\\github_repo\\all_code\\Python\\Google_Code_Jam\\2010\\Round_1_B\\Problem_B_Picking_Up_Chicks"

        fname = "B-small-practice"
        #fname = "B-large-practice"
        #fname = 'test'

        #super(gcj_solver.ProblemSolver, self).__init__(self, base_path, fname, True, False)

        gcj_solver.ProblemSolver.__init__(self, base_path, fname, True, True)

        # Problem parameters
        self._n = None
        self._k = None
        self._b = None
        self._t = None
        self._chicks = None

                       
    def get_case_input(self):
        """
        See base class
        """

        self._reset_input_vars()

        first_line = self._in_file.readline().strip()
        (self._n, self._k, self._b, self._t) = [int(x) for x in first_line.split(" ")]
        locations = [int(x) for x in self._in_file.readline().strip().split(" ")]
        velocities = [int(x) for x in self._in_file.readline().strip().split(" ")]
        swaps = [0] * len(locations)

        #print locations
        self._chicks = zip(locations, velocities, swaps)
        self._chicks = [list(tuple) for tuple in self._chicks]



    def _reset_input_vars(self):
        # Resets input variables
        pass

    def _cleanup(self):
        # Store the winners and losers in an external file.
        # They can then be loaded in next time so things
        # don't need to be recalculated
        pass


    def _init(self):
        # Load any winners/losers that have been calculated on
        # a previous run so things don't need to be
        # recalculated
        pass


    def solve_case(self):

        logger.log("n:{n}, k:{k}, b:{b}, t:{t}".format(n=self._n, k=self._k, b=self._b, t=self._t), i_debug=self._debug, i_force=self._force_printing, o_log_file=self._debug_file)
        logger.log("chicks: {0}".format(self._chicks), i_debug=self._debug, i_force=self._force_printing, o_log_file=self._debug_file)

        ret = self._solve_state(self._chicks, 0, 0, sys.maxint)
        if ret == sys.maxint:
            return "No Solution"

        return ret
        #print self._chicks
        #print("ljlj {0}".format(self._chicks))


    def _solve_state(self, i_state, i_cur_time, i_num_swaps, i_min_num_swaps, i_indent=0):
        """
        i_cur_time : The number of time steps that have already been used.
        For example: if i_cur_time is 5 and the max time is 8, then there are 3
        time steps left: 6, 7, and 8.
        """

        #self.log(' ' * i_indent + "time: {0}, state: {1}, num_swaps: {2}, min_num_swaps: {3}".format(i_cur_time, i_state, i_num_swaps, i_min_num_swaps))
        
        if i_cur_time >= self._t:
            # No swapping will help, and we can't step forward anymore,
            # so our current effort has failed
            return i_min_num_swaps
        elif i_num_swaps >= i_min_num_swaps:
            # Short circuit
            logger.log("i_num_swaps >= i_min_num_swaps with {0} > {1}".format(i_num_swaps,i_min_num_swaps), i_debug=self._debug, i_force=self._force_printing, o_log_file=self._debug_file)
            return i_min_num_swaps
        elif self._num_arrived(i_state) >= self._k:
            # Goal achieved. Based on the previous condition,
            # we know that num_swaps is better than min_num_swaps
            logger.log("Goal Achieved", i_debug=self._debug, i_force=self._force_printing, o_log_file=self._debug_file)
            return i_num_swaps

        # Skip the first pair (which is the original state) so as to
        # avoid infinite recursion
        #new_states = self._generate_swaps(i_state)[1:]
        new_states = self._generate_swaps(i_state)

        for index, state in enumerate(new_states):
            num_swaps = self._num_swaps(state)
            updated_num_swaps = i_num_swaps + num_swaps

            if updated_num_swaps >= i_min_num_swaps:
                # No point in checking futher. Short circuit
                continue

            copy_of_state = copy.deepcopy(state)
            num_steps_left = self._t - i_cur_time
            self._step_forward(copy_of_state, i_num_steps=num_steps_left)
            if self._num_arrived(copy_of_state) >= self._k:
                # A valid state!
                # We know this state won't produce a smaller number of swaps than
                # what has already been found. Short circuit.
                i_min_num_swaps = min(i_min_num_swaps, updated_num_swaps)
                continue

            copy_of_state = copy.deepcopy(state)
            num_steps = self._step_forward(copy_of_state, i_num_steps='max', i_max=num_steps_left)
            #print ' ' * i_indent, 'num_steps: ', num_steps

            if num_steps == 0:
                # At least one chick was blocked from moving freely for
                # a single time step. Force the state to proceed until
                # a chick is blocked that isn't currently being blocked from
                # proceeding a single timestep
                num_steps = self._advance_past_first_set_of_blocked_chicks(copy_of_state, num_steps_left)

            updated_time = i_cur_time + num_steps

            if updated_time >= self._t:
                # No swapping will help, and we can't step forward anymore,
                # so our current effort has failed
                if updated_time == self._t:
                    # Print this case explicity because the 'continue' statement will cause the later log call
                    # to be skipped
                    self.log(' ' * i_indent + 'swap total of {0} and time of {1} : {2} min_num_swaps:{3}'.format(updated_num_swaps, updated_time, copy_of_state, i_min_num_swaps))
                continue

            self.log(' ' * i_indent + 'swap total of {0} and time of {1} : {2} min_num_swaps:{3}'.format(updated_num_swaps, updated_time, copy_of_state, i_min_num_swaps))

            # Don't make a recursive call on the original state. Doing so would result
            # in an infinite loop
            if index > -1:
                # Add in the number of swaps for each chick
                i_min_num_swaps = self._solve_state(copy_of_state, updated_time, updated_num_swaps, i_min_num_swaps, i_indent + 2)

        return i_min_num_swaps



    def _step_forward(self, i_state, i_num_steps, i_max=sys.maxint):
        """
        Return : the number of steps taken (the number of time 'ticks')
        """

        num_steps = 0
        if i_num_steps == 'max':
            while self._can_step_forward(i_state) and (num_steps < i_max):
                self._step_forward_internal(i_state, 1)
                num_steps += 1
        else:
            self._step_forward_internal(i_state, i_num_steps)
            num_steps = i_num_steps
        return num_steps



    def _can_step_forward(self, i_state):
        """
        Returns True if every chick can move forward their full amount
        for a single tick.
        """
        return self._step_forward_internal(copy.deepcopy(i_state), 1) == 0


    def _step_forward_internal(self, i_state, i_num_steps):
        """
        i_state[-1] is the furthest along chick
        i_state[0] is the furthest away chick
        """

        num_blocked = 0
        for i in range(len(i_state) - 1, -1, -1):
            cur_chick = i_state[i]
            unhindered = cur_chick[0] + (cur_chick[1] * i_num_steps)
            if i == (len(i_state) - 1):
                # Chick in the front
                cur_chick_pos = unhindered
            else:
                # Remember, can't pass the chick in front of you
                chick_ahead = i_state[i+1]
                cur_chick_pos = min(unhindered, chick_ahead[0] - 1)
                if unhindered > cur_chick_pos:
                    num_blocked += 1
            cur_chick[0] = cur_chick_pos

        return num_blocked



    def _num_arrived(self, i_state):
        """
        Returns the number of chicks that have reached the
        destinatation
        """
        return len(filter(lambda x: x[0] >= self._b, i_state))



    def _num_swaps(self, i_state):
        """
        Returns the number of times a pair of chicks has been
        swapped for the given state
        """

        # Sum up the 3rd element (which is the number of times
        # the chick has been swapped) and divided by 2, since
        # swapping a single pair of chicks will result in both
        # of their swap counts being incremented
        return sum([chick[2] for chick in i_state]) / 2



    def _generate_clump_permutations_imp(self, i_clump, i_num_swaps_to_get_here, io_clumps, io_swaps_for_clumps):
        """
        For every chick but the last (which is the one in front),
        try to swap it
        """

        # Never swap a slower chick to be in front of a faster one.

        # Keep the permutation where nothing changes!
        """
        print('io_clumps:')
        for i in io_clumps:
            print i
        """

        if i_clump not in io_clumps:
            io_clumps.append(i_clump)

        for i in range (len(i_clump) - 1):
            if i_clump[i][1] > i_clump[i+1][1]:
                # The chick behind is faster. Swap them and add
                # this new clump
                new_clump = i_clump[:i]

                # Increase the faster chick's position, decrease the
                # slower chick's. Add one to each of their swap counts
                faster_chick = [i_clump[i][0] + 1, i_clump[i][1], i_clump[i][2] + 1]
                slower_chick = [i_clump[i+1][0] - 1, i_clump[i+1][1], i_clump[i+1][2] + 1]

                new_clump.extend([slower_chick,faster_chick])
                new_clump.extend(i_clump[i+2:])
                if new_clump not in io_clumps:
                    # This new clump hasn't been discovered yet.
                    # Add it and generate the clumps that stem
                    # from this one
                    io_clumps.append(new_clump)
                    self._generate_clump_permutations_imp(new_clump, i_num_swaps_to_get_here + 1, io_clumps, io_swaps_for_clumps)


    def _generate_clump_permutations(self, i_clump):
        clump_list = []
        swaps_for_clumps = []
        self._generate_clump_permutations_imp(i_clump, 0, clump_list, swaps_for_clumps)

        #assert(len(clump_list) == len(swaps_for_clumps))
        """
        print 'clump list'
        for c in clump_list:
            print c
        print 'num swaps'
        for c in swaps_for_clumps:
            print c
        """
        return clump_list
        
        #return zip(clump_list, swaps_for_clumps)


    def _get_clumps(self, i_state):
        """
        Returns a list of clumps, where each clump is a list
        of chicks that are next to each other
        Note: chicks are assumed to be in order from furthest
        from finish line to closest to finish line
        """

        clumps = []
        clump = []
        for i, chick in enumerate(i_state):
            if not clump:
                # Beginning of clump
                clump.append(chick)
            elif (clump[-1][0] + 1) == chick[0]:
                # Current chick is directly in front of the previous chick
                clump.append(chick)
            else:
                # There is a gap between the previous and the current chicks
                clumps.append(clump)
                clump = []
                clump.append(chick)

        # Don't forget the final clump
        if clump:
            clumps.append(clump)

        return clumps


    def _generate_new_swap_states(self, i_clumps_list):
        """
        Input: A list of lists, where the inner list's items are
        3-tuples (pos,vec,num swaps)
        """
        if not i_clumps_list:
            return []

        ret = []

        #print ("generating new swap states for {0}".format(i_clumps_list[1:]))
        new_swap_states = self._generate_new_swap_states(i_clumps_list[1:])
        for clump in i_clumps_list[0]:
            if not new_swap_states:
                # The last clump
                #print ("adding ", clump)
                ret.append(copy.deepcopy(clump))
            else:
                for new_swap_state in new_swap_states:
                    #print ("appending ", new_swap_state, " to ", clump)
                    retval = copy.deepcopy(clump)
                    retval.extend(new_swap_state)
                    #retval = (retval[0], retval[1] + new_swap_state[1])

                    ret.append(retval)

        #print ("returning ", ret)
        return ret


    def _generate_swaps(self, i_state):
        # You can only swap chicks that are next to each other.
        # Call a group of chicks that are all next to each other
        # a 'clump.' The total # of valid states is the product
        # of valid swaps for each clump

        clumps = self._get_clumps(i_state)

        #print 'clumpers: ', clumps

        new_clumps_list = [self._generate_clump_permutations(clump) for clump in clumps]

        #print 'new clumps list: ', new_clumps_list

        # Each set of new clumps is a list of tuples where item 0
        # is the new clump state and item 1 is the number of swaps
        # needed to get to that state from the original

        #retval = self._generate_new_swap_states(new_clumps_list)
        #print 'new swap states: ', retval

        return self._generate_new_swap_states(new_clumps_list)


    def _advance_past_first_set_of_blocked_chicks(self, io_state, i_max_steps):
        """
        It's assummed that the state could not be advanced even one time step
        without at least one chick getting blocked.
        """

        num_chicks_initially_blocked = self._step_forward_internal(copy.deepcopy(io_state), 1)

        # Keep doubling the time step until we reach a state where
        # a chick is blocked that is NOT in the initial group of
        # blocked chicks
        old_num_steps = 1
        num_steps = 1
        num_blocked = self._step_forward_internal(copy.deepcopy(io_state), num_steps)

        # Keep doubling the number of steps
        # max_steps_taken is always a number of steps
        # that, if taken, will result in more than only
        # the initial set of chicks to be blocked
        while True:
            if num_steps > i_max_steps:
                max_steps_taken = i_max_steps + 1
                break
            elif num_blocked > num_chicks_initially_blocked:
                # Technically, I could just set max_steps_taken
                # equal to num_steps, since I know that num_steps
                # is <= i_max_steps, but this could change if the
                # order of if statements is switched
                max_steps_taken = min(num_steps, i_max_steps + 1)
                break

            old_num_steps = num_steps
            num_steps *= 2
            num_blocked = self._step_forward_internal(copy.deepcopy(io_state), num_steps)

        # Now that you've found the maximum, perform a binary search to find
        # the maximum number of time steps without any additional chicks
        # being blocked
        _max = max_steps_taken
        _min = old_num_steps
        while True:
            # Pick the number immediately in between min and max
            increment = (_max - _min) / 2
            if 0 == increment:
                # Min should be one less than max, so there is nowhere left to search.
                # The number has been found.
                old_num_steps = _min
                break
            
            num_steps = _min + increment

            num_blocked = self._step_forward_internal(copy.deepcopy(io_state), num_steps)
            if num_blocked > num_chicks_initially_blocked:
                # Attempt failed. Drop down the ceiling.
                _max = num_steps
            else:
                # Attempt succeeded. Raise the floor.
                _min = num_steps

        self._step_forward_internal(io_state, old_num_steps)
        assert(old_num_steps <= i_max_steps)
        return old_num_steps
        



if __name__ == "__main__":

    #run_unit_tests()
    

    solver = Solver()

    print("running tests")
    solver.solve()

