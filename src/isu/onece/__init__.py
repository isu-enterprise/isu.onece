# Example package with a console entry point
from __future__ import print_function

import zope.schema
from isu.onece.interfaces import IVocabularyItem, IDimesion, IQuality
from zope.interface import implementer

from isu.onece.registers import AccumulatorRegister


@implementer(IDimesion)
class Dimention(zope.schema.Object):
    """Defines the reference to vocabulary record objects
    stored in Documents."""


@implementer(IQuality)
class Quantity(zope.schema.Object):
    """Defines the reference to amounts in a Documents."""


class VocabularyItem(zope.schema.Object):
    """Defines a VocabularyItem fields in Documents"""
