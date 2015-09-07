SEVERITY_ERROR = 'error'
SEVERITY_WARNING = 'warning'


class Issue(object):
    def __init__(self, message, severity=SEVERITY_ERROR):
        self.message = message
        self.severity = severity
