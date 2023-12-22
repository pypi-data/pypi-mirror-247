class LengthError(Exception):
    def __init__(self):
        self.message = "The length of the row does " \
                       "not match the previous row(s)."
        super().__init__(self.message)


