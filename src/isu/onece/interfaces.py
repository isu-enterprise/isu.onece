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
    group = zope.schema.List(title=_N("Members"),
                             description=_N("Group of objects"),
                             unique=True,
                             required=True
                             )
    subgrouping = zope.schema.Bool(title=_N("Subgrouping"),
                                   description=_N("Whether this group can "
                                                  "have subgroups"),
                                   required=True
                                   )


class ICatalog(IObject):
    """A catalog interface that defines
    one default field -
    `name` - identifier of an item
    FIXME: May be define an id???
    """
    name = zope.schema.TextLine(title=_N("Name"),
                                description=_N("Name of an item of the "
                                               "catalog"),
                                required=True,
                                constraint=lambda x: x.strip())


class IDocument(ICatalog):
    """Interface describes documents identified
    by a number in a sequence and an issue data.
    """

    number = zope.schema.TextLine(
        title=_("Number")
    )

    data = zope.schema.Datetime(
        title=_("Date")
    )
