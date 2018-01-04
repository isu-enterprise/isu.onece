from .interfaces import IDocument, IAccumulatorRegister
from zope.interface import implementer, implementedBy
import zope.schema
from collections import OrderedDict
from isu.onece.interfaces import IDimesion, IQuality, IRegister
from isu.onece.interfaces import IDocumentCreated, IDocumentAccepted
from isu.onece.interfaces import IDocumentRejected, IDocumentAboutToBeDeleted
from zope.component import getGlobalSiteManager


class RegisterStructure(object):
    """The container of the register structure"""

    def __init__(self, interface):
        self.interface = interface
        self.dimensions = []
        self.quantities = []
        self.requisites = []
        self.valid = True

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
    """Implements a simile uncached register functionality.

    The user has the responsibility that the supplied documents will
    have the reference fields
    """

    def __init__(self, interface):
        self.__structure__ = RegisterStructure(interface)
        self._registerSubscribers()

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

    def _getValues(self, doc, struct, code=True):
        #value = []
        for ref in struct:
            v = getattr(doc, ref)
            if code:
                v = v.code
            # value.append(v)
            yield v

    def onAccepted(self, doc):
        pass

    def onCreated(self, doc):
        pass

    def onRejected(self, doc):
        pass

    def onAboutToBeDeleted(self, doc):
        pass

    def _registerSubscribers(self):
        GM = getGlobalSiteManager()
        rg = GM.registerSubscriptionAdapter
        i = self.getStrcture().interface
        rg(self.onCreated, (i,), IDocumentCreated)
        rg(self.onAccepted, (i,), IDocumentAccepted)
        rg(self.onRejected, (i,), IDocumentRejected)
        rg(self.onAboutToBeDeleted, (i,), IDocumentAboutToBeDeleted)

    def __del__(self):
        self.destroy()

    def destroy(self):
        if self.getStrcture().valid:
            GM = getGlobalSiteManager()
            urg = GM.unregisterSubscriptionAdapter
            i = self.getStrcture().interface
            urg(self.onCreated, (i,), IDocumentCreated)
            urg(self.onAccepted, (i,), IDocumentAccepted)
            urg(self.onRejected, (i,), IDocumentRejected)
            urg(self.onAboutToBeDeleted, (i,), IDocumentAboutToBeDeleted)
            self.getStrcture().valid = False


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

    def remove(self, doc):
        self._validate(doc)
        self._documents.remove(doc)
        self._updatebalance(doc, positive=False)
        return doc

    def documents(self, date=None, accepted=True, **kw):
        for doc in self._documents:
            if doc.accepted == accepted:
                yield doc

    def balance(self, **kw):
        # TODO: date and dimensions must be supplied explicitly.
        # return self._balance
        quantities = self.getStrcture().quantities
        amount = [0.0] * len(quantities)
        for doc in self.documents(**kw):
            for i, v in enumerate(self._getValues(doc, quantities, code=False)):
                amount[i] += v
        return amount

    def _updatebalance(self, doc, positive=True):
        pass
