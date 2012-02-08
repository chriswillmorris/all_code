import sys


def chain(i_li):
    """
    i_li : An iterable
    return : A list with len(i_li) items.
    The first item is i_li[0]. The second item is i_li[0:2].
    The third item is i_li[0:3], etc
    """
    ret = []
    for i, v in enumerate(i_li):
        ret.append(i_li[0:i + 1])
    return ret


def _mod_options(i_prev, i_thresh):
    """
    i_prev (list) : the part of the list that has already been smoothed.
    The mod options will be based on the most recently-smoothed cell
    i_thresh (int) : the maximum valid absolute value of the distance between
    neighboring cells
    return : a list of the possible modified values
    """

    # TODO: maybe do range from max(i_prev[-1] - i_thresh, 0) to min(i_prev[-1] + i_thresh, 255)
    if i_prev:
        return [min(i_prev[-1] + i_thresh, 255), max(i_prev[-1] - i_thresh, 0)]
    else:
        return range(256)
        
    

def _insert_options(i_prev, i_next, i_thresh, i_insert_cost, i_remaining_cost):
    """
    i_prev (list): the part of the list that has already been smoothed
    i_next (int): the next item
    i_thresh (int) : the maxium valid absolute value of the distance between
    neighboring cells
    i_insert_cost (int) : the cost to insert a cell
    i_remaining_cost (int): the remaining cost left before exceeding an already
    found minimum cost
    return : a list of lists where each sublist contains a series of exclusively
    increasing or exclusively decreasing integers that go from i_prev to i_next
    """

    # Truncate the lists to ensure they don't exceed the
    # maximum cost
    max_length = i_remaining_cost // i_insert_cost

    ret = []
    if not i_prev:
        nums_1 = range(0 + i_thresh, i_next, i_thresh)
        nums_2 = range(255 - i_thresh, i_next, -i_thresh)
        ret.extend(chain(nums_1)[:max_length])
        ret.extend(chain(nums_2)[:max_length])
    elif i_prev[-1] < i_next:
        nums = range(i_prev[-1] + i_thresh, i_next, i_thresh)
        ret.extend(chain(nums)[:max_length])
    elif i_prev[-1] > i_next:
        nums = range(i_prev[-1] - i_thresh, i_next, -i_thresh)
        ret.extend(chain(nums)[:max_length])

    return ret
    

def _output(i_data, o_log_file, i_debug):
    """
    i_data : the output to be printed
    o_log_file (file) : An open file where debug text should
    be written
    i_debug (bool) : True if debug statements should be written
    """
    if o_log_file:
        o_log_file.write(i_data + '\n')
    if i_debug:
        print i_data
    

def indent(num):
    return "  " * num


def print_result(calculated_answer, expected_answer):
    if calculated_answer == expected_answer:
        print "Pass"
    else:
        print "Expected {0}, Got {1}".format(expected_answer, calculated_answer)
        print "Fail"


def test_smooth(tests):
    # Order of params:
    # list, prev, original cell, delete, insert, threshold, curr cost, minimum cost, indent
    for test_num in tests:
        print "Test #: {0}".format(test_num)
        if test_num == 0:
            print_result(smooth([1,1,1,1],[],True,100,100,3, 0, 300, 0), 0)
        elif test_num == 1:
            print_result(smooth([1,100,2],[],True,100,100,3, 0, 200, 0), 100)
        elif test_num == 2:
            print_result(smooth([1,100,2],[],True,50,100,3, 0, 100, 0), 50)
        elif test_num == 3:
            # Insert a 61 between the 40 and 101
            print_result(smooth([40,40,40,101,81,60],[],True,5,4,40, 0, 25, 0), 4)
        elif test_num == 4:
            print_result(smooth([1,25],[],True,100,1,4, 0, 100, 0), 5)
        else:
            print "Skipped"


def smooth_2(i_prev_list, i_curr_item, i_m):
    """
    Returns True if the absolute difference between the
    two values is less than or equal to a threshold value

    i_a : The first value
    i_b : The second value
    i_m : The threshold value

    Returns : True if the absolute difference between the
    two values is less than or equal to a threshold value

    Note: an empty list automatically causes this to
    return True
    """
    if (not i_prev_list) or (not i_curr_item):
        return True
    return abs(i_prev_list[-1] - i_curr_item) <= i_m

        
