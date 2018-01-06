from isu.onece.register import StructuredRegisterBase
from isu.onece.register.interfaces import IAccumulatorRegister
from isu.onece.register._record import RecordRegisterStructure
from zope.interface import implementer


class AccumulatorRegisterStructure(RecordRegisterStructure):
    """The container of the register structure"""

    def __init__(self, interface=None):
        super(AccumulatorRegisterStructure, self).__init__(interface=interface)
        self.dimensions = []
        self.quantities = []
        self.requisites = []

    def extend(self, aList, iterable):
        for i in iterable:
            if i not in aList:
                aList.append(i)
        return aList

    # EVENTS = RecordRegisterStructure.EVENTS + [
    #     (IDocumentAccepted, "onDocumentAccepted"),
    #     (IDocumentRejected, "onDocumentRejected")
    # ]


class AggregationRegisterBase(StructuredRegisterBase):
    __structure__type__ = AccumulatorRegisterStructure

    def getStrcture(self):
        return self.__structure__

    def addDimensions(self, *fields):
        rs = self.getStrcture()
        rs.extend(rs.dimensions, fields)
        return fields

    addDimension = addDimensions

    def addQuantities(self, *fields):
        rs = self.getStrcture()
        rs.extend(rs.quantities, fields)
        return fields

    addQuantity = addQuantities

    def _getValues(self, doc, struct, code=True):
        for ref in struct:
            v = getattr(doc, ref)
            if code:
                v = v.code
            yield v


@implementer(IAccumulatorRegister)
class AccumulatorRegister(AggregationRegisterBase):
    pass
