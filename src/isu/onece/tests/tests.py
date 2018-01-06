from zope.interface import implementer, providedBy
from zope.component import getGlobalSiteManager, getUtility
from isu.onece.interfaces import IRecord
from isu.onece.register.interfaces import IAccumulatorRegister
from isu.onece.interfaces import IDocument, IFlowDocument
from isu.onece.interfaces import IDocumentEvent, IDocumentAccepted
# from isu.onece import AccumulatorRegister
from isu.onece.register import SimpleRecordRegister, SimpleDocumentRegister
from isu.onece.register import SimpleAccumulatorRegister
from isu.onece import Record, Dimension, Quantity, RecordRef
import datetime
from nose.tools import nottest
import zope.schema
from nose.plugins.skip import SkipTest
from isu.onece import DocumentBase
import random
from pprint import pprint


_N = str


class TestReferenceBook:

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_minimal(self):  # FIXME: Stupid test
        @implementer(IRecord)
        class RefBook(object):

            def __init__():
                pass


class TestDoc(DocumentBase):
    """Just stub document"""


@implementer(IFlowDocument)
class TestDocFlow(TestDoc):
    def __init__(self, number, date, amount, receipt=True):
        super(TestDocFlow, self).__init__(number, date)
        self._amount = amount
        self.receipt = receipt

    def amount(self, axes=None):  # Axis - sing. Axes - plur.
        return self._amount


@SkipTest
class TestAccumulatorRegistry:
    def setUp(self):
        d = TestDocFlow(number="123424PQ",
                        date=datetime.date(year=2017, month=4, day=24),
                        amount=1000
                        )
        self.doc = d
        self.reg = SimpleAccumulatorRegister()

    def create_doc(self, number, amount, receipt=True):
        d = TestDocFlow(

            number=number,
            date=datetime.date(year=2017, month=4, day=24),
            receipt=receipt,
            amount=amount
        )
        return d

    def test_implementation(self):
        assert IAccumulatorRegister.implementedBy(SimpleAccumulatorRegister)

    def test_document_impl(self):
        assert IDocument.implementedBy(TestDoc)

    def test_document(self):
        assert IDocument.providedBy(self.doc)

    #@nottest
    def test_add_document(self):
        self.reg.add(self.doc)
        assert len(self.reg.documents()) > 0
        assert self.reg.documents()[0] == self.doc
        self.reg.remove(self.doc)
        assert len(self.reg.documents()) == 0

    def test_accumulator(self):
        am = 1000.0
        d = self.create_doc("123", am, True)
        self.reg.add(d)
        assert abs(self.reg.balance()[0] - am) < 0.0001


class IDepartment(IRecord):
    """Marker interface denoting departments of an
    enterprise.
    """
    title = zope.schema.TextLine(title=_N("Title"),
                                 description=_N("Title of the item of the "
                                                "catalog"),
                                 required=True,
                                 constraint=lambda x: x.strip())


class ICashRecord(IDocument):
    department = RecordRef(IDepartment)
    amount = zope.schema.Float(
        title="Amount",
        description="Amount of money"
    )


@implementer(IDepartment)
class Department(Record):
    def __init__(self, code, title):
        self.code = code
        self.title = title
        self.created()

    def __str__(self):
        return "{}({}={})".format(self.__class__.__name__,
                                  self.code, self.title)


doc_num = 1


departments = SimpleRecordRegister(IDepartment)

dep3 = Department(3, "The third department")
dep2 = Department(2, "The second department")
dep1 = Department(1, "The first department")


class TestRecordRegister:
    def setUp(self):
        self.cachbox = SimpleRecordRegister(ICashRecord)

    def tearDown(self):
        self.cachbox.destroy()


@implementer(ICashRecord)
class CashRecord(DocumentBase):
    def __init__(self, number, date, department, amount):
        super(CashRecord, self).__init__(number=number, date=date)
        self.department = department
        self.amount = amount
        self.created()

    def __str__(self):
        return "{}(dep={},amount={} at {})".format(self.__class__.__name__,
                                                   self.department,
                                                   self.amount,
                                                   self.date)


class PurseRecords(SimpleDocumentRegister):
    pass


class Purse(SimpleAccumulatorRegister):
    def __init__(self, interface):
        super(Purse, self).__init__(interface)
        self.total_amount = 0

    def onDocumentRejected(self, doc):
        # print("Rej:", doc)
        self.total_amount -= doc.amount
        super(Purse, self).onDocumentRejected(doc)

    def onDocumentAccepted(self, doc):
        # print("Acc:", doc)
        self.total_amount += doc.amount
        super(Purse, self).onDocumentAccepted(doc)

    def onRecordCreated(self, rec):
        we
        pass

    def onRecordAboutToBeDeleted(self, rec):
        er
        pass


class TestPurse:

    def setUp(self):
        self.docs = PurseRecords(ICashRecord)
        p = self.purse = Purse(ICashRecord)
        p.addDimension("department")
        p.addQuantities("amount")

        self.doc = self.new_doc(1000, dep=dep1)

    def tearDown(self):
        self.purse.destroy()

    def test_utilities(self):
        docs = self.docs
        docs2 = getUtility(ICashRecord, name="document-register")
        assert docs is docs2

    def test_add_document(self):

        assert self.purse.value() == {}
        self.doc.accept()
        assert self.purse.value() == {(1,): (1000,)}
        assert self.purse.value((dep1,))[0] == 1000  # FIXME: This is wrong

    def test_add_documents(self):
        assert self.purse.total_amount == 0
        SM = getGlobalSiteManager()

        s = 0
        for i in range(10):
            am = random.randint(1, 10000)
            doc = self.new_doc(amount=am)
            s += am
            doc.accept()

        assert self.purse.total_amount == s
        s1 = s

        self.acc_s = 0

        def accept_handler(doc):
            self.acc_s += doc.amount

        SM.registerSubscriptionAdapter(
            accept_handler, (IDocument,), IDocumentAccepted)

        s = 0

        docs = []
        for i in range(10):
            am = random.randint(1, 10000)
            doc = self.new_doc(amount=am)
            docs.append(doc)
            s += am
            doc.accept()

        SM.unregisterSubscriptionAdapter(
            accept_handler, (IDocument,), IDocumentAccepted)

        # assert self.purse.balance()[0] == s
        assert self.acc_s == s
        assert self.purse.total_amount == s + s1

    def new_doc(self, amount, dep=None):
        global doc_num
        a = str(amount)
        d = datetime.datetime.now()
        num = doc_num
        doc_num += 1
        if dep is None:
            dep = departments[doc_num % len(departments)]
        date = datetime.datetime.utcnow()
        return CashRecord(num, date, dep, amount)

    def test_doc(self):
        amount = 100
        d = self.new_doc(amount)
        assert d.amount == amount
