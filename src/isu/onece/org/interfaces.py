# Organizational unit related interfaces, in general.
from isu.onece.interfaces import IObject, IVocabularyItem, IDocument, IPerson


class IOrganization(IObject):
    pass


class ISpecification(IDocument):
    pass


class IEmployee(IPerson):
    pass
