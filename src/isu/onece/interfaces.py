from zope.interface import Interface, Attribute
import zope.schema
import zope.schema.interfaces


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


class IVocabularyItemBase(Interface):
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


class IHierarchyBase(Interface):
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
    `title` - identifier of an item
    """
    title = zope.schema.TextLine(title=_N("Title"),
                                 description=_N("Title of the item of the "
                                                "catalog"),
                                 required=True,
                                 constraint=lambda x: x.strip())


class IVocabulary(IComponent):
    """Defines a vocabulary"""
    terms = zope.schema.List(
        title=_N("Vocabulary"),
        description=_N("A vocabulary mapping an id to a name"),
        value_type=zope.schema.Object(
            schema=IVocabularyItem
        )
    )


class IDocument(IVocabularyItem, IComponent):
    """Interface describes documents identified
    by a number in a sequence and an issue data.
    """

    number = zope.schema.TextLine(
        title=_("Number"),
        description=_("The unique number of the "
                      "document at least within "
                      "the document species."
                      "By default this should be a "
                      "synonym of the `code` field."
                      ),
        required=True,
        constraint=lambda x: x.strip()
    )

    date = zope.schema.Datetime(
        title=_("Date"),
        description=_("The issue date of the"
                      "document."),
        required=True
    )

    accepted = zope.schema.Bool(
        title=_("Accepted"),
        description=_("Is the document accepted. By default it is not."),
        readonly=True
    )

    def accept():
        """Accept the document as to be valid."""

    def reject():
        """Make the document to be no longer valid."""

    def update():
        """The document changed a set of its states."""


class IFlowDocument(IDocument):
    receipt = zope.schema.Bool(
        title=_("receipt"),
        description=_(
            "Determinates whether the document a receipt (True) or an expense document."),
        required=True
        # readonly = true # ? FIXME: Determinate!
    )


class IDocumentEvent(Interface):
    """Marker interface of a general document event."""


class IDocumentCreated(IDocumentEvent):
    """Maker interface denoting the event of a document creation."""


class IDocumentAccepted(IDocumentEvent):
    """Maker interface denoting the event of a document acceptance."""


class IDocumentRejected(IDocumentEvent):
    """Maker interface denoting the event of a document rejection."""


class IDocumentAboutToBeDeleted(IDocumentEvent):
    """Maker interface denoting the event of
    a document about to be removed."""


class IRegister(IComponent):

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
    def balance(date, axes=None):
        """Return balance for the axes
        """


class ITurnoverRegister(IRegister):
    pass


class IPerson(IVocabularyItem):
    pass
