from google_utils import spreadsheet
from bible import metadata

import copy

Monday = 'monday'
Tuesday = 'tuesday'
Wednesday = 'wednesday'
Thursday = 'thursday'
Friday = 'friday'
Saturday = 'saturday'
Sunday = 'sunday'
Days = [Monday,
        Tuesday,
        Wednesday,
        Thursday,
        Friday,
        Saturday,
        Sunday]

class _Day(object):
    def __init__(self,
                 i_ot_start_book = None, i_ot_start_chap = None,
                 i_ot_end_book = None, i_ot_end_chap = None,
                 i_nt_start_book = None, i_nt_start_chap = None,
                 i_nt_end_book = None, i_nt_end_chap = None):
        self.ot_start_book = i_ot_start_book
        self.ot_start_chap = i_ot_start_chap
        self.ot_end_book = i_ot_end_book
        self.ot_end_chap = i_ot_end_chap
        self.nt_start_book = i_nt_start_book
        self.nt_start_chap = i_nt_start_chap
        self.nt_end_book = i_nt_end_book
        self.nt_end_chap = i_nt_end_chap


    def __str__(self):
        return """Old Testament:{0} {1} to {2} {3}
New Testament:{4} {5} to {6} {7}""".format(
            self.ot_start_book, self.ot_start_chap,
            self.ot_end_book, self.ot_end_chap,
            self.nt_start_book, self.nt_start_chap,
            self.nt_end_book, self.nt_end_chap)

    def __repr__(self):
        return str(self)


    def __eq__(self, rhs):
        return ((self.ot_start_book == rhs.ot_start_book) and
                (self.ot_start_chap == rhs.ot_start_chap) and
                (self.ot_end_book == rhs.ot_end_book) and
                (self.ot_end_chap == rhs.ot_end_chap) and
                (self.nt_start_book == rhs.nt_start_book) and
                (self.nt_start_chap == rhs.nt_start_chap) and
                (self.nt_end_book == rhs.nt_end_book) and
                (self.nt_end_chap == rhs.nt_end_chap))


def _str_to_int(i_val):
    """
    i_val (str) : A string representing an integer.
    Note: "None" can be used to signify that it is
    not a number
    """

    if i_val == 'None':
        return None
    else:
        return int(i_val)


def _internal_day_to_external(i_day):
    """
    i_day (_Day) : The day whose form should be converted
    return : An 8-tuple where:
    item 1 is the starting Old Testament book
    item 2 is the starting Old Testament chapter
    item 3 is the ending Old Testament book
    item 4 is the ending Old Testament chapter
    items 5-8 are the same, but for the New Testament
    """
    return (i_day.ot_start_book, i_day.ot_start_chap,
            i_day.ot_end_book, i_day.ot_end_chap,
            i_day.nt_start_book, i_day.nt_start_chap,
            i_day.nt_end_book, i_day.nt_end_chap)


def _advance_internal(i_end_book, i_end_chap, i_rule):
    """
    i_end_book (str) : The book the previous day ended with
    i_end_chap (str) : The ending chapter number from the
    previous day
    i_rule (int) : The number of chapters to read
    return : A 4-tuple where item 1 is the start book,
    item 2 is the start chapter, item 3 is the end book,
    and item 4 is the end chapter. If i_end_chapter is
    not a book of the Bible, None will be returned
    """

    if i_rule == 0:
        # No chapters to read
        return (i_end_book, i_end_chap, i_end_book, i_end_chap)

    books = None
    if i_end_book in metadata.OTBooks:
        books = metadata.OTBooks
    elif i_end_book in metadata.NTBooks:
        books = metadata.NTBooks
    else:
        return None
        
    num_chaps = metadata.BooksToChapters[i_end_book]
    if i_end_chap == num_chaps:
        # The previous end book has been completely
        # read
        if books.index(i_end_book) == (len(books) - 1):
            # The last book in the testament has
            # been read
            return (i_end_book, i_end_chap, i_end_book, i_end_chap)
        else:
            next_book = books[books.index(i_end_book) + 1]
            return _advance_internal(next_book, 0, i_rule)
    elif (i_end_chap + i_rule) > num_chaps:
        # Not enough chapters left to satisfy rule
        start_book = i_end_book
        start_chap = i_end_chap + 1
        if books.index(i_end_book) == (len(books) - 1):
            # The last book in the testament has
            # been read
            return (start_book, start_chap, i_end_book, num_chaps)
        else:
            # Advance to the next book
            next_book = books[books.index(start_book) + 1]
            advanced = _advance_internal(next_book, 0, i_rule)
            return (start_book, start_chap, advanced[2], advanced[3])
    else:
        # There are enough chapters in the current book to
        # satisfy the rule
        return (i_end_book, i_end_chap + 1, i_end_book, i_end_chap + i_rule)
        

