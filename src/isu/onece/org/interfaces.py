# Organizational unit related interfaces, in general.
from isu.onece.interfaces import IRecord, IDocument


class IOrganization(IRecord):
    pass


class ISpecification(IDocument):
    pass

class IPerson(IRecord):
    pass

class IEmployee(IPerson):
    pass
