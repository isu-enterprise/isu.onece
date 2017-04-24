from zope.interface import implementer
from isu.onece.interfaces import IVocabularyItem
from isu.onece.interfaces import IAccumulatorRegister, IDocument
from isu.onece.registers import AccumulatorRegister
import datetime


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
        self.code=code
        self.title=title
        self.number=number
        self.date=date
        
class TestDocFlow(TestDoc):
    def __init__(self, code, title, number, date, receipt=True):
        super(TestDocFlow, self).__init__(code, title, number, date)
        self.receipt = receipt
    

class TestAccumulatorRegistry:
    def setUp(self):
        d=TestDocFlow(code=1, 
            title="Document-1", 
            number="123424PQ", 
            date=datetime.date(year=2017, month=4, day=24))
        self.doc = d
        self.reg = AccumulatorRegister()
        
    def test_implementation(self):
        assert IAccumulatorRegister.implementedBy(AccumulatorRegister)
        
    def test_document_impl(self):
        assert IDocument.implementedBy(TestDoc)
        
    def test_document(self):
        assert IDocument.providedBy(self.doc)
        
    def test_add_document(self):
        self.reg.add(self.doc)
        assert len(self.reg.documents())>0
        assert self.reg.documents()[0] == self.doc
        self.reg.remove(self.doc)
        assert len(self.reg.documents())==0
        