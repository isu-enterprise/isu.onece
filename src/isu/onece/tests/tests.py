from zope.interface import implementer
from isu.onece.interfaces import IVocabularyItem
from isu.onece.interfaces import IAccumulatorRegister, IDocument, IFlowDocument
from isu.onece.registers import AccumulatorRegister
import datetime
from nose.tools import nottest


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
    def __init__(self, code, title, number, date, receipt=True):
        super(TestDocFlow, self).__init__(code, title, number, date)
        self._amount = 100
        self.receipt = receipt

    def amount(self, axes=None):  # Axis - sing. Axes - plur.
        return self._amount


class TestAccumulatorRegistry:
    def setUp(self):
        d = TestDocFlow(code=1,
                        title="Document-1",
                        number="123424PQ",
                        date=datetime.date(year=2017, month=4, day=24))
        self.doc = d
        self.reg = AccumulatorRegister()

    def create_doc(self, number, amount, receipt=True):
        d = TestDocFlow(code=2123,
                        title="Document-1234",
                        number="123424PQ1234",
                        date=datetime.date(year=2017, month=4, day=24),
                        receipt=receipt)
        d._amount = amount
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
