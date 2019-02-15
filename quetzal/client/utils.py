import atexit
import code
import logging
import pathlib
import warnings

from .config import get_config_dir


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
