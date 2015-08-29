from app.view_models.validation_issue import ValidationIssue, SEVERITY_ERROR


class ViewModelBase(object):
    validation_issues = None

    def append_validation_issue(self, message, severity=SEVERITY_ERROR):
        if (self.validation_issues is None):
            self.validation_issues = []
        self.validation_issues.append(
            ValidationIssue(message, severity)
        )

    def is_valid(self):
        if (self.validation_issues is None or len(self.validation_issues) <= 0):
            return True
        return False
