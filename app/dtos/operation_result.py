from app.dtos.issue import Issue, SEVERITY_ERROR


class OperationResult(object):
    def __init__(self, input_data):
        self.input_data = input_data
        self.output_data = None
        self.issues = []

    def set_output_data(self, output_data):
        self.output_data = output_data

    def append_issue(self, message, severity=SEVERITY_ERROR):
        self.issues.append(
            Issue(message, severity)
        )

    def copy_issues_to(self, other_result):
        for issue in self.issues:
            other_result.append_issue(issue.message)

    def has_issue(self):
        return not len(self.issues) <= 0

    def serialize_issues(self):
        serialized = []
        for issue in self.issues:
            serialized.append(issue.__dict__)
        return serialized