def smooth(i_array, i_prev, i_d, i_i, i_m, i_curr_cost, i_min_cost, i_indent, o_out_file, i_debug_flag, i_just_inserted=False):

    """
    Returns the minimum cost to smooth the original array
    
    i_array [in] = The array to smooth
    i_prev [in] = The previous cell
    i_d [in] = The cost to delete a cell
    i_i [in] = The cost to insert a cell
    i_m [in] = The threshold used to determine if the array is smooth
    i_curr_cost [in] = The cost that has been spent up to this point
    i_min_cost [in] = The minimum cost that has been found for
    smoothing the original array.
    o_out_file (file) : An open file where the output should
    be stored
    i_debug_flag (bool) : True if debug text should be printed
    
    """

    #raw_input()

    # The cost to smooth i_array
    min_smooth_cost = i_min_cost

    if min_smooth_cost == 0:
        # Minimum cost found
        _output("{0}Minimum cost of 0 has been found:".format(indent(i_indent)), o_out_file, i_debug_flag)
        _output("{ind}{prev}  {arr}".format(ind=indent(i_indent), prev=i_prev, arr=i_array), o_out_file, i_debug_flag)
        return min_smooth_cost, i_prev + i_array
    elif i_curr_cost >= min_smooth_cost:
        # No use searching any more since the
        # i_curr_cost will never be less than
        # the already-found min_smooth_cost
        _output("{0}curr cost >= min_smooth_cost:".format(indent(i_indent)), o_out_file, i_debug_flag)
        _output("{ind}{prev}  {arr}".format(ind=indent(i_indent), prev=i_prev, arr=i_array), o_out_file, i_debug_flag)
        return min_smooth_cost, i_prev + i_array
    elif not i_array:
        # Empty array. Nothing to smooth
        _output("{0}Empty array, min cost of {1}:".format(indent(i_indent),min(i_curr_cost, min_smooth_cost)), o_out_file, i_debug_flag)
        _output("{ind}{prev}  {arr}".format(ind=indent(i_indent), prev=i_prev, arr=i_array), o_out_file, i_debug_flag)
        return min(i_curr_cost, min_smooth_cost), i_prev + i_array
    elif (len(i_array) == 1) and smooth_2(i_prev, i_array[0], i_m):
        # Single cell is smoothable with i_prev
        _output("{0}Single-element array, min cost of {1}:".format(indent(i_indent), min(i_curr_cost, min_smooth_cost)), o_out_file, i_debug_flag)
        _output("{ind}{prev}  {arr}".format(ind=indent(i_indent), prev=i_prev, arr=i_array), o_out_file, i_debug_flag)
        return min(i_curr_cost, min_smooth_cost), i_prev + i_array
    elif (i_d == 0) or (i_i == 0) or (i_m == 0):
        # You can undoubtedly make the array smooth
        # with a cost of 0!
        # Note: this check, technically, only needs
        # to be at the top level
        _output("{0}Either deleting, inserting, or smooth threshold is 0".format(indent(i_indent)), o_out_file, i_debug_flag)
        return min(i_curr_cost, min_smooth_cost), i_prev + i_array

    _output("{0}{1}   {2} w/ cost:{3}".format(indent(i_indent), i_prev, i_array, i_curr_cost), o_out_file, i_debug_flag)

    # You might need to make an unlimited number of
    # insertions, but can make a maximum of n
    # deletions and n changes. If you make x deletions,
    # then you can make a maximum of n-x changes, since
    # changes and deletions only apply to the original
    # cells, and you can't change a cell that has been
    # deleted

    # When coming to an original cell, you can either:
    # leave it alone and proceed to the next cell
    # delete it and proceed to the next cell
    # modify it and proceed to the next cell
    # insert a new cell before k
    # f. leave k alone

    # When making a move, make sure that whatever cell
    # becomes cell_prev meets the requirements of being
    # smooth



    # Leave cell unchanged
    if smooth_2(i_prev, i_array[0], i_m):
        _output("{0}Leave cell unchanged".format(indent(i_indent)), o_out_file, i_debug_flag)
        min_smooth_cost, solution = smooth(i_array[1:], i_prev + [i_array[0]],
                             i_d, i_i, i_m,
                             i_curr_cost, min_smooth_cost, i_indent + 1, o_out_file, i_debug_flag)
    if min_smooth_cost == 0:
        # No need to check any further
        return min_smooth_cost, solution


    # Delete the cell
    _output("{0}Deleting cell {1}".format(indent(i_indent), i_array[0]), o_out_file, i_debug_flag)
    min_smooth_cost, solution = smooth(i_array[1:], i_prev,
                             i_d, i_i, i_m,
                             i_curr_cost + i_d, min_smooth_cost, i_indent + 1, o_out_file, i_debug_flag)
    if min_smooth_cost == 0:
        # No need to check any further
        return min_smooth_cost, solution


    # Change the cell's value
    mod_options = _mod_options(i_prev, i_m)
    for mod_val in mod_options:
        mod_cost = abs(i_array[0] - mod_val)
        new_cost = i_curr_cost + mod_cost
        if (mod_val != i_array[0]) and (new_cost < min_smooth_cost):
            _output("{0}Modifying cell {1} to {2}".format(indent(i_indent), i_array[0], mod_val), o_out_file, i_debug_flag)
            # Don't modify to the same value. That makes no sense.
            min_smooth_cost, solution = smooth(i_array[1:], i_prev + [mod_val],
                                     i_d, i_i, i_m,
                                     new_cost, min_smooth_cost, i_indent + 1, o_out_file, i_debug_flag)
        if min_smooth_cost == 0:
            # No need to check any further
            return min_smooth_cost, solution


    # Insert a cell
    if i_prev and not i_just_inserted:
        # At least one cell has been processed and cells were not
        # just inserted. If cells were just inserted, we don't need
        # to insert more; we need to either skip, delete, or modify
        # the current original cell. This single flag makes the
        # algorithm much faster.
        cells_to_insert = _insert_options(i_prev, i_array[0], i_m, i_i, min_smooth_cost - i_curr_cost)
        for attempt in cells_to_insert:
            # Try every set of insert options
            _output("{0}Inserting {1}".format(indent(i_indent), attempt), o_out_file, i_debug_flag)
            min_smooth_cost, solution = smooth(i_array, i_prev + attempt,
                                     i_d, i_i, i_m,
                                     i_curr_cost + (len(attempt) * i_i), min_smooth_cost, i_indent + 1, o_out_file, i_debug_flag, i_just_inserted=True)
            if min_smooth_cost == 0:
                # No need to check any further
                return min_smooth_cost, solution


    return min_smooth_cost, i_prev + i_array

    

