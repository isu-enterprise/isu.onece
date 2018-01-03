from zope.interface import implementer
from isu.onece.interfaces import IVocabularyItem
from isu.onece.interfaces import IAccumulatorRegister, IDocument, IFlowDocument
from isu.onece import AccumulatorRegister
from isu.onece import VocabularyItem, Dimention, Quantity
import datetime
from nose.tools import nottest
from zope.schema import Float


class TestReferenceBook:

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_minimal(self):
        @implementer(IVocabularyItem)
        class RefBook(object):

            def __init__():
                pass


@implementer(IDocument)
class TestDoc(object):
    def __init__(self, code, title, number, date):
        self.code = code
        self.title = title
        self.number = number
        self.date = date


@implementer(IFlowDocument)
class TestDocFlow(TestDoc):
    def __init__(self, code, title, number, date, amount, receipt=True):
        super(TestDocFlow, self).__init__(code, title,
                                          number, date)
        self._amount = amount
        self.receipt = receipt

    def amount(self, axes=None):  # Axis - sing. Axes - plur.
        return self._amount


class TestAccumulatorRegistry:
    def setUp(self):
        d = TestDocFlow(code=1,
                        title="Document-1",
                        number="123424PQ",
                        date=datetime.date(year=2017, month=4, day=24),
                        amount=1000
                        )
        self.doc = d
        self.reg = AccumulatorRegister()

    def create_doc(self, number, amount, receipt=True):
        d = TestDocFlow(code=2123,
                        title="Document-1234",
                        number="123424PQ1234",
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
        assert abs(self.reg.balance() - am) < 0.0001


class IDepartment(IVocabularyItem):
    """Marker interface denoting departments of an
    enterprise.
    """


class IKassaRecord(IDocument):
    department = VocabularyItem(IDepartment)
    amount = Float(
        title="Amount",
        description="Amount of money"
    )


class IPurse(IAccumulatorRegister):
    department = Dimention(
        IKassaRecord, "department"
    )
    amount = Quantity(
        IKassaRecord, "amount"
    )


@implementer(IVocabularyItem)
class Department(object):
    def __init__(self, code, title):
        self.code = code
        self.title = title


@implementer(IKassaRecord)
class KassaRecord(object):

    def _getnumber(self):
        return self.code

    def _setnumber(self, value):
        self.code = value

    number = property(_getnumber, _setnumber)

    def __init__(self, number, title, department, amount):
        self.number = number
        self.title = title
        self.department = department
        self.amount = amount


@implementer(IPurse)
class Purse(AccumulatorRegister):
    pass


doc_num = 1

dep1 = Department(1, "The first department")
dep2 = Department(2, "The second department")
dep3 = Department(3, "The third department")
departments = [dep1, dep2, dep3]


class TestPurse:
    def new_doc(self, amount):
        global doc_num
        a = str(amount)
        d = datetime.datetime.now()
        title = "{}-{}-{}".format(KassaRecord.__name__, str(d), a)
        num = doc_num
        doc_num += 1
        dep = departments[doc_num % len(departments)]
        return KassaRecord(num, title, dep, amount)

    def test_doc(self):
        amount = 100
        d = self.new_doc(amount)
        assert d.amount == amount
