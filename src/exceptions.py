class MissingKeywords(Exception):
    message = "Keywords are required"

    def __init__(self, message=None):
        super().__init__()
        if message:
            self.message = message