def _advance(i_day, i_rule):
    """
    i_day (Day) : The day to advance
    i_rule : a 2-tuple where the first item contains
    the number of Old Testament chapters to read and
    the second item contains the number of New
    Testament chapters to read.
    return (_Day): The advanced Day
    """
    new_ot = _advance_internal(i_day.ot_end_book, i_day.ot_end_chap, i_rule[0])
    new_nt = _advance_internal(i_day.nt_end_book, i_day.nt_end_chap, i_rule[1])

    day = _Day()
    day.ot_start_book = new_ot[0]
    day.ot_start_chap = new_ot[1]
    day.ot_end_book = new_ot[2]
    day.ot_end_chap = new_ot[3]
    day.nt_start_book = new_nt[0]
    day.nt_start_chap = new_nt[1]
    day.nt_end_book = new_nt[2]
    day.nt_end_chap = new_nt[3]
    return day


def _get_day_schedule(i_row):
    """
    i_row (gdata.spreadsheet.SpreadsheetsList) : The row from
    which the starting and ending book names and chapter
    numbers for the Old and New Testaments should be
    retrieved.
    return : An 8-tuple with the following description:
    1:  starting Old Testament book to read
    2:  starting Old Testament chapter to read
    3:  ending Old Testament book to read
    4:  ending  Old Testament chapter to read
    items 5-8 are the same, but for the New Testament
    """
    ot_start_book = i_row.custom['oldtestamentstartbook'].text
    ot_start_chap = _str_to_int(i_row.custom['oldtestamentstartchapter'].text)
    ot_end_book = i_row.custom['oldtestamentendbook'].text
    ot_end_chap = _str_to_int(i_row.custom['oldtestamentendchapter'].text)
    nt_start_book = i_row.custom['newtestamentstartbook'].text
    nt_start_chap = _str_to_int(i_row.custom['newtestamentstartchapter'].text)
    nt_end_book = i_row.custom['newtestamentendbook'].text
    nt_end_chap = _str_to_int(i_row.custom['newtestamentendchapter'].text)

    return (ot_start_book, ot_start_chap,
            ot_end_book, ot_end_chap,
            nt_start_book, nt_start_chap,
            nt_end_book, nt_end_chap)

    

def _get_num_chaps_to_read(i_row):
    """
    i_row (gdata.spreadsheet.SpreadsheetsList) : The row from
    which the number of Old Testament and New Testament
    chapters to read is retrieved
    return : A 2-tuple. Item 1 is the number of Old
    Testament chapters to read and Item 2 is the number
    of New Testament chapters to read
    """
    num_ot = _str_to_int(i_row.custom['oldtestamentchapterstoread'].text)
    num_nt = _str_to_int(i_row.custom['newtestamentchapterstoread'].text)
    return (num_ot, num_nt)


def get_rules(i_client, i_spreadsheet_key, i_worksheet_id):
    """
    Gets the rules that govern how many chapters
    from each testament to read each day
    i_client (gdata.spreadsheeet.service.SpreadsheetsService) : the already-logged-in spreadsheet
    service client
    i_spreadsheet_key (string) : the key of the
    spreadsheet that contains the Bible-reading
    schedule
    i_worksheet_id (string) : the worksheet id
    of the worksheet that contains the Bible-reading
    schedule
    return : a list with two elements. The first
    element is a 7-item tuple containing the
    amount of chapters to read in the Old
    Testament. The second element is the same,
    but for the New Testament
    """
    feed = i_client.GetListFeed(i_spreadsheet_key, i_worksheet_id)
    rules_orig = [_get_num_chaps_to_read(row) for row in feed.entry]

    rules = []
    rules.append(tuple([item[0] for item in rules_orig]))
    rules.append(tuple([item[1] for item in rules_orig]))
    return rules


