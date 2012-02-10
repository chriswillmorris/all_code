class ProblemSolver(object):
    def __init__(self):
        pass


    def solve(self, i_in_file, o_out_file, o_debug_file, i_expected_answers):
        """
        i_in_file (str) : the name of the input file
        o_out_file (str) : the name of the file where
        the output will be written
        o_debug_file (str) : the name of the file where
        the debug information will be written
        i_expected_answers (iterable) : an iterable
        that contains the list of expected answers to
        compare against
        """

        in_file = open(i_in_file, 'r')

        num_cases = int(in_file.readline())

        print num_cases

        num_expected_answers = len(i_expected_answers)

        in_file.close()
