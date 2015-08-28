SEVERITY_ERROR = 'error'
SEVERITY_WARNING = 'warning'
SEVERITY_INFO = 'info'
SEVERITY_DEBUG = 'debug'


class ValidationIssue(object):
    severity = SEVERITY_ERROR
    message = ''

    def __init__(self, message, severity=SEVERITY_ERROR):
        self.message = message
        self.severity = severity
