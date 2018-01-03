

class DocumentException(Exception):
    """Defines a document exception"""

    @property
    def document(self):
        return self.context

    def __init__(self, context, msg):
        super(DocumentException, self).__init__(msg)
        self.context = context


class DocumentNotAccepted(DocumentException):
    """A Document cannot be accepted for some reason."""


class DocumentNotRejected(DocumentException):
    """A Document cannot be rejected for some reason."""
