class TimeCardValidationIssue(object):
    LEVEL_ERROR = 128
    LEVEL_WARNING = 64

    def __init__(self, level, notes):
        self.level = level
        self.notes = notes
