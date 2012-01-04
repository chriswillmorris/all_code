import gdata.spreadsheet.service

def login(i_name, i_password):
    """
    i_name (string) : the email of the account to
    log in to
    i_password (string) : the password for the account
    to log in to
    return : the logged-in spreadsheet service client  (gdata.spreadsheeet.service.SpreadsheetsService)
    or None if logging in fails
    """

    client = gdata.spreadsheet.service.SpreadsheetsService()
    client.email = i_name
    client.password = i_password
    client.source = 'Chris Morris\' Bible Reading Schedule Updater'
    try:
        client.ProgrammaticLogin()
    except:
        return None
    return client


def get_spreadsheet_key(i_client, i_name):
    """
    i_client (gdata.spreadsheeet.service.SpreadsheetsService): the already-logged-in spreadsheet
    service client
    i_name (string) : the name of the spreadsheet
    whose key should be retrieved
    return : the key of the indicated spreadsheet
    or None if this spreadsheet is not found
    """

    feed = i_client.GetSpreadsheetsFeed()
    key = None
    for entry in feed.entry:
        if entry.title.text == i_name:
            key = entry.id.text.rsplit('/',1)[1]
            return key
    return key


def get_worksheet_id(i_client, i_spreadsheet_key, i_num):
    """
    i_client (gdata.spreadsheeet.service.SpreadsheetsService) : the already-logged-in spreadsheet
    service client
    i_spreadsheet_key (string) : the key of the
    spreadsheet whose worksheet you want to retrieve
    i_num (integer) : the 0-based index signalling
    which worksheet's key to retrieve
    return : the id of the indicated worksheet
    or None if this worksheet is not found
    """
    feed = i_client.GetWorksheetsFeed(i_spreadsheet_key)

    if i_num >= len(feed.entry):
        return None

    worksheet_id = feed.entry[i_num].id.text.rsplit('/',1)[1]

    return worksheet_id


def get_credentials(i_username, i_password, i_spreadsheet_name, i_worksheet_index):
    """
    i_username (str) : The google username to be used when retrieving
    the Bible reading schedule
    i_username (str) : The google password to be used when retrieving
    the Bible reading schedule
    i_spreadsheet_name (str) : The name of the spreadsheet
    whose credentials should be retrieved
    i_worksheet_index (int) : The 0-based index of the
    worksheet to retrieve
    return : the gdata.spreadsheeet.service.SpreadsheetsService client, the spreadsheet key, and the spreadsheet
    id
    """
    client = login(i_username, i_password)
    if not client:
        print "Spreadsheet client retrieval failed"
        return
    
    key = get_spreadsheet_key(client, i_spreadsheet_name)
    if not key:
        print "Spreadsheet key retrieval failed"
        return
    
    id = get_worksheet_id(client, key, i_worksheet_index)
    if not id:
        print "Worksheet id retrieval failed"
        return

    return (client, key, id)
