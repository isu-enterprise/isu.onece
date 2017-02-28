from zope.interface import Interface
import zope.schema


def _N(x):
    return x


_ = _N


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


class ICatalogItemBase(IObject):
    """A Base interface to create
    various catalogs. Here we do not
    suppose any relation, only identifier.
    """
    id = zope.schema.Field( # FIXME: Suppose the user must specify.
        title=_("Code"),
        description=_("The identifier denoting "
                      "the record of the catalog"),
        required=True
    )

class IHierarchyItemBase(IObject):
    """The base of hierarchy composition, e.g.,
    species, but here we consider subjects connected
    with is_a relation.
    """
    parent_id = zope.schema.Field(  # FIXME: the type is unknown
        title=_("Parent code"),
        description=_("The identifier denoting "
                      "the parent record of the "
                      "current item of the catalog."),
        required=False
    )

# FIXME: Consider it redundant
#class IHierarchicalCatalogItemBase(ICatalogItemBase, IHierarchyItemBase):
#    """The basis of hierarchical catalog construction.
#    """


class ICatalogItem(ICatalogItemBase):
    """A catalog interface that defines
    one default field -
    `name` - identifier of an item
    """
    name = zope.schema.TextLine(title=_N("Name"),
                                description=_N("Name of an item of the "
                                               "catalog"),
                                required=True,
                                constraint=lambda x: x.strip())

class IHierarchicalCatalogItem(ICatalogItem, IHierarchyItemBase):
    """The item of an hierarchical catalog. The
    items already have names inherited from ICatalogItem.
    """


class IDocument(ICatalogItem):
    """Interface describes documents identified
    by a number in a sequence and an issue data.
    """

    number = zope.schema.TextLine(
        title=_("Number")
    )

    data = zope.schema.Datetime(
        title=_("Date")
    )


class IPerson(ICatalogItem):
    pass
