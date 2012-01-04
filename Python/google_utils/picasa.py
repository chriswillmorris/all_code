import gdata.photos.service

def login(i_name, i_password):
    """
    i_name (string) : the email of the account to
    log in to
    i_password (string) : the password for the account
    to log in to
    return : the logged-in picasa service client  (gdata.photos.service.PhotosService)
    or None if logging in fails
    """

    client = gdata.photos.service.PhotosService()
    client.email = i_name
    client.password = i_password
    client.source = 'Picasa Program'
    try:
        client.ProgrammaticLogin()
    except:
        return None
    return client
