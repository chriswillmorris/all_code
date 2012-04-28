import google_utils.doc_list as doc_list_util

import logger

import gdata.docs.client as doc_client
import gdata.docs.service as doc_service

import os
import shelve
import time
import urllib

_debug = True

_backup_root = '/home/chris/Desktop/docs_backup'

_config_file = os.path.join(_backup_root, '.config.bin')

_debug_file = os.path.join(_backup_root, '.backup_docs_debug.txt')

# The key that maps to the last time this script
# was run
_time_key = 'last_updated'

# The key that maps to a CollectionMap
# A CollectionMap is a map where the keys are
# resource ids and the values are full paths
# that represent the location of that
# collection/folder
_collections_key = 'collections'

# The key that maps to a NonCollectionMap
# A NonCollectionMap is a map where the keys are
# resource ids and the values are full paths
# that represent the location of that
# file
_files_key = 'files'



"""
    


    def create_collection_paths(i_col, io_new_collection_map, i_new_paths_already_used, i_old_collection_map, i_old_collection_paths_    used):
      # Returns a uniqe path for the i_col collection.
      # The returned path might exist in the old map, but
      # only for the same collection.
    
      if i_col is deleted or trashed:
        return

      if i_col.id in io_new_collection_map:
        # Collection has already been created
        return io_new_collection_map[i_col.id]

      if i_col has root for parent:
        # A collection can have multiple parents, where
        # one of them is the root
        # Handle the root case
        child_disk_path = create_child_path('', i_col, io_new_paths_already_used, i_old_collection_map, i_old_collection_paths_used)
        io_new_collection_map[i_col.id].append(child_disk_path)
        io_paths_already_used.append(child_disk_path)

      # Parent collections must be created before
      # creating this collection. Create the parent
      # collections.
      # Note: this assumes that you cannot have cycles,
      # where X is the parent of Y and then, traversing
      # up the chain, you eventually come to see that Y
      # is the parent of X. I tested this in Google Docs
      # and it seems like you aren't allowed to do this.
      for parent in i_col.parents:
        parent_disk_paths = create_collection_paths(parent, io_new_collection_map, i_new_paths_already_used, i_old_collection_map, i_old_collection_paths_used)
        assert len(parent_disk_paths) > 0

        for parent_disk_path in parent_disk_paths:
            # Since returning a copy of the values could be slow, build
            # up a separate list
            child_disk_path = create_child_path(parent_disk_path, i_col, io_new_paths_already_used, i_old_collection_map, i_old_collection_paths_used)
            io_new_collection_map[i_col.id].append(child_disk_path)
            io_paths_already_used.add(child_disk_path)

      return io_new_collection_map[i_col.id]



    def create_file_names(i_file, io_new_file_map, io_new_placed_files, i_new_collection_map, i_old_file_map, i_old_placed_files):
      # This will calculate a list of unique file paths
      # for i_file, insert them into the file map and
      # file list, and return this list. The names might
      # have not yet been used in the new backup,
      # but might have been used in the old backup, but
      # only for the same file. ie. If some path pathX is
      # calculated for some file X, if pathX is already
      # used in the new map, try a differnt path name.
      # If pathX is used for
      # file X in the old map, we can use the path.
      # Otherwise, we must discard pathX and create a new
      # path.
      # Return the calculated paths to i_file

      if i_file.id in io_new_file_map:
        return io_new_file_map[i_file.id]

      io_new_file_map[i_file.id] = []
      
      if i_file has root as parent:
        child_path = create_child_path('', i_file, i_new_placed_files, i_old_file_map, i_old_placed_files
        io_new_file_map[i_file.id].append(child_path)
        io_new_placed_files.append(child_path)
      
      for parent in i_file.parents:
        parent_paths = i_new_collection_map[parent]
        for parent_path in parent_paths:
          child_path = create_child_path(parent_path, i_file, i_new_placed_files, i_old_file_map, i_old_placed_files)
          io_new_file_map[i_file.id].append(child_path)
          io_new_placed_files.append(child_path)

      return io_new_file_map[i_file.id]



   # limitation: must be able to hold all the
   # file paths in memory
   def place_file(i_file, io_new_file_map, io_new_placed_files, i_new_collection_map, io_old_file_map, io_old_placed_files):
     # Put i_file on disk. This might involve doing nothing
     # in the case that i_file is already on disk in the
     # appropriate spot. Or it might involve moving the file
     # from its old location(s) (multiple locations due
     # to having multiple parent collections) to new
     # locations because its name or its set of parent
     # collections change, or it might involve downloading
     # the file again, in the case that its contents have
     # changed
     # Note: 
     if i_file is deleted or trashed:
       don't put it on disk (it should already
       have been removed from disk in a previous step)
       return
       
     new_file_names = create_file_names(i_file, io_new_file_map, io_new_placed_files, i_new_collection_map, io_old_file_map, io_old_placed_files)
     if file is new:
       # file paths are guaranteed to be unused by
       # both the old set of files and the set of
       # new files that have already been put on
       # disk
       for name in new_file_names:
         _download_file(i_file.url, name)
         io_new_placed_files.append(name)
         io_new_file_map[i_file.id].append(name)
     elif file's contents have changed:
       for name in new_file_names:
         _download_file(i_file.url, name)
         # Note: it doesn't matter if the location is the same
         as it was in the old file map
         io_new_placed_files.append(name)
         io_new_file_map[i_file.id].append(name)
     else:
       # File is not new and its contents haven't changed
       for name in new_file_names:
         if name in io_old_file_map[i_file.id]:
           # Nothing has changed about the file
         else:
           # Name change
           _download_file(i_file.url, name)

         io_new_placed_files.append(name)
         io_new_file_map[i_file.id].append(name)

     # Remove all artifacts. These are created because,
     # when a file moves, we don't erase its previous
     # location until this point.
     # Remove the artifact entries from the old map and
     # old file list. Otherwise,
     # they will take up space and make it more
     # difficult to find unique names for new files
     # that need to be placed, in the future
     for old_name in io_old_file_map[i_file.id]:
       if old_name not in io_new_placed_files:
         # Remove the artifact; it existed in the old
         # file map but shouldn't exist anymore
         try:
            os.remove(old_name)
         except OSError:
            output = "Attempted to delete a file that was expected "
            output += "to exist, but doesn't: {0}".format(old_name)
            logger.log(output, i_debug=_debug, i_force=True)

         io_old_placed_files.remove(old_name)

     del io_old_file_map[i_file.id]
"""







