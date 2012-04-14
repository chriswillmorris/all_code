import Google_Code_Jam.problem_solver as gcj_solver

# Used for testing
reload(gcj_solver)

import logger

import copy
import os


inputs = ["ejp mysljylc kd kxveddknmc re jsicpdrysi",
"rbcpc ypc rtcsra dkh wyfrepkym veddknkmkrkcd",
"de kr kd eoya kw aej tysr re ujdr lkgc jv"]

outputs = ["our language is impossible to understand",
"there are twenty six factorial possibilities",
"so it is okay if you want to just give up"]

alphabet = dict()
for in1,out1 in zip(inputs,outputs):
    for a,b in zip(in1, out1):
        alphabet[a] = b

alphabet['z'] = 'q'
alphabet['q'] = 'z'
        
full_alphabet = 'abcdefghijklmnopqrstuvwxyz'
for letter in full_alphabet:
    if letter not in alphabet.keys():
        print "missing key: ", letter
    if letter not in alphabet.values():
        print "missing value: ", letter

def run_unit_tests():
    """
    Runs all the unit tests
    """

    #solver = Solver()



    for a in alphabet:
        print a, alphabet[a]


        
    print "All tests passed"




class Solver(gcj_solver.ProblemSolver):

    
    def __init__(self):
        base_path = "/home/chris/all_code/Python/Google_Code_Jam/2012/Qualification_Round/Problem_A"

        fname = 'A-small-attempt0'

        gcj_solver.ProblemSolver.__init__(self, base_path, fname, True, False)


        # Problem parameters
        self._g = None

                       
    def get_case_input(self):
        """
        See base class
        """

        self._reset_input_vars()

        first_line = self._in_file.readline().strip()
        self._g = first_line
        


    def _reset_input_vars(self):
        # Resets input variables
        pass

    def _cleanup(self):
        pass


    def _init(self):
        pass


    def solve_case(self):
        logger.log("g:{g}".format(g=self._g), i_force=True, o_log_file=self._debug_file)

        output = ''
        for i in self._g:
            output += alphabet[i]

        return output
    




if __name__ == "__main__":

    #run_unit_tests()
    

    solver = Solver()

    print("running tests")
    solver.solve()

