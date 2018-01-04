from .interfaces import IDocument, IAccumulatorRegister
from zope.interface import implementer, implementedBy
import zope.schema
from collections import OrderedDict
from isu.onece.interfaces import IDimesion, IQuality, IRegister


# class RegisterBase(object):
#     dimensions = OrderedDict()
#     quantities = OrderedDict()
#     requsites = OrderedDict()
#     bound = False

#     def __new__(cls, *args, **kw):
#         if not cls.bound:
#             cls.bind()
#         return object.__new__(cls, *args, **kw)

#     @classmethod
#     def bind(cls):
#         for i in implementedBy(cls):
#             for name, field in zope.schema.getFields(i).items():
#                 if IDimesion.providedBy(field):
#                     cls.dimensions[name] = field
#                 elif IQuality.providedBy(field):
#                     cls.quantities[name] = field
#                 else:
#                     cls.requsites[name] = field

#         assert cls.dimensions and cls.quantities, "empty binding"

#         cls.bound = True
#         return cls.bound

class RegisterStructure(object):
    def __init__(self, interface):
        self.interface = interface
        self.dimensions = []
        self.quantities = []
        self.requisites = []

    def extend(self, aList, iterable):
        for i in iterable:
            # idx = aList.find(i)
            # if idx >= 0:
            #     aList.pop(idx)
            # aList.append(i)
            if i not in aList:
                aList.append(i)
        return aList


@implementer(IRegister)
class RegisterBase(object):
    def __init__(self, interface):
        self.__structure__ = RegisterStructure(interface)

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

    def getStrcture(self):
        return self.__structure__

    def _validate(self, obj):
        i = self.getStrcture().interface
        assert i.providedBy(obj), "argument must be an {} provider".format(i)


class AccumulatorRegisterBase(RegisterBase):
    pass


@implementer(IAccumulatorRegister)
class AccumulatorRegister(AccumulatorRegisterBase):
    """Accumulates amounts by means of
    accumulating document's data.
    """

    def __init__(self, interface):
        super(AccumulatorRegister, self).__init__(interface)
        self._documents = []

    def add(self, doc):
        self._validate(doc)
        self._documents.append(doc)
        # TODO: request all transactions
        # self._balance += self._get_amount(doc)
        self._updatebalance(doc)
        return doc

    def _get_amount(self, doc, asxes=None):
        db = doc.amount()
        if not doc.receipt:
            db = -db
        return db

    def remove(self, doc):
        self._validate(doc)
        self._documents.remove(doc)
        self._updatebalance(doc, positive=False)
        return doc

    def documents(self, filter=None):
        return self._documents

    def balance(self, date=None, dimensions=None):
        # TODO: date and dimensions must be supplied explicitly.
        # return self._balance
        return [0.0]

    def _updatebalance(self, doc, positive=True):
        pass