def _create_child_path(i_parent_path, i_child, i_new_paths_already_used, i_old_child_map, i_old_paths_used_for_obj):
    """
    Returns a unique path for the child object.
    The unique path is guaranteed to not already exist
    in i_new_paths_already_used. It could exist in
    i_old_paths_used_for_obj, but only if this path
    is used for the same object in the old map


    i_parent_path (str) : The already-guaranteed-to-be-unique
    path of the parent if i_child
    i_child (file or collection) : The object to create a
    unique path for
    i_new_paths-already_used (collection of strings) : the
    paths that have already been used in the new gdocs backup
    i_old_child_map (maps object id to collection of strings) :
    contains the old collections of paths used for i_child
    i_old_paths_used_for_obj (collection of strings) : the
    paths that were used in the old gdocs backup
    """

    attempt = os.join(i_parent_path, i_child.filename)

    # Keep appending a string until the path is unique or the path
    # is found to have not changed since the last backup
    while attempt in i_new_paths_already_used or (attempt in i_old_paths_for_obj and attempt not in i_old_child_map[i_child.resource_id]):
        attempt += '__uniq__'
    return attempt




def _download_file(i_url, i_path, o_log_file=None):
    """
    Download a file to a certain path

    i_url (str) : The url to the file to download
    i_path (str) : The path to download the url to
    """
    msg = "Attempting to download {url} to {path}".format(url=i_url, path=i_path)
    logger.log(msg, i_debug=True, o_log_file=o_log_file)

    if os.path.isfile(i_path):
        output = "{path} was expected to be non-existent".format(path=i_path)
        output += " but it does exist. Skipping download."
        logger.log(output, i_debug=_debug, o_log_file=o_log_file, i_force=True)
        return False

    try:
        f_name, headers = urllib.urlretrieve(i_url, i_path)
    except:
        # Try to 'sudo' this script. Then it might work
        msg = "Exception thrown when attempting file download with url: {0} and file path: {1}".format(i_url,i_path)
        logger.log(msg, i_debug=True, o_log_file=o_log_file)
        logger.log(sys.exc_info(), i_debug=True, o_log_file=o_log_file)
        return False

    return True
       


def _remove_file(i_id, io_file_map):
    """
    Removes a file from disk and from the file map

    i_id : The resource id of the file to remove
    io_file_map : The file map where the file's
    path can be found
    Return : The list of file names that correspond
    to io_file_map[i_id] that were not found on disk
    """

    # Remove from disk
    failed_removals = []
    for path in io_file_map[i_id]:
        try:
            os.remove(path)
        except OSError:
            output = "Attempted to delete a file that was expected "
            output += "to exist, but doesn't: {0}".format(path)
            logger.log(output, i_debug=_debug, i_force=True)
            failed_removals.append(path)

    # Remove from database
    del io_file_map[i_id]

    return failed_removals
            


    


