from app.dtos.issue import Issue, SEVERITY_ERROR


class OperationResult(object):
    issues = None
    input_data = None
    output_data = None

    def __init__(self, input_data):
        self.input_data = input_data

    def set_output_data(self, output_data):
        self.output_data = output_data

    def append_issue(self, message, severity=SEVERITY_ERROR):
        if (self.issues is None):
            self.issues = []
        self.issues.append(
            Issue(message, severity)
        )

    def has_issue(self):
        if (self.issues is None or len(self.issues) <= 0):
            return False
        return True
