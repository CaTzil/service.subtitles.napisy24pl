## @package xbmcvfs
#  Classes and functions to work with files and folders.
#

class File(object):
    def __init__(self, filename, type = None):
        """
        'w' - opt open for write
        example:
         f = xbmcvfs.File(file, ['w'])
        """
        pass

    def close(self):
        """
        example:
         f = xbmcvfs.File(file)
         f.close()
        """
        pass

    def read(self, bytes = None):
        """
        bytes : how many bytes to read [opt]- if not set it will read the whole file
        example:
        f = xbmcvfs.File(file)
        b = f.read()
        f.close()
        """
        pass

    def readBytes(self, numbytes):
        """
        readBytes(numbytes)

        numbytes : how many bytes to read [opt]- if not set it will read the whole file

        returns: bytearray

        example:
        f = xbmcvfs.File(file)
        b = f.read()
        f.close()
        """
        return bytearray

    def seek(self):
        """
        FilePosition : position in the file
        Whence : where in a file to seek from[0 begining, 1 current , 2 end possition]
        example:
         f = xbmcvfs.File(file)
         result = f.seek(8129, 0)
         f.close()
        """
        pass

    def size(self):
        """
        example:
         f = xbmcvfs.File(file)
         s = f.size()
         f.close()
        """
        return int

    def write(self, buffer):
        """
        buffer : buffer to write to file
        example:
         f = xbmcvfs.File(file, 'w', True)
         result = f.write(buffer)
         f.close()
        """
        pass

#noinspection PyUnusedLocal
def copy(source, destination):
    """Copy file to destination, returns true/false.

    source: string - file to copy.
    destination: string - destination file

    Example:
        success = xbmcvfs.copy(source, destination)"""
    return bool

#noinspection PyUnusedLocal
def delete(file):
    """Deletes a file.

    file: string - file to delete

    Example:
        xbmcvfs.delete(file)"""
    pass

#noinspection PyUnusedLocal
def rename(file, newFileName):
    """Renames a file, returns true/false.

    file: string - file to rename
    newFileName: string - new filename, including the full path

    Example:
        success = xbmcvfs.rename(file,newFileName)"""
    return bool

#noinspection PyUnusedLocal
def mkdir(path):
    """Create a folder.

    path: folder

    Example:
        success = xbmcfvs.mkdir(path)
    """
    return bool

#noinspection PyUnusedLocal
def mkdirs(path):
    """
    mkdirs(path)--Create folder(s) - it will create all folders in the path.

    path : folder

    example:

    - success = xbmcvfs.mkdirs(path)
    """
    return bool

#noinspection PyUnusedLocal
def rmdir(path):
    """Remove a folder.

    path: folder

    Example:
        success = xbmcfvs.rmdir(path)
    """
    return bool

#noinspection PyUnusedLocal
def exists(path):
    """Checks for a file or folder existance, mimics Pythons os.path.exists()

    path: string - file or folder

    Example:
        success = xbmcvfs.exists(path)"""
    return bool

def listdir(path):
    """
    listdir(path) -- lists content of a folder.

    path        : folder

    example:
     - dirs, files = xbmcvfs.listdir(path)
    """
    pass

def mkdirs(path):
    """Create folder(s) - it will create all folders in the path.

    path: folder

    Example:
        success = xbmcfvs.mkdirs(path)
    """
    return bool

class Stat(object):
    def __init__(self, path):
        """
        Stat(path) -- get file or file system status.

        path        : file or folder

        example:
        - print xbmcvfs.Stat(path).st_mtime()
        """

    def st_mode(self):
        return None

    def st_ino(self):
        return None

    def st_nlink(self):
        return None

    def st_uid(self):
        return None

    def st_gid(self):
        return None

    def st_size(self):
        return None

    def st_atime(self):
        return None

    def st_mtime(self):
        return None

    def st_ctime(self):
        return None
