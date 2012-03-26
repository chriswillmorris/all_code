import Google_Code_Jam.problem_solver as gcj_solver

# Used for testing
reload(gcj_solver)

import logger

import os



def _get_first_dir(i_path):
    """
    Returns the first directory in a path

    i_path (str): either empty or it is a '/'
    followed by a directory name followed by
    an optional path (which meets the same
    criteria as i_path)
    return (str): the first directory in the
    path, or NULL if the path is empty or if
    the input is malformed
    """

    # Validate input
    if (not i_path) or (i_path[0] != '/'):
        return None

    if len(i_path) == 1:
        return None

    second_slash_pos = i_path.find('/', 1)
    if second_slash_pos == -1:
        return i_path[1:]

    return i_path[1:second_slash_pos]


def _num_dirs(i_path):
    """
    Returns the number of directories listed
    in a path
    
    i_path (str): same desc as for get_first_dir
    return (int): the number of directories
    listed in the path, or None if the input
    is malformed
    """

    # Validate input
    if (not i_path) or (i_path[0] != '/'):
        return None

    if len(i_path) == 1:
        return None

    # Remove trailing forward slashes
    stripped_path = i_path.rstrip('/')
    
    return stripped_path.count('/')



class Node(object):
    def __init__(self, i_name):
        """
        i_name (str): the name of the directory
        this Node represents
        """

        # The directory this Node represents
        self._dir = i_name

        # This node's children
        self._children = []


    def dir_name(self):
        return self._dir


    def add_child(self, i_child):
        """
        i_child (Node): The chld to add
        """

        self._children.append(i_child)


    def children(self):
        return self._children


def _print_tree(i_node, i_indent):
    """
    Prints the directory names of a tree
    of Nodes

    i_node (Node): The root of the Node tree
    i_indent (int): The amount to indent
    when printing the directory name
    """

    print (' ' * i_indent) + i_node.dir_name()

    [_print_tree(node, i_indent + 1) for node in i_node.children()]


def _add_path(i_node, i_path):
    """
    Adds a path (if necessary) to the directory
    structure and returns the number of new
    directories needed to do this

    i_node (Node): the head of the directory
    structure
    i_path (str): Same specifications as in
    _num_dirs(...)
    return (int): The number of directories that
    need to be added to i_node to make sure
    i_path exists on it
    """

    cur_dir = _get_first_dir(i_path)

    # Validate input
    if not cur_dir:
        return 0
    
    for node in i_node.children():
        if node.dir_name() == cur_dir:
            # The top-level directory in cur_dir
            # was found. Go one level deeper
            return _add_path(node, i_path[len(cur_dir) + 1:])
    else:
        # The top-level directory in cur_dir
        # was not found. The entire path needs
        # to be created

        path = i_path
        prev_node = i_node

        while path and (path[0] == '/') and (len(path) > 1):

            second_slash_pos = path.find('/', 1)
            if second_slash_pos == -1:
                # The last directory in the path
                node = Node(path[1:])
                path = ""
            else:
                node = Node(path[1:second_slash_pos])
                path = path[second_slash_pos:]

            prev_node.add_child(node)
            prev_node = node
        
        return _num_dirs(i_path)


def run_unit_tests():
    """
    Runs all the unit tests
    """

    assert(_get_first_dir("abc") == None)
    assert(_get_first_dir("/abc") == "abc")
    assert(_get_first_dir("/abc/") == "abc")
    assert(_get_first_dir("/abc/def") == "abc")
    assert(_get_first_dir("/") == None)
    assert(_get_first_dir("") == None)

    assert(_num_dirs("") == None)
    assert(_num_dirs("/") == None)
    assert(_num_dirs("/abc") == 1)
    assert(_num_dirs("/abc/") == 1)
    assert(_num_dirs("/abc/def") == 2)
    assert(_num_dirs("/abc/def/") == 2)
    assert(_num_dirs("/abc/def/ghi") == 3)

    node = Node("abc")
    n2 = Node("def")
    n3 = Node("ghi")
    n4 = Node("jkl")
    n5 = Node("mno")
    n4.add_child(n5)
    node.add_child(n2)
    node.add_child(n4)
    n5.add_child(n3)
    _print_tree(node, 0)


    root = Node("root")
    assert(_add_path(root, "/abc") == 1)
    assert(_add_path(root, "/ced/s/lkj") == 3)
    assert(_add_path(root, "/ced/bloy") == 1)
    assert(_add_path(root, "/ced/s/wer") == 1)
    _print_tree(root, 0)
    
    print "All tests passed"




class Solver(gcj_solver.ProblemSolver):

    
    def __init__(self):
        base_path = "C:\\Users\\cmorris\\Documents\\Projects\\github_repo\\all_code\\Python\\Google_Code_Jam\\2010\\Round_1_B\\Problem_A_File_Fix_It"
        

        """
        gcj_solver.ProblemSolver.__init__(
            self,
            os.path.join(base_path, "A-small-practice.in"),
            os.path.join(base_path, "A-small-practice.out"),
            True,
            o_debug_file = os.path.join(base_path, "A-small-practice.debug"))
        """



        gcj_solver.ProblemSolver.__init__(
            self,
            os.path.join(base_path, "A-large-practice.in"),
            os.path.join(base_path, "A-large-practice.out"),
            True,
            o_debug_file = os.path.join(base_path, "A-large-practice.debug"))


        self._force_printing = False
        self._debug = False

        # Problem parameters
        self._n = None
        self._m = None
        self._input_dirs = []
        self._dirs_to_create = []

                       

    def get_case_input(self):
        """
        See base class
        """

        self._reset_input_vars()


        first_line = self._in_file.readline().strip()
        (self._n, self._m) = [int(x) for x in first_line.split(" ")]
        for i in range(self._n):
            self._input_dirs.append(self._in_file.readline().strip())
        for i in range(self._m):
            self._dirs_to_create.append(self._in_file.readline().strip())


    def _reset_input_vars(self):
        # See base documentation
        self._input_dirs = []
        self._dirs_to_create = []


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
        logger.log("n:{n}, m:{m}, existing dirs:{existing_dirs}, dirs to create:{dirs_to_create}".format(n=self._n, m=self._m, existing_dirs=self._input_dirs, dirs_to_create=self._dirs_to_create), i_force=True, o_log_file=self._debug_file)

        root = Node("root")
        for input_dir in self._input_dirs:
            _add_path(root, input_dir)

        num_dirs_created = 0
        for dir_to_create in self._dirs_to_create:
            num_dirs_created += _add_path(root, dir_to_create)

        return num_dirs_created





if __name__ == "__main__":

    #run_unit_tests()

    solver = Solver()

    print("running tests")
    solver.solve()
