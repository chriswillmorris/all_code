import Google_Code_Jam.problem_solver as gcj_solver

# Used for testing
reload(gcj_solver)

import logger



def run_unit_tests():
    """
    Runs all the unit tests
    """

    slvr = Solver()
    print slvr._recycled(23,32)
    print "All tests passed"



class Solver(gcj_solver.ProblemSolver):

    
    def __init__(self):
        base_path = "/home/chris/all_code/Python/Google_Code_Jam/2012/Qualification_Round/Problem_C"

        fname = 'C-small-practice'
        fname = 'C-large-practice'
        #fname = 'test'

        gcj_solver.ProblemSolver.__init__(self, base_path, fname, True, False)

        # Problem parameters
        self._A = None
        self._B = None

        self._non_recycled = set()
        self._recycled = set()

                       
    def get_case_input(self):
        """
        See base class
        """

        self._reset_input_vars()

        first_line = self._in_file.readline().strip()
        self._A, self._B = [int(x) for x in first_line.split(' ')]


    def _reset_input_vars(self):
        # Resets input variables
        pass

    def _cleanup(self):
        pass


    def _init(self):
        pass


    def solve_case(self):
        logger.log("A:{A}, B:{B}".format(A=self._A, B=self._B), i_force=True, o_log_file=self._debug_file)

        num_recycled = 0
        recycled = set()
        for i in range(self._A, self._B + 1):
            if i < 10:
                # Single digit numbers fail automatically
                continue
            si = str(i)

            # Try every set of rotated digits
            for j in range(1,len(si)):
                new_num = int(si[j:] + si[:j])
                if new_num == i:
                    # Equal digits don't count
                    continue
                if (new_num >= self._A) and (new_num <= self._B):
                    # The rotated number is within the bounds
                    if ((i,new_num) not in recycled) and ((new_num,i) not in recycled):
                        # It's already been seen as recycled
                        recycled.add((i,new_num))
                        #print i,new_num
                        num_recycled += 1

        #print recycled
        return num_recycled



if __name__ == "__main__":

    #run_unit_tests()
    


    solver = Solver()

    print("running tests")
    solver.solve()