def main():
    logger.log("Preparing to back up Google documents", i_debug=True)

    """
    last_time = last time the docs were backed up.

    For every resource id in the database file
    that has been deleted or
    trashed on Google docs, remove it from disk.

    Build up a list of unique paths for all gdocs
    collections.
    # This handles new, deleted, trashed,
    # and already-existing collections.
    # Note: this will fail if the list of
    # collection paths cannot fit in memory
    new_collection_map = {}
    new_collection_paths_already_used = []
    for coll in collections on gdocs:
      create_collection_paths(coll, new_collection_map, new_collection_paths_already_used, old_collection_map, old_collection_paths_already_used)


    # Create a list of file locations used before the
    # backup
    old_placed_files = []
    for paths_for_file in old_file_map.values():
      old_placed_files.extend(paths_for_file)

    new_file_map = {}
    new_placed_files = []

    for file in files on gdocs:
      place_file(file, new_file_map, new_placed_files, new_collection_map, old_file_map, old_placed_files)



    Store the updated timestamp.
    """

    # Try opening debug file

    try:
        debug_file = open(_debug_file, 'w')
    except:
        output = "Failed to open the debug file at {0}".format(_debug_file)
        logger.log(output, i_debug=_debug, i_force=True)
        debug_file = None

    output = "Preparing to backup Google Docs."
    logger.log(output, i_debug=_debug, i_force=True)

    # Get the time this backup started to process
    start_time = time.localtime()
    output = "Time this backup started: {0}".format(start_time)
    logger.log(output, i_debug=_debug, o_log_file=debug_file, i_force=True)

    output = "Opening config file at {0}".format(_config_file)
    logger.log(output, i_debug=_debug, o_log_file=debug_file, i_force=False)
    try:
        config_map = shelve.open(_config_file)
    except:
        output = "Failed to open the config file at {0}".format(_config_file)
        logger.log(output, i_debug=_debug, i_force=True)
        return
    
    # Get the time the last backup was performed
    output = "Getting the time of the last backup."
    logger.log(output, i_debug=_debug, i_force=True)
    prev_time = config_map.get(_time_key)
    if not prev_time:
        # The script has never been run. Set time
        # to be from 1970, before Google Docs
        # ever existed. This ensures ALL data
        # will be synced
        output = "First time script has been run. "
        output += "Downloading all documents."
        logger.log(output, i_debug=_debug, i_force=True)
        prev_time = time.struct_time((
        1970, # year
        1, # month
        1, # day
        0, # hour
        0, # minute
        0, # second
        -1, # doesn't matter
        -1, # doesn't matter
        0, # doesn't matter
        ))
        # The remaining attributes in time.struct_time
        # don't matter
    output = "Time of last backup: {0}".format(prev_time)
    logger.log(output, i_debug=_debug, o_log_file=debug_file)

    #client,token = doc_list_util.login('myname@gmail.com', 'mypassword', 'my app')
    # TODO the meat of the algorithm
    old_collection_map = config_map.get(_collections_key, dict())
    old_file_map = config_map.get(_files_key, dict())


    #doc_query = doc_service.DocumentQuery()
    #doc_query['show_collections'] = 'true'
    #query_uri = doc_query.ToUri()
    clquery = doc_client.DocsQuery(show_collections='true', show_root='true')
    client,token = doc_list_util.login('myname', 'mypassword', 'blah')
    #print query_uri
    # maybe pass in query_uri
    feed = client.GetAllResources(show_root=True, q=clquery)
    # /feeds/documents/private/full?show_collections=True

    #for item in feed:
        #print "ha"

    """
    For every resource id in the database file
    that has been deleted or
    trashed on Google docs, remove it from disk
    """
    output = "Removing all deleted or trashed docs from "
    output += "disk"
    logger.log(output, i_debug=_debug, i_force=True)

    #files_on_gdocs = client.GetAllResources(show_root=True)

    # This is very slow because it does a full search
    # of the gdocs ids for every single id in the map
    for id in old_file_map.keys():
        for _item in feed:
            if (id == _file.resource_id):
                if _item.deleted or _item.IsTrashed():
                    # File has been deleted or trashed on gdocs

                    output = "{0} has been deleted or trashed on gdocs".format(old_file_map[id])
                    logger.log(output, i_debug=_debug, i_force=True)

                    _remove_file(id, old_file_map)
                    break
            else:
                output = "{0} has not been deleted or trashed on gdocs".format(old_file_map[id])
                logger.log(output, i_debug=_debug, i_force=True)
        else:
            # File is no longer on gdocs
            output = "{0} is no longer on gdocs".format(old_file_map[id])
            logger.log(output, i_debug=_debug, i_force=True)

            _remove_file(id, old_file_map)


    """
    For every collection in the database, if its path has
    changed in gdocs, update its path in the database
    and move the file to the new path (create the new
    path if necessary)
    """
    """
    for id in old_collection_map.keys():

        # TODO
        if old_collection_map[id].parents == parent collections on gdocs for id:
            # The 
            continue
        gdocs_path = get_
        disk_path_from_gdocs = _create_disk_path(gdocs_path)

        current_collection_path = old_file_map[id]

        if disk_path_from_gdocs == current_disk_path
        
        pass
    """
        

    

    # Store the updated resource id maps
    output = "Storing the updated resource id maps."
    logger.log(output, i_debug=_debug, i_force=True)
    config_map[_files_key] = new_file_map
    config_map[_collections_key] = new_collection_map

    # Store the updated time
    output = "Storing the updated time."
    logger.log(output, i_debug=_debug, i_force=True)
    config_map[_time_key] = start_time

    config_map.close()

    if debug_file:
        debug_file.close()


