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
        base_path = "C:\\Users\\cmorris\\Documents\\Projects\\github_repo\\all_code\\Python\\Google_Code_Jam\\2012\\Round_1_A\\Problem_A"
        
        fname = 'B-small-attempt0'
        fname = 'B-large'
        fname = 'test'

        gcj_solver.ProblemSolver.__init__(self, base_path, fname, True, False)

        # Problem parameters
        self._A = None
        self._B = None
        self._probs = None

                       
    def get_case_input(self):
        """
        See base class
        """

        self._reset_input_vars()

        first_line = self._in_file.readline().strip()
        first_line = first_line.split(' ')
        #print "first line", first_line
        self._A = int(first_line[0])
        self._B = int(first_line[1])

        second_line = self._in_file.readline().strip().split(' ')
        #print "second line", second_line
        self._probs = [float(x) for x in second_line]



    def _reset_input_vars(self):
        # Resets input variables
        pass

    def _cleanup(self):
        pass


    def _init(self):
        pass


    def solve_case(self):
        logger.log("A:{A}, B:{B}, probs:{probs}".format(A=self._A,B=self._B,probs=self._probs), i_force=True, o_log_file=self._debug_file)

        return None
    



if __name__ == "__main__":

    #run_unit_tests()
    

    solver = Solver()

    print("running tests")
    solver.solve()

