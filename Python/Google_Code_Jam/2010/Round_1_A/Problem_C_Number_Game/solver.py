import Google_Code_Jam.problem_solver as gcj_solver

# Used for testing
reload(gcj_solver)

import logger

import os
import pickle


def _is_losing_state(i_state):
    return (i_state[0] == 0) or (i_state[1] == 0)


def _generate_next_states(i_state):
    """ Generates all possible states from i_state """

    low,high = min(i_state),max(i_state)

    # This should round down
    n_subs = high / low

    # Return numbers closest to 0,
    # This will help with short-circuit evaluation
    return [(low, high - (low * i)) for i in range(n_subs,0,-1)]


def _add_state(i_state, i_list):
    i_list.add(i_state)
    i_list.add(tuple(reversed(i_state)))



class Solver(gcj_solver.ProblemSolver):

    g_winners = set()
    g_losers = set()
    
    def __init__(self):
        base_path = "C:\\Users\\cmorris\\Documents\\Projects\\github_repo\\all_code\\Python\\Google_Code_Jam\\2010\\Round_1_A\\Problem_C_Number_Game"
        
        """
        gcj_solver.ProblemSolver.__init__(
            self,
            os.path.join(base_path, "C-small-practice.in"),
            os.path.join(base_path, "C-small-practice.out"),
            True,
            o_debug_file = os.path.join(base_path, "C-small-practice.debug"))
        """

        gcj_solver.ProblemSolver.__init__(
            self,
            os.path.join(base_path, "C-large-practice.in"),
            os.path.join(base_path, "C-large-practice.out"),
            True,
            o_debug_file = os.path.join(base_path, "C-large-practice.debug"))

        self._force_printing = False
        self._debug = False

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


    def _cleanup(self):
        # Store the winners and losers in an external file.
        # They can then be loaded in next time so things
        # don't need to be recalculated
        logger.log("Writing winners and losers to disk", i_force=True, o_log_file=self._debug_file, i_debug=self._debug)       
        pickle.dump(Solver.g_winners, open("winners.bin", 'wb'))
        pickle.dump(Solver.g_losers, open("losers.bin", 'wb'))


    def _init(self):
        # Load any winners/losers that have been calculated on
        # a previous run so things don't need to be
        # recalculated
        logger.log("Loading winners and losers from disk", i_force=True, o_log_file=self._debug_file, i_debug=self._debug)

        winners_loc = 'winners.bin'
        losers_loc = 'losers.bin'

        # Get previously-discovered winners
        try:
            winners_file = open(winners_loc, 'rb')
        except IOError:
            winners_file = open(winners_loc, 'wb')
            winners_file = open(winners_loc, 'rb')
        try:
            Solver.g_winners = pickle.load(winners_file)
        except EOFError:
            Solver.g_winners = set()

        # Get previously-discovered losers
        try:
            losers_file = open(losers_loc, 'rb')
        except IOError:
            losers_file = open(losers_loc, 'wb')
            losers_file = open(losers_loc, 'rb')
        try:
            Solver.g_losers = pickle.load(losers_file)
        except EOFError:
            Solver.g_losers = set()



    def solve_case(self):
        logger.log("a1:{a1}, a2:{a2}, b1:{b1}, b2:{b2}".format(a1=self._a1, a2=self._a2, b1=self._b1, b2=self._b2), i_force=True, o_log_file=self._debug_file)

        # Test every position requested and count the number of
        # winning positions
        num_wins = 0
        for a in range(self._a1, self._a2 + 1):
            for b in range(self._b1, self._b2 + 1):
                state = (a,b)
                self._build_tree(state)
                if state in Solver.g_winners:
                    num_wins += 1
        return num_wins


    def _build_tree(self, i_orig_state):
        """
        From a given state, this builds out a list of all the
        resulting states, recording whether they are winners
        or losers, until it can be determined with certainty
        whether the given state is a winner or a loser.

        Note: The static losers and winners list is modified.
        This means that subsequent calls will not need to
        discover whether a state is a winner/loser if it was
        discovered and recorded on a previous call.
        """

        unsolved = set()
        all_generated_states_are_lost = True
        for state in _generate_next_states(i_orig_state):
            #print state

            if _is_losing_state(state):
                # The state is already lost
                output = "state already lost: {0}".format(state)
                logger.log(output, i_force=self._force_printing, o_log_file=self._debug_file, i_debug=self._debug)
                continue

            # At least one generated state isn't already lost
            all_generated_states_are_lost = False

            if state in Solver.g_losers:
                # You can force the other player to lose.
                # Add this state and its reverse
                logger.log("add W: {0}".format(i_orig_state), i_force=self._force_printing, o_log_file=self._debug_file, i_debug=self._debug)
                _add_state(i_orig_state, Solver.g_winners)

                # No need to build out state further
                return
            elif state not in Solver.g_winners:
                # Note: if state is not in the winners set,
                # neither is the reverse of state
                unsolved.add(state)

        if all_generated_states_are_lost:
            # Every generated state is already lost
            logger.log("add L: {0}".format(i_orig_state), i_force=self._force_printing, o_log_file=self._debug_file, i_debug=self._debug)
            _add_state(i_orig_state, Solver.g_losers)
            return

        if len(unsolved) == 0:
            # Every resulting state is a winner, so you can't
            # force the other player to lose
            logger.log("add L: {0}".format(i_orig_state), i_force=self._force_printing, o_log_file=self._debug_file, i_debug=self._debug)
            _add_state(i_orig_state, Solver.g_losers)
        else:
            for state2 in unsolved:
                self._build_tree(state2)
                if state2 in Solver.g_losers:
                    # You can force the other player to lose
                    logger.log("add W: {0}".format(i_orig_state), i_force=self._force_printing, o_log_file=self._debug_file, i_debug=self._debug)
                    _add_state(i_orig_state, Solver.g_winners)

                    # No need to build out state further
                    return

            if i_orig_state not in Solver.g_winners:
                # Since i_orig_state was not found to be a winner,
                # it must be a loser
                logger.log("add L: {0}".format(i_orig_state), i_force=self._force_printing, o_log_file=self._debug_file, i_debug=self._debug)
                _add_state(i_orig_state, Solver.g_losers)
                        


if __name__ == "__main__":
    solver = Solver()

    print("running tests")
    solver.solve()
    
