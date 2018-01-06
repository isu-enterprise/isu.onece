# Example package with a console entry point
from __future__ import print_function

import zope.schema
from isu.onece.register.interfaces import IDimesion, IQuality
from isu.onece.interfaces import IRecordRef
from isu.onece.interfaces import IRecord, IDocument
from isu.onece.interfaces import IRecordCreated, IRecordAboutToBeDeleted
from isu.onece.interfaces import IDocumentAccepted, IDocumentRejected
from zope.interface import implementer, directlyProvides, providedBy
import zope.schema.interfaces
# from isu.onece.registers import AccumulatorRegister
import zope.component.event
from isu.onece.exceptions import DocumentNotAccepted, DocumentNotRejected
from zope.component import adapter, subscribers

# FIXME: Is the description of a Register a class or instance?


class Reference(zope.schema.DottedName):
    """Reference to a record or a data field."""

    def __init__(self, fieldname, **kwargs):
        super(Reference, self).__init__(zope.schema.interfaces.IField)
        self._fieldname = fieldname


@implementer(IDimesion)
class Dimension(Reference):
    """Defines the reference to vocabulary record objects
    stored in Documents."""


@implementer(IQuality)
class Quantity(Reference):
    """Defines the reference to amounts in a Documents."""


@implementer(IRecordRef)
class RecordRef(zope.schema.Object):
    """Defines a record reference in other records' schema."""


def notify(required, provided, context=None):
    sl = subscribers(required, provided, context=context)
    return sl


class RecordBase(object):
    def __init__(self, code):
        self.code = code

    def created(self):
        """Helper method to notify that the record
        has been created and initialized to a correct
        state."""
        notify((self,), IRecordCreated)

    def delete(self):
        """Notify the system, that the record data
        will be removed from warehouses."""
        notify((self,), IRecordAboutToBeDeleted)


@implementer(IRecord)
class Record(RecordBase):
    """Defines a Record field in Documents"""


class DocumentBase(RecordBase):
    def _getnumber(self):
        return self.code

    number = property(_getnumber)

    def __init__(self, number, date):
        super(DocumentBase, self).__init__(code=number)
        self.date = date
        self.accepted = False

    def accept(self):
        """Notify the system that the document becoming
        valid and its data can be used in accounting calculations.
        """
        if not self.accepted:
            notify((self,), IDocumentAccepted)
            self.accepted = True

    def reject(self):
        """Notify the system that the document is no longer
        valid and its data should not be accounted."""
        if self.accepted:
            notify((self,), IDocumentRejected)
            self.accepted = False

    def delete(self):
        """Notify the system, that the document data
        will be removed from warehouses."""
        if self.accepted:
            self.reject()  # FIXME: What to do if it is not rejected?
        super(DocumentBase, self).delete()


@implementer(IDocument)
class Document(DocumentBase):
    """Defines base type for documents, the application type"""