def get_schedule(i_client, i_spreadsheet_key, i_worksheet_id):
    """
    Gets the rules that govern how many chapters
    from each testament to read each day
    i_client (gdata.spreadsheeet.service.SpreadsheetsService) : the already-logged-in spreadsheet
    service client
    i_spreadsheet_key (string) : the key of the
    spreadsheet that contains the Bible-reading
    schedule
    i_worksheet_id (string) : the worksheet id
    of the worksheet that contains the Bible-reading
    schedule
    return : a 7-tuple. The 1st item represents Monday,
    the 2nd item represents Tuesday, etc, all the way up
    to Sunday.
    Each day is an 8-tuple with the following description:
    1:  starting Old Testament book to read
    2:  starting Old Testament chapter to read
    3:  ending Old Testament book to read
    4:  ending  Old Testament chapter to read
    items 5-8 are the same, but for the New Testament
    """
    feed = i_client.GetListFeed(i_spreadsheet_key, i_worksheet_id)
    schedule = [_get_day_schedule(row) for row in feed.entry]
    return schedule


def _compare(i_expected, i_given, i_test_num):
    """
    i_expected : The expected value
    i_given : The given value
    i_test_num : The number of the test
    """
    
    if i_expected == i_given:
        print "Test {0} : Pass".format(i_test_num)
    else:
        print "Test {0} : Fail".format(i_test_num)
        print "Expected: {0}".format(i_expected)
        print "Given: {0}".format(i_given)



def test():
    #update_schedule()
    test_num = 1

    ret = _advance_internal(metadata.Genesis, 23, 4)
    expected = (metadata.Genesis, 24, metadata.Genesis, 27)
    _compare(expected, ret, test_num)
    test_num += 1

    ret = _advance_internal(metadata.SongOfSolomon, 7, 4)
    expected = (metadata.SongOfSolomon, 8, metadata.Isaiah, 4)
    _compare(expected, ret, test_num)
    test_num += 1

    ret = _advance_internal(metadata.SongOfSolomon, 4, 4)
    expected = (metadata.SongOfSolomon, 5, metadata.SongOfSolomon, 8)
    _compare(expected, ret, test_num)
    test_num += 1

    ret = _advance_internal(metadata.Malachi, 0, 4)
    expected = (metadata.Malachi, 1, metadata.Malachi, 4)
    _compare(expected, ret, test_num)
    test_num += 1

    ret = _advance_internal(metadata.Malachi, 2, 4)
    expected = (metadata.Malachi, 3, metadata.Malachi, 4)
    _compare(expected, ret, test_num)
    test_num += 1

    
    rules = [(0, 4, 0, 4, 0, 4, 2),
             (3, 0, 3, 0, 3, 0, 2)]
    schedule = [None] * 7
    schedule[6] = (None, None, metadata.SecondSamuel, 24,
                   None, None, metadata.Matthew, 16)
    ret = update_internal(schedule, rules)
    mon = _Day(metadata.SecondSamuel, 24, metadata.SecondSamuel, 24,
               metadata.Matthew, 17, metadata.Matthew, 19)
    tue = _Day(metadata.FirstKings, 1, metadata.FirstKings, 4,
               metadata.Matthew, 19, metadata.Matthew, 19)
    wed = _Day(metadata.FirstKings, 4, metadata.FirstKings, 4,
               metadata.Matthew, 20, metadata.Matthew, 22)
    thur = _Day(metadata.FirstKings, 5, metadata.FirstKings, 8,
                metadata.Matthew, 22, metadata.Matthew, 22)
    fri = _Day(metadata.FirstKings, 8, metadata.FirstKings, 8,
               metadata.Matthew, 23, metadata.Matthew, 25)
    sat = _Day(metadata.FirstKings, 9, metadata.FirstKings, 12,
               metadata.Matthew, 25, metadata.Matthew, 25)
    sun = _Day(metadata.FirstKings, 13, metadata.FirstKings, 14,
               metadata.Matthew, 26, metadata.Matthew, 27)
    expected = [mon, tue, wed, thur, fri, sat, sun]
    _compare(expected, ret, test_num)
    test_num += 1


    rules = [(0, 4, 0, 4, 0, 4, 2),
             (3, 0, 3, 0, 3, 0, 2)]
    schedule = [None] * 7
    schedule[6] = (None, None, metadata.Joel, 2,
                   None, None, metadata.Hebrews, 11)
    ret = update_internal(schedule, rules)
    mon = _Day(metadata.Joel, 2, metadata.Joel, 2,
               metadata.Hebrews, 12, metadata.James, 3)
    tue = _Day(metadata.Joel, 3, metadata.Amos, 4,
               metadata.James, 3, metadata.James, 3)
    wed = _Day(metadata.Amos, 4, metadata.Amos, 4,
               metadata.James, 4, metadata.FirstPeter, 3)
    thur = _Day(metadata.Amos, 5, metadata.Amos, 8,
                metadata.FirstPeter, 3, metadata.FirstPeter, 3)
    fri = _Day(metadata.Amos, 8, metadata.Amos, 8,
               metadata.FirstPeter, 4, metadata.SecondPeter, 3)
    sat = _Day(metadata.Amos, 9, metadata.Jonah, 4,
               metadata.SecondPeter, 3, metadata.SecondPeter, 3)
    sun = _Day(metadata.Micah, 1, metadata.Micah, 2,
               metadata.FirstJohn, 1, metadata.FirstJohn, 2)
    expected = [mon, tue, wed, thur, fri, sat, sun]
    _compare(expected, ret, test_num)
    test_num += 1
    


