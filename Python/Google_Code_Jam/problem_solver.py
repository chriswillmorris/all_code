import logger

import os



class ProblemSolver(object):

    def __init__(self, i_base_path_name, i_base_file_name, i_debug, i_force_printing):
        assert i_base_path_name
        assert i_base_file_name
        incomplete_file_name = os.path.join(i_base_path_name, i_base_file_name)

        self._in_file = open(incomplete_file_name + '.in', 'r')
        self._out_file = open(incomplete_file_name + '.out', 'w')
        self._debug_file = open(incomplete_file_name + '.debug', 'w')

        self._debug = i_debug

        self._force_printing = i_force_printing


    def solve(self, i_expected_answers=None):
        """
        Solves the supplies problems and compares them
        to a set of expected answers

        i_expected_answers (iterable) : an iterable
        that contains the list of expected answers to
        compare against
        """

        num_cases = int(self._in_file.readline())
        
        logger.log("{num} cases".format(num= num_cases), self._debug, self._debug_file)

        num_expected_answers = len(i_expected_answers) if i_expected_answers else 0

        num_to_test = num_cases
        if (num_expected_answers > 0) and (num_expected_answers < num_cases):
            # Only use num_expected_answers if it is a
            # valid number
            num_to_test = num_expected_answers

        self._init()

        for i in range(num_to_test):
            self.get_case_input()

            # TODO: Temporary, to limit execution
            #if (i != 49):
            #if (i < 3) or (i > 6):
                #continue

            case_stmt = "Case #{case_num}: ".format(case_num=i+1) 
            logger.log(case_stmt, i_force=True, o_log_file=self._debug_file)
            self._out_file.write(case_stmt)

            output = self.solve_case()

            # Write output to a file.

            logger.log(output, i_force=True, o_log_file=self._debug_file)
            self._out_file.write(str(output) + '\n')

            if i_expected_answers:
                # Compare generated output with expected output
                if i_expected_answers[i] != output:
                    logger.log("Failed", i_force=True, o_log_file=self._debug_file)
                    logger.log("Expected: {0}".format(i_expected_answers[i]), i_force=True, o_log_file=self._debug_file)
                    logger.log("Calculated: {0}".format(output), i_force=True, o_log_file=self._debug_file)

        self._cleanup()

        self._out_file.close()
        self._in_file.close()
        if self._debug_file:
            self._debug_file.close()




    def get_case_input(self):
        """
        Populates the child class' parameters based on the
        input file.

        i_in_file (file) : An already opened file that
        points to the beginning of a test case.
        """
        pass



    def solve_case(self):
        """
        Solves a given case (this assumes the inputs for
        the case are already filled in)

        Return : A tuple of output where the first element
        is the actualy output required by the problem statement
        and the rest of the output is used for debugging
        purposes
        """
        pass


    def _cleanup(self):
        """
        Performs necessary cleanup
        """
        pass


    def _init(self):
        """
        Performs necessary initialization
        """
        pass
