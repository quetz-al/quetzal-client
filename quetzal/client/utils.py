import atexit
import code
import hashlib
import logging
import pathlib


import appdirs


logger = logging.getLogger(__name__)


# readline is special: it works on unix flavors but not on windows; we have
# to use pyreadline, which only works on windows.
try:
    import readline
    _readline_available = True
except:
    try:
        import pyreadline as readline
    except:
        logger.debug('readline not available', exc_info=True)
        _readline_available = False


# An interactive console with history support!
# from: https://docs.python.org/3/library/readline.html
class HistoryConsole(code.InteractiveConsole):

    def __init__(self, locals=None, filename="<console>"):
        super(HistoryConsole, self).__init__(locals, filename)
        histfile = pathlib.Path(get_config_dir()) / '.history'
        self.init_history(str(histfile))

    def init_history(self, histfile):
        if not _readline_available:
            return

        readline.parse_and_bind("tab: complete")
        if hasattr(readline, "read_history_file"):
            try:
                readline.read_history_file(histfile)
            except FileNotFoundError:
                pass
            atexit.register(self.save_history, histfile)

    def save_history(self, histfile):
        if not _readline_available:
            return

        try:
            file = pathlib.Path(histfile)
            file.parent.mkdir(parents=True, exist_ok=True)
            readline.set_history_length(1000)
            readline.write_history_file(histfile)
        except:
            logger.debug('Could not save console history', exc_info=True)


def get_data_dir():
    from quetzal.client import __version__
    # Only keep major.minor
    version = '.'.join(__version__.split('.')[:2])
    dirname = appdirs.user_data_dir(
        appname='quetzal-client',
        appauthor='quetzal',
        version=version,
        roaming=False
    )
    return dirname


def get_config_dir():
    from quetzal.client import __version__
    # Only keep major.minor
    version = '.'.join(__version__.split('.')[:2])
    return appdirs.user_config_dir(
        appname='quetzal-client',
        appauthor='quetzal',
        version=version,
        roaming=False,
    )


def get_readable_info(file_obj):
    """ Extract useful information from reading a file

    This function calculates the md5sum and the file size in bytes from a
    file-like object. It does both operations at the same time, which means
    that there is no need to read the object twice.

    After this function reads the file content, it will set the file pointer
    to its original position through `tell`.

    Parameters
    ----------
    file_obj: file-like
        File object. It needs the `read` and `tell` methods.

    Returns
    -------
    md5sum, size: str, int
        MD5 sum and size of the file object contents

    """
    size = 0
    position = file_obj.tell()
    hashobj = hashlib.new('md5')
    while True:
        chunk = file_obj.read(4096)
        size += len(chunk)
        if not chunk:
            break
        hashobj.update(chunk)
    file_obj.seek(position)
    return hashobj.hexdigest(), size
