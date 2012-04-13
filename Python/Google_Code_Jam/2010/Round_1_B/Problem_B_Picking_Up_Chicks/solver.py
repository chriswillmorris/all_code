import Google_Code_Jam.problem_solver as gcj_solver

# Used for testing
reload(gcj_solver)

import logger

import copy
import os



def run_unit_tests():
    """
    Runs all the unit tests
    """

    solver = Solver()
    solver._generate_clump_permutations

    chicks = [[0,5], [1,3], [2,4], [3,1], [4,6]]
    res = solver._generate_clump_permutations(chicks)

    expected = [
        [[0, 5], [1, 3], [2, 4], [3, 1], [4, 6]],
        [[1, 3], [0, 5], [2, 4], [3, 1], [4, 6]],
        [[1, 3], [2, 4], [0, 5], [3, 1], [4, 6]],
        [[1, 3], [2, 4], [3, 1], [0, 5], [4, 6]],
        [[1, 3], [3, 1], [2, 4], [0, 5], [4, 6]],
        [[3, 1], [1, 3], [2, 4], [0, 5], [4, 6]],
        [[1, 3], [0, 5], [3, 1], [2, 4], [4, 6]],
        [[1, 3], [3, 1], [0, 5], [2, 4], [4, 6]],
        [[3, 1], [1, 3], [0, 5], [2, 4], [4, 6]],
        [[0, 5], [1, 3], [3, 1], [2, 4], [4, 6]],
        [[0, 5], [3, 1], [1, 3], [2, 4], [4, 6]],
        [[3, 1], [0, 5], [1, 3], [2, 4], [4, 6]]
        ]

    assert (len(expected) == len(res))
    for case in expected:
        assert case in res


    chicks = [[4,3],[5,2],[6,4],[8,6],[10,6],[11,3],[12,1],[14,10]]
    res = solver._get_clumps(chicks)

    expected = [
        [[4, 3], [5, 2], [6, 4]],
        [[8, 6]],
        [[10, 6], [11, 3], [12, 1]],
        [[14, 10]]
        ]
    assert (len(expected) == len(res))
    for case in expected:
        assert case in res



    res = [solver._generate_clump_permutations(clump) for clump in res]


    expected = [
        [
            [[4,3],[5,2],[6,4]],
            [[5,2],[4,3],[6,4]]
            ],
    [
        [[8,6]]
        ],
    [
        [[10,6],[11,3],[12,1]],
        [[11,3],[10,6],[12,1]],
        [[11,3],[12,1],[10,6]],
        [[12,1],[11,3],[10,6]],
        [[10,6],[12,1],[11,3]],
        [[12,1],[10,6],[11,3]]
        ],
    [
        [[14,10]]
        ]
        ]


    assert (len(expected) == len(res))
    for case in expected:
        assert case in res


    inputs = [
        [
            [1,5,11],
            [1,11,5]
            ],
        [
            [6,8,10],
            [10,8,6]
            ]
        ]

    res = solver._generate_new_swap_states(inputs)
        
    expected = [
        [1,5,11,6,8,10],
        [1,5,11,10,8,6],
        [1,11,5,6,8,10],
        [1,11,5,10,8,6]
        ]

    assert (len(expected) == len(res))
    for case in expected:
        assert case in res
        
    print "All tests passed"




class Solver(gcj_solver.ProblemSolver):

    
    def __init__(self):
        base_path = "C:\\Users\\cmorris\\Documents\\Projects\\github_repo\\all_code\\Python\\Google_Code_Jam\\2010\\Round_1_B\\Problem_B_Picking_Up_Chicks"
        


        gcj_solver.ProblemSolver.__init__(
            self,
            os.path.join(base_path, "B-small-practice.in"),
            os.path.join(base_path, "B-small-practice.out"),
            True,
            o_debug_file = os.path.join(base_path, "B-small-practice.debug"))



        """
        gcj_solver.ProblemSolver.__init__(
            self,
            os.path.join(base_path, "B-large-practice.in"),
            os.path.join(base_path, "B-large-practice.out"),
            True,
            o_debug_file = os.path.join(base_path, "B-large-practice.debug"))
        """


        self._force_printing = False
        self._debug = True

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

        #print locations
        self._chicks = zip(locations, velocities)
        


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
        logger.log("n:{n}, k:{k}, b:{b}, t:{t}".format(n=self._n, k=self._k, b=self._b, t=self._t), i_force=True, o_log_file=self._debug_file)
        #print self._chicks
        logger.log("chicks: {0}".format(self._chicks), i_debug=self._debug, i_force=False, o_log_file=self._debug_file)
        #print self._chicks
        #print("ljlj {0}".format(self._chicks))


    def _generate_clump_permutations_imp(self, i_clump, io_clumps):
        """
        For every chick but the last (which is the one in front),
        try to swap it
        """

        # Never swap a slower chick to be in front of a faster one.

        # Keep the permutation where nothing changes!
        if i_clump not in io_clumps:
            io_clumps.append(i_clump)

        for i in range (len(i_clump) - 1):
            if i_clump[i][1] > i_clump[i+1][1]:
                # The chick behind is faster. Swap them and add
                # this new clump
                new_clump = i_clump[:i]
                new_clump.extend([i_clump[i+1],i_clump[i]])
                new_clump.extend(i_clump[i+2:])
                if new_clump not in io_clumps:
                    # This new clump hasn't been discovered yet.
                    # Add it and generate the clumps that stem
                    # from this one
                    io_clumps.append(new_clump)
                    self._generate_clump_permutations_imp(new_clump, io_clumps)


    def _generate_clump_permutations(self, i_clump):
        clump_list = []
        self._generate_clump_permutations_imp(i_clump, clump_list)
        return clump_list


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
                    ret.append(retval)

        #print ("returning ", ret)
        return ret


    def _generate_swaps(self, i_state):
        # You can only swap chicks that are next to each other.
        # Call a group of chicks that are all next to each other
        # a 'clump.' The total # of valid states is the product
        # of valid swaps for each clump

        clumps = self._get_clumps(i_state)

        new_clumps_list = [self._generate_clump_permutations(clump) for clump in clumps]

        # Each set of new culmps is a list of tuples where item 0
        # is the new clump state and item 1 is the number of swaps
        # needed to get to that state from the original

        return self._generate_new_swap_states(new_clumps_list)




if __name__ == "__main__":

    run_unit_tests()
    
    """
    solver = Solver()

    print("running tests")
    solver.solve()
    """
