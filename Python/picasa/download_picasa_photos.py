#!/usr/bin/python

import google_utils.picasa
import logger

import os
import sys
import urllib
import urllib2

def download_file(i_url, i_dir_name, o_log_file):
    """
    i_url (str) : The url where the file exists at
    i_dir_name (str) : The directory where the file should
    be downloaded to
    o_log_file (file) : An opened file where logging output
    should go. Or None if there is no such file
    """

    # Download the data at URL to the current directory

    # The basename is everything after the last '/'
    prefix = i_url[0 : i_url.rindex('/') + 1]
    basename = i_url[i_url.rindex('/') + 1:]

    # Get the download link
    url = prefix + 'd/' + basename
    #url = i_url.replace(basename, "d/"+basename)
    #print "download url: ",url

    #filename = dir_name + "/" + basename
    filename = os.path.join(i_dir_name, basename)
    if not os.path.isfile(filename):
        logger.log("downloading {0} into {1}".format(url, filename), True, o_log_file)
        try:
            f_name, headers = urllib.urlretrieve(url, filename)
        except:
            # Try to 'sudo' this script. Then it might work
            msg = "Exception thrown when attempting photo download!"
            logger.log(msg, True, o_log_file)
            logger.log(sys.exc_info(), True, o_log_file)


def download_photos(i_username, i_password, i_dir):
    """
    i_username - username
    i_password - password
    i_dir - directory to put photos in
    """

    log_file = None
    log_file = open('download_photos_log.txt','w')

    # Log in
    client = google_utils.picasa.login(i_username, i_password)
    if not client:
        logger.log("Picasa login failed", True, log_file)
        return

    # Get list of photo albums
    albums = client.GetUserFeed()
    for album in albums.entry:
        #print 'title: {0}, number of photos: {1}, id: {2}'.format(
        #    album.title.text,album.numphotos.text, album.gphoto_id.text)


        # Make the directory to store the photos in this album

        # In the album title:
        # Remove all apostrophes and replace 'w/' with 'with'
        # and replace '/' with '_'
        album_title = album.title.text.replace('/','_')
        album_title = album_title.replace("'","")
        album_title = album_title.replace('w/','with')

        album_dir = os.path.join(i_dir, album_title)

        if not os.path.isdir(album_dir) :
            # Directory does not exist. Make it
            logger.log ("making directory at {0}".format(album_dir), True, log_file)
            os.mkdir(album_dir)

        # Replace api with base to only get the public photos
        feed_string = '/data/feed/base/user/default/albumid/{0}?kind=photo'.format(album.gphoto_id.text)
        photos = client.GetFeed(feed_string)

        # Download the photos into the specified directory
        try:
            for photo in photos.entry:
                #print 'Photo title:',photo.title.text
                #print 'Photo Content Source:',photo.content.src
                #print type(photo.content.src)
                download_file(photo.content.src, album_dir, log_file)
        except:
            msg = "Exception thrown when attempting photo download\n"
            msg += str(sys.exc_info())
            logger.log(msg, True, log_file)

    if log_file:
        log_file.close()


if __name__ == '__main__':
    """
    Usage: DownloadPicasaPhotos <username> <password> <dir to place photos in>
    Example: DownloadPicasaPhotos bob myPa55w0rd /home/bob/Photos/
    """

    print "Starting to download Picasa photos"
    main(sys.argv[1], sys.argv[2], sys.argv[3])
    print "Done dowloading Picasa photos"
