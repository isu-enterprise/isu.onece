from isu.onece.register import StructuredRegisterBase
from isu.onece.register.interfaces import IAccumulatorRegister
from isu.onece.register._record import RegisterStructure
from zope.interface import implementer
from isu.onece.interfaces import IDocumentAccepted, IDocumentRejected


class AccumulatorRegisterStructure(RegisterStructure):
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

    EVENTS = RegisterStructure.EVENTS + [
        (IDocumentAccepted, "onDocumentAccepted"),
        (IDocumentRejected, "onDocumentRejected")
    ]


class AggregationRegisterBase(StructuredRegisterBase):
    __structure__type__ = AccumulatorRegisterStructure

    def getStructure(self):
        return self.__structure__

    def addDimensions(self, *fields):
        rs = self.getStructure()
        rs.extend(rs.dimensions, fields)
        return fields

    addDimension = addDimensions

    def addQuantities(self, *fields):
        rs = self.getStructure()
        rs.extend(rs.quantities, fields)
        return fields

    addQuantity = addQuantities

    def _getValues(self, doc, struct, code=True):
        for ref in struct:
            v = getattr(doc, ref)
            if code:
                v = v.code
            yield v

    def _key(self, doc, code=True):
        return tuple(self._getValues(doc,
                                     self.getStructure().dimensions,
                                     code=code))

    def _value(self, doc, code=False):
        return tuple(self._getValues(doc,
                                     self.getStructure().quantities,
                                     code=code))

    def value(self, query=None):
        raise RuntimeError("implemented by subclass")


@implementer(IAccumulatorRegister)
class SimpleAccumulatorRegister(AggregationRegisterBase):
    def __init__(self, interface=None):
        super(SimpleAccumulatorRegister, self).__init__(interface=interface)
        # Надо узнать все значения размерностей
        self.aggregator = {}

    def _getKeyVal(self, doc):
        k = self._key(doc)
        v = self._value(doc)
        return k, v

    def onDocumentAccepted(self, doc):
        agg = self.aggregator
        k, v = self._getKeyVal(doc)
        if k in agg:
            agg[k] += v
        else:
            agg[k] = v

    def onDocumentRejected(self, doc):
        agg = self.aggregator
        k, v = self._getKeyVal(doc)
        if k in agg:
            agg[k] -= v
        else:
            raise RuntimeError("unknown rejected document data")

    def value(self, key=None):
        if key is None:
            return self.aggregator
        else:
            def __(x):
                if hasattr(x, 'code'):
                    x = x.code
                return x
            key = tuple([__(k) for k in key])
            return self.aggregator[key]
