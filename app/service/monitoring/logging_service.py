import logging
import inspect
from logentries import LogentriesHandler
from cid.log import CidContextFilter
from django.conf import settings

class LoggingService(object):

    def __init__(self):
        self.log = logging.getLogger('logentries')
        self.log.setLevel(logging.INFO)
        self.log.addFilter(CidContextFilter())

    def error(self, message):
        caller = self._caller_name()
        formatted = self._format(message, caller)
        self.log.error(formatted)

    def warn(self, message):
        caller = self._caller_name()
        formatted = self._format(message, caller)
        self.log.warn(formatted)

    def info(self, message):
        caller = self._caller_name()
        formatted = self._format(message, caller)
        self.log.info(formatted)

    def debug(self, message):
        caller = self._caller_name()
        formatted = self._format(message, caller)
        # For debug info, print to console as well
        print formatted
        self.log.debug(formatted)

    def _format(self, message, caller):
        return '{}; REPORTER: {}'.format(message, caller)

    def _caller_name(self, skip=2):
        """Get a name of a caller in the format module.class.method

           `skip` specifies how many levels of stack to skip while getting caller
           name. skip=1 means "who calls me", skip=2 "who calls my caller" etc.

           An empty string is returned if skipped levels exceed stack height
        """
        stack = inspect.stack()
        start = 0 + skip
        if len(stack) < start + 1:
          return ''
        parentframe = stack[start][0]

        name = []
        module = inspect.getmodule(parentframe)

        if module:
            name.append(module.__name__)
        # detect classname
        if 'self' in parentframe.f_locals:
            name.append(parentframe.f_locals['self'].__class__.__name__)
        codename = parentframe.f_code.co_name
        if codename != '<module>':  # top level usually
            name.append( codename ) # function or a method
        del parentframe
        return ".".join(name[1:])
