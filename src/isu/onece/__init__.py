# Example package with a console entry point
from __future__ import print_function

import zope.schema
from isu.onece.interfaces import IRecord, IDimesion, IQuality, IDocument
from isu.onece.interfaces import IDocumentEvent, IDocumentCreated, IDocumentAccepted
from isu.onece.interfaces import IDocumentRejected, IDocumentAboutToBeDeleted
from zope.interface import implementer, directlyProvides, providedBy
import zope.schema.interfaces
from isu.onece.registers import AccumulatorRegister
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


class Record(zope.schema.Object):
    """Defines a Record field in Documents"""


def notify(required, provided, context=None):
    sl = subscribers(required, provided, context=context)
    return sl


@implementer(IDocument)
class DocumentBase(object):
    def _getnumber(self):
        return self.code

    def _setnumber(self, value):
        self.code = value

    number = property(_getnumber, _setnumber)

    def __init__(self, number, date):
        self.date = date
        self.number = number
        self.accepted = False
        self.initialize()

    def initialize(self):
        self.accepted = False

    def _notify_created(self):
        # FIXME: How to issue this event after all inits?
        notify((self,), IDocumentCreated)

    def accept(self):
        if not self.accepted:
            notify((self,), IDocumentAccepted)
            self.accepted = True

    def reject(self):
        if self.accepted:
            notify((self,), IDocumentRejected)
            self.accepted = False

    def __del__(self):
        if self.accepted:
            self.reject()  # FIXME: What to do if it is not rejected?
        notify((self,), IDocumentAboutToBeDeleted)