def test_remove_file():
    print("testing remove file")
    name1 = '/home/chris/Desktop/sandbox/test1.tst'
    name2 = '/home/chris/Desktop/sandbox/test2.tst'
    names = [name1, name2]

    # Make sure that, initially, the file names don't exist
    for name in names:
        try:
            os.remove(name)
        except OSError:
            # File already doesn't exist. Not a problem
            pass

    # Set up database
    resource_id = 1
    database = { resource_id : names }

    # Since the file names don't exist, this should
    # return all the file names (because they couldn't
    # be deleted)
    assert names == _remove_file(resource_id, database)

    # Item should be removed from database
    assert False == bool(database)

    # Create one of the two files
    open(name1, 'w')

    database = { resource_id : names }

    # Since name2 does not exist, it should be
    # returned (because it couldn't be deleted)
    assert [name2] == _remove_file(resource_id, database)

    # Item should be removed from database
    assert False == bool(database)


    # Create one of the two files
    open(name1, 'w')
    open(name2, 'w')

    database = { resource_id : names }

    # Since name2 does not exist, it should be
    # returned (because it couldn't be deleted)
    assert [] == _remove_file(resource_id, database)

    # Item should be removed from database
    assert False == bool(database)

    print("Done testing remove file")


def test_download_file():
    print("Testing download_file")
    name1 = '/home/chris/Desktop/sandbox/test1.tst'
    name2 = '/home/chris/Desktop/sandbox/test2.tst'
    names = [name1, name2]
    good_url = 'http://www.draconika.com/img/green-dragon.jpg'
    bad_url = 'http:skjdfljsdkfj'
    urls = [good_url, bad_url]    

    # Make sure that, initially, the file names don't exist
    for name in names:
        try:
            os.remove(name)
        except OSError:
            # File already doesn't exist. Not a problem
            pass

    # Valid url and file doesn't exist
    assert True == _download_file(good_url, name1)

    # Invalid url
    assert False == _download_file(bad_url, name2)

    # Create one of the two files
    open(name1, 'w')

    # File already exists!
    assert False == _download_file(good_url, name1)

    print("Done testing download_file")


def test_create_child_path():

    print("Testing create child path")


    #(i_parent_path, i_child, i_new_paths_already_used, i_old_child_map, i_old_paths_used_for_obj):


    # Populate the old map

    # Populate the new map

    # Create the parent

    # Create a child that will have a clashing filename


    # Create a child that will not have a clashing filename

    print("Done testing create child path")






def sample_test():

    print "Testing sample test"

    clquery = doc_client.DocsQuery(show_collections='true', show_root='true')
    client,token = doc_list_util.login('myname', 'mypassword', 'blah')
    #print query_uri
    # maybe pass in query_uri
    feed = client.GetAllResources(show_root=True, q=clquery)

    item0 = feed[0]

    labels0 = item0.GetLabels()
    print "Labels: {0}".format(labels0)
    type0 = item0.GetResourceType()
    print "Resource Type: {0}".format(type0)
    collections0 = item0.InCollections()
    print "Collections: {0}".format(collections0)
    isTrashed0 = item0.IsTrashed()
    print "Is Trashed: {0}".format(isTrashed0)
    deleted0 = item0.deleted
    print "Is Deleted: {0}".format(deleted0)
    filename0 = item0.filename
    print "Filename: {0}".format(filename0)
    id0 = item0.id
    print "ID: {0}".format(id0)
    resourceid0 = item0.resource_id
    print "Resource ID: {0}".format(resourceid0)
    suggestedfilename0 = item0.suggested_filename
    print "Suggested Filename: {0}".format(suggestedfilename0)
    title0 = item0.title
    print "Title: {0}".format(title0)
    updated0 = item0.updated
    print "Updated: {0}".format(updated0)
    
    print "Done testing sample test"
    

    
    

def run_all_tests():
    print("starting tests")
    sample_test()

    #test_remove_file()
    #test_download_file()
    #test_create_child_path()

    print("all tests passed")

    
               

if __name__ == '__main__':
    run_all_tests()
    #main()
