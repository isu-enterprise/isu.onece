# Organizational unit related interfaces, in general.
from isu.onece.interfaces import IObject, ICatalog, IDocument


class IOrganization(IObject):
    pass


class ISpecufication(IDocument):
    pass


class IEmployee(IPerson):
    pass
