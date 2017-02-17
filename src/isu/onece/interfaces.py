from zope.interface import Interface
import zope.schema


def _N(x):
    return x


class IObject(Interface):
    """This interface defines a root of 1C Enterprise like
    objects, e.g., Subsystems, Reference Books, Registers (Regystres) (?).
    """


class IGroup(Interface):
    """Defines an interface of object that
    contains a group of similar objects.
    """
    group = zope.schema.List(title=("Members"),
                             unique=True
                             )


class IReferenceBook(IObject):
    """A Reference Book interface that defines
    one default field -
    `name` - identifier of an item
    """
    name = zope.schema.TextLine(title=_N("Name"),
                                description=_N("Name of an item of the "
                                               "reference book"),
                                required=True,
                                constraint=lambda x: x.strip())
