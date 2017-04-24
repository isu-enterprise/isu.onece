from .interfaces import IDocument, IAccumulatorRegister
from zope.interface import implementer

@implementer(IAccumulatorRegister)
class AccumulatorRegister(object):
    """Accumulates amounts by means of
    accumulating document'S data.
    """
    

    def __init__(self):
        super(AccumulatorRegister, self).__init__()
        self._documents=[]
        
    def add(self, doc):
        assert IDocument.providedBy(doc), "argument must be IDocument provider"
        self._documents.append(doc)
        return doc
        
    def remove(self, doc):
        assert IDocument.providedBy(doc), "argument must be IDocument provider"
        self._documents.remove(doc)
        return doc
        
    def documents(self, filter=None):
        return self._documents
            
        
