from zope.interface import implementer, providedBy
from zope.component import getGlobalSiteManager
from isu.onece.interfaces import IRecord
from isu.onece.interfaces import IAccumulatorRegister, IDocument, IFlowDocument
from isu.onece.interfaces import IDocumentEvent, IDocumentAccepted
from isu.onece import AccumulatorRegister
from isu.onece import Record, Dimension, Quantity
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
        self.reg = AccumulatorRegister()

    def create_doc(self, number, amount, receipt=True):
        d = TestDocFlow(

            number=number,
            date=datetime.date(year=2017, month=4, day=24),
            receipt=receipt,
            amount=amount
        )
        return d

    def test_implementation(self):
        assert IAccumulatorRegister.implementedBy(AccumulatorRegister)

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


class IKassaRecord(IDocument):
    department = Record(IDepartment)
    amount = zope.schema.Float(
        title="Amount",
        description="Amount of money"
    )


# class IPurse(IAccumulatorRegister):
#     department = Dimension(
#         fieldname="department"
#     )
#     amount = Quantity(
#         fieldname="amount"
#     )
#     # FIXME: Delay the requisite implementation
#     #@requisite
#     # text=accessor
#     #@requisite
#     # def requisite method.


@implementer(IDepartment)
class Department(object):
    def __init__(self, code, title):
        self.code = code
        self.title = title


@implementer(IKassaRecord)
class KassaRecord(DocumentBase):
    def __init__(self, number, date, department, amount):
        super(KassaRecord, self).__init__(number=number, date=date)
        self.department = department
        self.amount = amount
        self._notify_created()

    def __str__(self):
        return "{}(dep={},amount={} at {})".format(self.__class__.__name__,
                                                   self.department,
                                                   self.amount,
                                                   self.date)


class Purse(AccumulatorRegister):
    def __init__(self, interface):
        super(Purse, self).__init__(interface)
        self.total_amount = 0

    def onRejected(self, doc):
        self.total_amount += doc.amount

    def onAccepted(self, doc):
        self.total_amount += doc.amount
        print("Accept:", doc.amount, self.total_amount)


doc_num = 1

dep1 = Department(1, "The first department")
dep2 = Department(2, "The second department")
dep3 = Department(3, "The third department")

departments = [dep1, dep2, dep3]


class TestPurse:

    def setUp(self):
        self.doc = self.new_doc(1000)
        p = self.purse = Purse(IKassaRecord)
        p.addDimension("department")
        p.addQuantities("amount")

    def tearDown(self):
        self.purse.destroy()

    def test_add_document(self):
        self.purse.add(self.doc)
        assert self.purse.balance()[0] == 0
        self.doc.accept()
        assert self.purse.balance()[0] == 1000

    def test_add_documents(self):
        assert self.purse.total_amount == 0
        SM = getGlobalSiteManager()

        self.acc_s = 0.0

        def accept_handler(doc):
            self.acc_s += doc.amount
            print("Accepted:", doc.amount, self.acc_s)

        SM.registerSubscriptionAdapter(
            accept_handler, (IDocument,), IDocumentAccepted)

        s = 0
        for i in range(10):
            am = random.randint(1, 10000)
            doc = self.new_doc(amount=am)
            # self.purse.add(doc)
            s += am
            doc.accept()
        # pprint(list(self.purse.documents())[:100])
        # assert self.purse.balance(accepted=False)[0] == s
        for doc in self.purse.documents(accepted=False):
            assert False
            doc.accept()
        # assert self.purse.balance()[0] == s
        assert self.acc_s == s
        print(self.purse.total_amount, s)
        assert self.purse.total_amount == s
        SM.unregisterSubscriptionAdapter(
            accept_handler, (IDocument,), IDocumentAccepted)

    def new_doc(self, amount):
        global doc_num
        a = str(amount)
        d = datetime.datetime.now()
        num = doc_num
        doc_num += 1
        dep = departments[doc_num % len(departments)]
        date = datetime.datetime.utcnow()
        return KassaRecord(num, date, dep, amount)

    def test_doc(self):
        amount = 100
        d = self.new_doc(amount)
        assert d.amount == amount