def _solve_case(i_in_file, o_log_file, i_debug_flag):
    """
    Solves a single case

    i_in_file (file) : An open file containing the input
    data
    o_log_file (file) : An open file where log output should
    be stored
    i_debug_flag (bool) : True if debug data should be written
    """

    # Strip the newline
    first_line = i_in_file.readline().strip()
    
    # Get the parameters
    [d,i,m,n] = [int(x) for x in first_line.split(" ")]
    _output("D:{0}, I:{1}, M:{2}, N:{3}".format(d,i,m,n), o_log_file, True)

    # Strip the newline
    second_line = i_in_file.readline().strip()

    # Get the array
    array = second_line.split(" ")

    # Convert the elements from chars to ints
    array = map(lambda x: int(x), array)
    
    #print array

    # We know the cost cannot be larger than it would
    # cost to delete every cell except for one
    reasonable_min_cost = (len(array) - 1) * d

    min_cost, solution = smooth(array, [], d, i, m, 0, reasonable_min_cost, 0, o_log_file, i_debug_flag)
    return (min_cost, solution)


def process(i_in_file, o_out_file, o_log_file, i_debug_flag, i_num_cases):
    """
    i_in_file (file) : An open file containing the input
    data
    o_out_file (file) : An open file where the output should
    be stored
    o_log_file (file) : An open file where the log data should
    be stored
    i_debug_flag (bool) : True if debug statements should be
    printed
    i_num_cases (int) : The number of cases to process
    """

    # Script starts here
    t = int(i_in_file.readline())

    _output("T: {0}".format(t), o_log_file, True)

    costs = []
    for i in range(t):
        
        if i >= i_num_cases:
            break
        
        
        min_cost, solution = _solve_case(i_in_file, o_log_file, i_debug_flag)

        output_line = "Case #{0}: {1}".format(i + 1, min_cost)
        print output_line
        o_out_file.write(output_line + '\n')

        costs.append((min_cost, solution))

    return costs


if __name__ == "__main__":

    tests = []
    tests.append(0)
    tests.append(1)
    tests.append(2)
    tests.append(3)
    tests.append(4)
    #tests = range(5)
    #test_smooth(tests)


    small_file = "B-small-practice.in"
    large_file = "B-large-practice.in"
    #in_file = open(small_file)
    in_file = open(large_file)
    out_file = open("output.txt",'w')
    log_file = open("log_file.txt", 'w')

    answers_expected = []
    answers_expected.extend([4, 17, 0, 0, 0, 0, 0, 0, 0, 0])
    answers_expected.extend([1, 0, 0, 27, 0, 109, 26, 31, 0, 0])
    answers_expected.extend([0, 122, 0, 18, 62, 42, 0, 7, 28, 7])
    answers_expected.extend([2, 15, 13, 114, 37, 9, 19, 59, 96, 88])
    answers_expected.extend([48, 0, 2, 37, 10, 0, 0, 0, 36, 24])
    answers_expected.extend([0, 0, 1, 16, 0, 34, 17, 18, 12, 0])
    answers_expected.extend([58, 0, 63, 0, 90, 2, 0, 0, 136, 9])
    answers_expected.extend([131, 19, 0, 0, 136, 34, 97, 44, 96, 0])
    answers_expected.extend([0, 41, 40, 0, 33, 0, 27, 0, 68, 0])
    answers_expected.extend([0, 78, 11, 11, 0, 0, 0, 129, 22, 0])

    answers_given = process(in_file, out_file, log_file, False, len(answers_expected))

    log_file.close()
    out_file.close()
    in_file.close()

    for index, case in enumerate(zip(answers_expected, answers_given)):
        expected_cost = case[0]
        calculated_cost = case[1][0]
        if case[0] != case[1][0]:
            print("Failure at case {0}".format(index + 1))
            print("Expected cost: {0}".format(expected_cost))
            print("Calculated cost: {0}".format(calculated_cost))
            print("Calculated solution: {0}").format(case[1][1])
            break
    else:
        print("Pass")

    """
    if answers_expected == answers_given[:len(answers_expected)]:
        print("Pass")
    else:
        print("Fail")
        print answers_expected
        print answers_given
    """
