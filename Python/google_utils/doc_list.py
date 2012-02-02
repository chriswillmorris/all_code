import gdata.docs.data
import gdata.docs.client


def login(i_name, i_password, i_app_name):
    """
    Returns an authorized client and its cooresponding
    ClientLoginToken, given the credentials passed in
    
    i_name (string) : the email of the account to
    log in to
    i_password (string) : the password for the account
    to log in to
    i_app_name (str) : the name of the application that will
    use the login
    return : a 2-tuple where item one is the logged-in
    Document List client (gdata.docs.client.DocsClient)
    and item two is the ClientLoginToken, or None if
    logging in fails
    """

    client = gdata.docs.client.DocsClient(source='Docs List App')
    client.ssl = True  # Force all API requests through HTTPS
    client.http_client.debug = False  # Set to True for debugging HTTP requests

    try:
        auth_token = client.client_login(i_name, i_password, i_app_name)
        return client, auth_token
    except:
        return None
