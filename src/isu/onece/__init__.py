# Example package with a console entry point
from __future__ import print_function

import zope.schema
from isu.onece.interfaces import IVocabularyItem, IDimesion, IQuality
from zope.interface import implementer
import zope.schema.interfaces
from isu.onece.registers import AccumulatorRegister


class Reference(zope.schema.Object):
    def __init__(self, schema, fieldname):
        super(Reference, self).__init__(zope.schema.interfaces.IField)
        self._schema = schema
        self._fieldname = fieldname


@implementer(IDimesion)
class Dimention(Reference):
    """Defines the reference to vocabulary record objects
    stored in Documents."""


@implementer(IQuality)
class Quantity(Reference):
    """Defines the reference to amounts in a Documents."""


class VocabularyItem(zope.schema.Object):
    """Defines a VocabularyItem fields in Documents"""
