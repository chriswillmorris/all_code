import Google_Code_Jam.problem_solver as gcj_solver

# Used for testing
reload(gcj_solver)

import os



class Solver(gcj_solver.ProblemSolver):
    
    def __init__(self):
        base_path = "C:\\Users\\cmorris\\Documents\\Projects\\github_repo\\all_code\\Python\\Google_Code_Jam\\2010\\Round_1_A\\Problem_C_Number_Game"
        
        
        gcj_solver.ProblemSolver.__init__(
            self,
            os.path.join(base_path, "C-small-practice.in"),
            os.path.join(base_path, "C-small-practice.out"),
            True,
            o_debug_file = os.path.join(base_path, "C-small-practice.debug"))

        # Problem parameters
        self._a1 = None
        self._a2 = None
        self._b1 = None
        self._b2 = None
                       

    def get_case_input(self):
        """
        See base class
        """

        first_line = self._in_file.readline().strip()
        (self._a1, self._a2, self._b1, self._b2) = [int(x) for x in first_line.split(" ")]


    def solve_case(self):
        print("a1:{a1}, a2:{a2}, b1:{b1}, b2:{b2}".format(a1=self._a1, a2=self._a2, b1=self._b1, b2=self._b2))

        # Test every position requested and count the number of
        # winning positions
        num_wins = 0
        for a in range(self._a1, self._a2 + 1):
            for b in range(self._b1, self._b2 + 1):
                state = (a,b)
                _build_tree(state)
                if state in g_winners:
                    num_wins += 1
                #print(state)
                
        return "Fake Data"



if __name__ == "__main__":
    solver = Solver()

    print("running tests")
    solver.solve()
    
