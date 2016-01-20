import logging
import inspect
from logentries import LogentriesHandler
from django.conf import settings

class LoggingService(object):

    def __init__(self):
        self.log = logging.getLogger('logentries')
        self.log.setLevel(logging.INFO)

    def error(self, message):
        self.log.error(message)

    def warn(self, message):
        self.log.warn(message)

    def info(self, message):
        caller = self._caller_name()
        formatted = self._format(message, caller)
        self.log.info(formatted)

    def debug(self, message):
        self.log.debug(message)

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
        # `modname` can be None when frame is executed directly in console
        # TODO(techtonik): consider using __main__
        if module:
            name.append(module.__name__)
        # detect classname
        if 'self' in parentframe.f_locals:
            # I don't know any way to detect call from the object method
            # XXX: there seems to be no way to detect static method call - it will
            #      be just a function call
            name.append(parentframe.f_locals['self'].__class__.__name__)
        codename = parentframe.f_code.co_name
        if codename != '<module>':  # top level usually
            name.append( codename ) # function or a method
        del parentframe
        return ".".join(name[1:])
