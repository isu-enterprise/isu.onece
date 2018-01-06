from .interfaces import IDocument, IAccumulatorRegister
from zope.interface import implementer, implementedBy
import zope.schema
from collections import OrderedDict
from isu.onece.interfaces import IDimesion, IQuality, IRegister
from isu.onece.interfaces import IDocumentCreated, IDocumentAccepted
from isu.onece.interfaces import IDocumentRejected, IDocumentAboutToBeDeleted
from zope.component import getGlobalSiteManager
from asq.initiators import query


class RegisterStructure(object):
    """The container of the register structure"""

    def __init__(self, interface):
        self.interface = interface
        self.dimensions = []
        self.quantities = []
        self.requisites = []
        self.subscibers = []

    def extend(self, aList, iterable):
        for i in iterable:
            # idx = aList.find(i)
            # if idx >= 0:
            #     aList.pop(idx)
            # aList.append(i)
            if i not in aList:
                aList.append(i)
        return aList

    EVENTS = [IDocumentCreated, IDocumentAccepted,
              IDocumentRejected, IDocumentAboutToBeDeleted]

    def subscribe(self, register):
        if self.subscibers:
            return
        GM = getGlobalSiteManager()
        rg = GM.registerSubscriptionAdapter
        i = self.interface
        r = register
        self.subscibers = [r.onCreated, r.onAccepted,
                           r.onRejected, r.onAboutToBeDeleted]
        for method, event in zip(self.subscibers, self.__class__.EVENTS):
            rg(method, (i,), event)

    def unsubscribe(self, register):
        if not self.subscibers:
            return
        GM = getGlobalSiteManager()
        urg = GM.unregisterSubscriptionAdapter
        i = self.interface
        r = register
        for method, event in zip(self.subscibers, self.__class__.EVENTS):
            urg(method, (i,), event)
        self.subscibers = []


tmp = None


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
        self.getStrcture().subscribe(self)

    def __del__(self):
        self.destroy()

    def destroy(self):
        self.getStrcture().unsubscribe(self)


class SimpleRegisterBase(RegisterBase):
    def __init__(self, interface):
        super(SimpleRegisterBase, self).__init__(interface)
        self.documents = OrderedDict()
        self.accepted = OrderedDict()

    def onCreated(self, doc):
        self.documents[doc.code] = doc

    def onAccepted(self, doc):
        self.accepted[doc.code] = doc

    def onRejected(self, doc):
        del self.accepted[doc.code]

    def onAboutToBeDeleted(self, doc):
        del self.documents[doc.code]

    def query(self, accepted=True):
        if accepted:
            q = query(self.accepted)
        return q


@implementer(IAccumulatorRegister)
class AccumulatorRegister(SimpleRegisterBase):
    """Accumulates amounts by means of
    accumulating document's data.
    """

    def balance(self, **kw):
        # TODO: date and dimensions must be supplied explicitly.
        # return self._balance
        quantities = self.getStrcture().quantities
        amount = [0.0] * len(quantities)
        for doc in self.query(**kw):
            for i, v in enumerate(self._getValues(doc, quantities, code=False)):
                amount[i] += v
        return amount

    def _updatebalance(self, doc, positive=True):
        pass

    def destroy(self):
        self.getStrcture().unsubscribe(self)
