from isu.onece.register.interfaces import IAccumulatorRegister, IDocumentRegister
from isu.onece.interfaces import IDocument
from zope.interface import implementer, implementedBy
import zope.schema
from collections import OrderedDict
from isu.onece.register.interfaces import IDimesion, IQuality, IRecordRegister
from isu.onece.interfaces import IRecordCreated, IRecordAboutToBeDeleted
from isu.onece.interfaces import IDocumentAccepted, IDocumentRejected
from zope.component import getGlobalSiteManager
from asq.initiators import query


class RegisterStructure(object):
    """The container of the register structure"""

    def __init__(self, interface):
        self.interface = interface
        self.subscibers = {}

    EVENTS = []

    def subscribe(self, register, interface=None):
        if self.subscibers:
            return
        GM = getGlobalSiteManager()
        rg = GM.registerSubscriptionAdapter
        i = interface or self.interface or zope.interface.Interface
        for event, methodname in self.__class__.EVENTS:
            method = getattr(register, methodname)
            rg(method, (i,), event)
            self.subscibers[event] = method

    def unsubscribe(self, register, interface=None):
        if not self.subscibers:
            return
        GM = getGlobalSiteManager()
        urg = GM.unregisterSubscriptionAdapter
        i = interface or self.interface or zope.interface.Interface
        for event, methodname in self.__class__.EVENTS:
            method = self.subscibers[event]
            urg(method, (i,), event)
            del self.subscibers[event]


class RecordRegisterStructure(RegisterStructure):

    EVENTS = RegisterStructure.EVENTS + [
        (IRecordCreated, "onRecordCreated"),
        (IRecordAboutToBeDeleted, "onRecordAboutToBeDeleted")
    ]


class DocumentRegisterStructure(RecordRegisterStructure):
    """The container of the register structure"""

    EVENTS = RecordRegisterStructure.EVENTS + [
        (IDocumentAccepted, "onDocumentAccepted"),
        (IDocumentRejected, "onDocumentRejected")
    ]


class StructuredRegisterBase(object):
    """Implements a simile register functionality.

    The user has the responsibility that the supplied documents will
    have the reference fields
    """

    __structure__type__ = None

    def __init__(self, interface=None):
        stype = self.__class__.__structure__type__

        if stype is None:
            raise ValueError("the class is not set up properly")

        self.__structure__ = stype(interface)
        if interface is not None:
            self.bind(interface)

    def bind(self, object_or_interface):
        self.getStrcture().subscribe(self, object_or_interface)

    def getStrcture(self):
        return self.__structure__

    # def onRecordCreated(self, doc):
    #     pass

    # def onRecordAboutToBeDeleted(self, doc):
    #     pass

    def __del__(self):
        self.destroy()

    def destroy(self):
        self.getStrcture().unsubscribe(self)


@implementer(IRecordRegister)
class RecordRegisterBase(StructuredRegisterBase):
    __structure__type__ = RecordRegisterStructure


@implementer(IDocumentRegister)
class DocumentRegisterBase(RecordRegisterBase):

    __structure__type__ = DocumentRegisterStructure


class SimpleRecordRegister(RecordRegisterBase):
    def __init__(self, interface):
        super(SimpleRecordRegister, self).__init__(interface)
        self.records = OrderedDict()

    def onRecordCreated(self, doc):
        self.records[doc.code] = doc

    def onRecordAboutToBeDeleted(self, doc):
        del self.records[doc.code]

    def query(self, collection=None):
        if collection is not None:
            return query(collection)

        return self.query(collection=self.records)

    def __len__(self):
        return len(self.records)

    def __getitem__(self, index):
        k = list(self.records.keys())[index]
        return self.records[k]


class SimpleDocumentRegister(SimpleRecordRegister):

    def __init__(self, interface):
        super(SimpleDocumentRegister, self).__init__(interface)
        self.accepted = OrderedDict()

    def _getDocuments(self):
        return self.records

    documents = property(_getDocuments)

    def onDocumentAccepted(self, doc):
        self.accepted[doc.code] = doc

    def onDocumentRejected(self, doc):
        del self.accepted[doc.code]

    def query(self, accepted=True, collection=None):
        if accepted:
            collection = self.accepted
        return super(SimpleDocumentRegister, self).query(collection=collection)


# @implementer(IAccumulatorRegister)
# class AccumulatorRegister(SimpleRegisterBase):
#     """Accumulates amounts by means of
#     accumulating document's data.
#     """

#     def balance(self, **kw):
#         # TODO: date and dimensions must be supplied explicitly.
#         # return self._balance
#         quantities = self.getStrcture().quantities
#         amount = [0.0] * len(quantities)
#         for doc in self.query(**kw):
#             for i, v in enumerate(self._getValues(doc, quantities, code=False)):
#                 amount[i] += v
#         return amount

#     def _updatebalance(self, doc, positive=True):
#         pass

#     def destroy(self):
#         self.getStrcture().unsubscribe(self)
