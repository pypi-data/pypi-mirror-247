class Result:
    def __init__(self, code, message, **kwargs):
        self.code = code
        self.message = message
        self.fields = kwargs

    def to_dict(self):
        result_dict = {
            "code": self.code,
            "message": self.message,
        }
        result_dict.update(self.fields)
        return result_dict

    @classmethod
    def ok(cls, **kwargs):
        return cls(code="0000", message="Success", **kwargs).to_dict()

    @classmethod
    def fail(cls, e: Exception, **kwargs):
        return cls(code=e.code[0], name=e.name[0], message=e.message, **kwargs).to_dict()
