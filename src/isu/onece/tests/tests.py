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
    

class TestAccumulatorRegistry:
    def setUp(self):
        pass
        
    def test_implementation(self):
        assert IAccumulatorRegister.implementedBy(AccumulatorRegister)
        
    def test_document_impl(self):
        assert IDocument.implementedBy(TestDoc)
        
    def test_document(self):
        d=TestDoc(code=1, 
            title="Document-1", 
            number="123424PQ", 
            date=datetime.date(year=2017, month=4, day=24))
        assert IDocument.providedBy(d)