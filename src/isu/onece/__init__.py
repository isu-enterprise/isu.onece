# Example package with a console entry point
from __future__ import print_function

import zope.schema
from isu.onece.interfaces import IVocabularyItem, IDimesion, IQuality, IDocument
from isu.onece.interfaces import IDocumentEvent, IDocumentCreated, IDocumentAccepted
from isu.onece.interfaces import IDocumentRejected, IDocumentAboutToBeDeleted
from zope.interface import implementer
import zope.schema.interfaces
from isu.onece.registers import AccumulatorRegister
import zope.event
from isu.onece.exceptions import DocumentNotAccepted, DocumentNotRejected

# FIXME: Is the description of a Register a class or instance?


class Reference(zope.schema.DottedName):
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


class VocabularyItem(zope.schema.Object):
    """Defines a VocabularyItem fields in Documents"""


@implementer(IDocumentEvent)
class DocumentEvent(object):
    """See IDocumentEvent"""

    @property
    def document(self):
        return self.context

    def __init__(self, context):
        self.context = context


@implementer(IDocumentCreated)
class DocumentCreated(DocumentEvent):
    """See IDocumentCreated"""


@implementer(IDocumentAccepted)
class DocumentAccepted(DocumentEvent):
    """See IDocumentAccepted"""


@implementer(IDocumentRejected)
class DocumentRejected(DocumentEvent):
    """See IDocumentRejected"""


@implementer(IDocumentAboutToBeDeleted)
class DocumentAboutToBeDeleted(DocumentEvent):
    """See IDocumentDeleted"""


@implementer(IDocument)
class DocumentBase(object):
    def _getnumber(self):
        return self.code

    def _setnumber(self, value):
        self.code = value

    number = property(_getnumber, _setnumber)

    def __init__():
        self.number = number
        self.title = title
        self.accepted = False

    def _notify_created(self):
        # FIXME: How to issue this event after all inits?
        zope.event.notify(DocumentCreated(self))

    def accept(self):
        if not self.accepted:
            zope.event.notify(DocumentAccepted(self))
            self.accepted = True

    def reject(self):
        if self.accepted:
            zope.event.notify(DocumentRejected(self))
            self.accepted = False

    def __del__(self):
        if self.accepted:
            self.reject()  # FIXME: What to do if it is not rejected?
        zope.event.notify(DocumentAboutToBeDeleted(self))
