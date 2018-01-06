from zope.interface import Interface, Attribute
import zope.schema
import zope.schema.interfaces
import zope.interface.interfaces
from isu.onece.interfaces import IComponent


def _N(x):
    return x


_ = _N


class IDimesion(zope.schema.interfaces.IDottedName):
    """Defines dimensions as a reference to VocabularyItem"""


class IQuality(zope.schema.interfaces.IDottedName):
    """Defines amounts as reference to a field"""


class IRequisite(zope.schema.interfaces.IDottedName):
    """Defines a requisite for a Register """


class IComponent(Interface):
    """This marker interface defines a root of 1C Enterprise like
    components, e.g., Subsystems, Reference Books, Registers.
    """


class IRegister(IComponent):
    """A register of something (Abstract marker interface)

    Consider it as a warehouse."""

    # def add(document):
    #     """Adds a document to the register
    #     """

    # def remove(document):
    #     """Removed a document from the register.
    #     """

    # def documents(filter=None):
    #     """Lists documents conforming the filter
    #     """


class IRecordRegister(IRegister):
    """A register of records, including documents.

    Consider it as a warehouse."""


class IDocumentRegister(IRegister):
    """A register of documents as an extension of
    record register. Marker."""


class IAggregationRegister(IRegister):
    """Defines register that make calculation over
    records of a record register."""

    def value(**kwargs):
        """Returns a tuple of aggregate values
        reflecting filter defined by combinations of
        'kwargs'."""


class ICumulativeRegister(IAggregationRegister):
    """Defines a register whose value is
    accumulated with all new document."""


class IAccumulatorRegister(ICumulativeRegister):
    pass


class ITurnoverRegister(ICumulativeRegister):
    pass


# class IPerson(IVocabularyItem):
#     pass
