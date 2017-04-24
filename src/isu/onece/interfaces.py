from zope.interface import Interface, Attribute
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


class IVocabularyItemBase(IObject):
    """A Base interface to create
    various catalogs. Here we do not
    suppose any relation, only identifier.
    """
    code = zope.schema.Field(  # FIXME: Suppose the user must specify.
        title=_("Code"),
        description=_("The identifier denoting "
                      "the record of the catalog"),
        required=True
    )


class IHierarchyBase(IObject):
    """The base of hierarchy composition, e.g.,
    species, but here we consider subjects connected
    with is_a relation.
    """
    parent_code = zope.schema.Field(  # FIXME: the type is unknown
        title=_("Parent code"),
        description=_("The identifier denoting "
                      "the parent record of the "
                      "current item of the catalog."),
        required=False
    )


class IVocabularyItem(IVocabularyItemBase):
    """A catalog interface that defines
    one default field -
    `name` - identifier of an item
    """
    title = zope.schema.TextLine(title=_N("Title"),
                                description=_N("Title of the item of the "
                                               "catalog"),
                                required=True,
                                constraint=lambda x: x.strip())


class IVocabulary(IObject):
    """Defines a vocabulary"""
    terms = zope.schema.List(
        title=_N("Vocabulary"),
        description=_N("A vocabulary mapping an id to a name"),
        value_type=zope.schema.Object(
            schema=IVocabularyItem
        )
    )


class IDocument(IVocabularyItem):
    """Interface describes documents identified
    by a number in a sequence and an issue data.
    """

    number = zope.schema.TextLine(
        title=_("Number")
    )

    data = zope.schema.Datetime(
        title=_("Date")
    )
    
class IFlowDocument(IDocument):
    receipt = zope.schema.Bool(
        title = _("receipt"),
        description= _("Determinates whether the document a receipt (True) or an expense document."),
        required=True
        # readonly = true # ? FIXME: Determinate!
    )

class IRegister(Interface):

    def add(document):
        """Adds a document to the register
        """

    def remove(document):
        """Removed a document from the register.
        """

    def documents(filter=None):
        """Lists documents conforming the filter
        """


class IAccumulatorRegister(IRegister):
    pass


class ITurnoverRegister(IRegister):
    pass


class IPerson(IVocabularyItem):
    pass