def update_internal(i_schedule, i_rules):
    """
    i_schedule : a 7-tuple. The 1st item represents Monday,
    the 2nd item represents Tuesday, etc, all the way up
    to Sunday.
    Each day is an 8-tuple with the following description:
    1:  starting Old Testament book to read
    2:  starting Old Testament chapter to read
    3:  ending Old Testament book to read
    4:  ending  Old Testament chapter to read
    items 5-8 are the same, but for the New Testament
    i_rules : a list with two elements. The first
    element is a 7-item tuple containing the
    amount of chapters to read in the Old
    Testament. The second element is the same,
    but for the New Testament
    return : The updated schedule as a7-tuple. The 1st item represents Monday,
    the 2nd item represents Tuesday, etc, all the way up
    to Sunday.
    Each day is an 8-tuple with the following description:
    1:  starting Old Testament book to read
    2:  starting Old Testament chapter to read
    3:  ending Old Testament book to read
    4:  ending  Old Testament chapter to read
    items 5-8 are the same, but for the New Testament
    """

    prev_day = _Day()
    prev_day.ot_end_book = i_schedule[6][2]
    prev_day.ot_end_chap = i_schedule[6][3]
    prev_day.nt_end_book = i_schedule[6][6]
    prev_day.nt_end_chap = i_schedule[6][7]
    #print prev_day

    new_sched = []

    for day_name, rule in zip(Days, zip(i_rules[0], i_rules[1])):
        day = _advance(prev_day, rule)
        new_sched.append(copy.copy(day))
        prev_day = day

    return [_internal_day_to_external(day) for day in new_sched]

    
def set_schedule(i_client, i_spreadsheet_key, i_worksheet_id, i_schedule):
    """
    Stores the Bible-reading schedule in the Google doc
    i_client (gdata.spreadsheeet.service.SpreadsheetsService) :
    the already-logged-in spreadsheet service client
    i_spreadsheet_key (string) : the key of the
    spreadsheet that contains the Bible-reading
    schedule
    i_worksheet_id (string) : the worksheet id
    of the worksheet that contains the Bible-reading
    schedule
    i_schedule : a 7-tuple. The 1st item represents Monday,
    the 2nd item represents Tuesday, etc, all the way up
    to Sunday.
    Each day is an 8-tuple with the following description:
    1:  starting Old Testament book to read
    2:  starting Old Testament chapter to read
    3:  ending Old Testament book to read
    4:  ending  Old Testament chapter to read
    items 5-8 are the same, but for the New Testament
    """
    # 1-base index for rows and columns
    for k, day in enumerate(i_schedule):
        col_index_and_value = [(g+4, str(entry)) for g, entry in enumerate(day)]
        for (col_index, value) in col_index_and_value:
            i_client.UpdateCell(k+2, col_index, value, i_spreadsheet_key, i_worksheet_id)


if __name__ == "__main__":
    test()
