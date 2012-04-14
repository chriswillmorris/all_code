import Google_Code_Jam.problem_solver as gcj_solver

# Used for testing
reload(gcj_solver)

import logger



def run_unit_tests():
    """
    Runs all the unit tests
    """
    print "All tests passed"



class Solver(gcj_solver.ProblemSolver):

    
    def __init__(self):
        base_path = "/home/chris/all_code/Python/Google_Code_Jam/2012/Round_1_A/Problem_A"
        
        fname = 'B-small-attempt0'
        fname = 'B-large'

        gcj_solver.ProblemSolver.__init__(self, base_path, fname, True, False)

        # Problem parameters
        self._N = None
        self._S = None
        self._p = None
        self._pts = None

                       
    def get_case_input(self):
        """
        See base class
        """

        self._reset_input_vars()

        first_line = self._in_file.readline().strip()
        inputs = first_line.split(' ')
        self._N = int(inputs[0])
        self._S = int(inputs[1])
        self._p = int(inputs[2])

        self._pts = []
        for total_score in inputs[3:]:
            self._pts.append(total_score)


    def _reset_input_vars(self):
        # Resets input variables
        pass

    def _cleanup(self):
        pass


    def _init(self):
        pass


    def solve_case(self):
        logger.log("N:{N}, S:{S}, p:{p}, pts:{pts}".format(N=self._N,S=self._S,p=self._p,pts=self._pts), i_force=True, o_log_file=self._debug_file)

        no_surprise = self._p + (2 * max(self._p - 1, 0))
        surprise = self._p + (2 * max(self._p - 2, 0))

        num_surprises_counted = 0

        num_qualified = 0
        for tot_score in self._pts:
            tot_score = int(tot_score)
            if tot_score >= no_surprise:
                num_qualified += 1
            elif (num_surprises_counted < self._S) and (tot_score >= surprise):
                num_qualified += 1
                num_surprises_counted +=1
                
        return num_qualified
    



if __name__ == "__main__":

    #run_unit_tests()
    

    solver = Solver()

    print("running tests")
    solver.solve()

