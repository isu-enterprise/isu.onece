from .interfaces import IDocument, IAccumulatorRegister
from zope.interface import implementer

@implementer(IAccumulatorRegister)
class AccumulatorRegister(object):
    """Accumulates amounts by means of
    accumulating document'S data.
    """

    def __init__(self):
        super(AccumulatorRegister, self).__init__()
