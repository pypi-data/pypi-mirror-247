class NotFoundEntityError(Exception):
    def __init__(self, entity_name):
        self.code = "0007",
        self.name = "NotFoundEntityError",
        self.message = f"{entity_name} is not found."
        super(NotFoundEntityError, self).__init__(self.message)
